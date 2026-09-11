"""Explicit POSIX loopback lifecycle. No reasoning or source mutation."""
from contextlib import contextmanager
from datetime import datetime, timezone
import errno
import fcntl
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import re
import secrets
import subprocess
import sys
import tempfile
import threading
import time
from urllib.request import Request, build_opener, ProxyHandler

import tie_dashboard as D


def now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def cache_for(project, session):
    root = Path(project).resolve(strict=True)
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,63}', session):
        raise D.ProjectionError('Invalid session ID for local cache')
    cache = root / '.tie-cache' / 'dashboard' / session
    # Never follow a redirected cache into canonical or another project's files.
    for p in [root / '.tie-cache', root / '.tie-cache/dashboard', cache]:
        if p.is_symlink():
            raise D.ProjectionError('Dashboard cache must not be a symlink')
    return root, cache


def ensure_cache(cache):
    cache.mkdir(parents=True, exist_ok=True, mode=0o700)
    for name in ['view.json','process.json','lifecycle.lock','publish.lock','service.log']:
        if (cache/name).is_symlink():
            raise D.ProjectionError('Cache files must not be symlinks')


@contextmanager
def locked(cache, name):
    ensure_cache(cache)
    fd = os.open(cache/name, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, 'a') as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        yield


def atomic_json(path, data, check=None):
    fd, name = tempfile.mkstemp(dir=path.parent, suffix='.tmp')
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as handle:
            json.dump(data, handle, ensure_ascii=False, allow_nan=False)
            handle.flush(); os.fsync(handle.fileno())
        if check is not None: check()
        if path.is_symlink():
            raise D.ProjectionError('Refusing redirected cache file')
        os.replace(name, path)
    finally:
        if os.path.exists(name): os.unlink(name)


def publish(root, cache, session, view):
    if view.get('project',{}).get('session') != session:
        raise D.ProjectionError('Projection Session does not match selected Session')
    with locked(cache,'publish.lock'):
        D.validate(view, root)
        envelope = {'projectRoot':str(root),'session':session,'publishedAt':now(),'view':view}
        # Atomic replacement follows a second source-version check.
        D.validate(view, root)
        atomic_json(cache/'view.json', envelope, lambda: D.validate(view,root))
    return {'published':True,'session':session}


def read_envelope(root, cache, session):
    if (cache/'view.json').is_symlink(): raise D.ProjectionError('Redirected projection cache')
    data = D.read_bytes(cache/'view.json')
    item = json.loads(data.decode('utf-8'), object_pairs_hook=D.unique_object)
    try:
        matches=item['projectRoot']==str(root) and item['session']==session and item['view']['project']['session']==session
    except (KeyError,TypeError):
        raise D.ProjectionError('Invalid cached projection envelope')
    if not matches: raise D.ProjectionError('Cached project/Session identity mismatch')
    return item, hashlib.sha256(data).hexdigest()


def source_status(view, root):
    issues=[]
    for source in view['sources']:
        try:
            path=D.source_path(root,source['path'])
            if hashlib.sha256(D.read_bytes(path)).hexdigest()!=source['sha256']:
                issues.append({'state':'stale','path':source['path']})
        except (OSError, ValueError, UnicodeError):
            issues.append({'state':'source_unavailable','path':source['path']})
    state='source_unavailable' if any(i['state']=='source_unavailable' for i in issues) else 'stale' if issues else 'pending' if view['reconciliation']=='pending' else 'current'
    return {'state':state,'issues':issues,'checkedAt':now()}


class LiveView:
    def __init__(self, root, cache, session):
        self.root,self.cache,self.session=root,cache,session
        self.lock=threading.Lock()
        self.envelope,self.revision=read_envelope(root,cache,session)
        D.validate(self.envelope['view'],root)

    def snapshot(self):
        with self.lock:
            error=False
            try:
                item,revision=read_envelope(self.root,self.cache,self.session)
                if revision!=self.revision:
                    D.validate(item['view'],self.root)
                    self.envelope,self.revision=item,revision
            except (OSError,ValueError,UnicodeError,KeyError,TypeError):
                error=True
            status=source_status(self.envelope['view'],self.root)
            if error: status['state']='projection_error'
            return {'view':self.envelope['view'],
                    'messages':D.load_messages(self.envelope['view']['uiLocale']),
                    'revision':self.revision,'status':status,
                    'publishedAt':self.envelope['publishedAt']}


def process_record(root,cache,session):
    path=cache/'process.json'
    if not path.exists():return None
    if path.is_symlink():raise D.ProjectionError('Redirected process record')
    item=D.load_json(path)
    if (item.get('projectRoot')!=str(root) or item.get('session')!=session or
        type(item.get('port')) is not int or not 1<=item['port']<=65535 or
        not re.fullmatch(r'[a-f0-9]{48}',item.get('token','')) or
        not re.fullmatch(r'[a-f0-9]{32}',item.get('instance',''))):
        raise D.ProjectionError('Invalid process identity; refusing to contact or stop it')
    return item


def request_instance(record, route='identity', method='GET'):
    url=f"http://127.0.0.1:{record['port']}/{record['token']}/{route}"
    req=Request(url,method=method)
    with build_opener(ProxyHandler({})).open(req,timeout=2) as response:
        return json.loads(response.read(D.MAX_BYTES).decode('utf-8'))


def identify(record):
    if not record:return False
    try:
        result=request_instance(record)
        return all(result.get(k)==record[k] for k in ['instance','projectRoot','session'])
    except (OSError,ValueError) as error:
        reason=getattr(error,'reason',error)
        if isinstance(reason,OSError) and reason.errno in (errno.EPERM,errno.EACCES):
            raise D.ProjectionError('Local socket access denied; instance status is unknown') from error
        return False


def public_record(record):
    return {'running':True,'pid':record['pid'],'instance':record['instance'],
            'url':f"http://127.0.0.1:{record['port']}/{record['token']}/"}


def foreground(root,cache,session,port):
    live=LiveView(root,cache,session)
    token,instance=secrets.token_hex(24),secrets.token_hex(16)
    class Handler(BaseHTTPRequestHandler):
        def log_message(self,*args):pass  # Do not log private route tokens or excerpts.
        def send(self,code,data,mime='application/json'):
            body=data.encode('utf-8') if isinstance(data,str) else json.dumps(data,ensure_ascii=False).encode('utf-8')
            self.send_response(code);self.send_header('Content-Type',mime+'; charset=utf-8')
            self.send_header('Content-Length',str(len(body)));self.send_header('Cache-Control','no-store')
            self.send_header('X-Content-Type-Options','nosniff');self.send_header('Referrer-Policy','no-referrer')
            self.send_header('X-Frame-Options','DENY');self.end_headers();self.wfile.write(body)
        def allowed(self):
            host=f'127.0.0.1:{self.server.server_port}'
            if self.headers.get('Host')!=host or self.headers.get('Origin') not in (None,'http://'+host):
                self.send(403,{'error':'Origin or Host rejected'});return False
            return True
        def do_GET(self):
            if not self.allowed():return
            base='/'+token+'/'
            if self.path==base+'identity':
                self.send(200,{'instance':instance,'projectRoot':str(root),'session':session});return
            if self.path not in (base,base+'state'):
                self.send(404,{'error':'Not found'});return
            snapshot=live.snapshot()
            if self.path==base+'state':self.send(200,snapshot);return
            build={'kind':'live','projectRoot':str(root),'checkedAt':snapshot['status']['checkedAt'],
                   'revision':snapshot['revision'],'status':snapshot['status']}
            self.send(200,D.build_html(snapshot['view'],build),'text/html')
        def do_POST(self):
            if not self.allowed():return
            if self.path!='/'+token+'/stop':self.send(404,{'error':'Not found'});return
            self.send(200,{'stopping':True,'instance':instance})
            threading.Thread(target=self.server.shutdown,daemon=True).start()
    try:server=ThreadingHTTPServer(('127.0.0.1',port),Handler)
    except OSError as error:
        if port and error.errno==errno.EADDRINUSE:server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
        else:raise
    record={'projectRoot':str(root),'session':session,'pid':os.getpid(),'port':server.server_port,
            'instance':instance,'token':token,'startedAt':now()}
    atomic_json(cache/'process.json',record)
    try:server.serve_forever(poll_interval=0.1)
    finally:
        server.server_close()
        try:
            if D.load_json(cache/'process.json').get('instance')==instance:(cache/'process.json').unlink()
        except (OSError,ValueError):pass


def start(root,cache,session,port):
    with locked(cache,'lifecycle.lock'):
        record=process_record(root,cache,session)
        if identify(record):return {**public_record(record),'reused':True}
        # A stale PID is never signaled. Start a new authenticated instance instead.
        item,_=read_envelope(root,cache,session);D.validate(item['view'],root)
        logfd=os.open(cache/'service.log',os.O_CREAT|os.O_WRONLY|os.O_APPEND|os.O_NOFOLLOW,0o600)
        with os.fdopen(logfd,'ab') as log:
            child=subprocess.Popen([sys.executable,'-B',str(Path(__file__).with_name('tie_dashboard.py')),
                '_serve','--project',str(root),'--session',session,'--port',str(port)],
                stdin=subprocess.DEVNULL,stdout=log,stderr=log,start_new_session=True,close_fds=True)
        for _ in range(80):
            if child.poll() is not None:
                raise D.ProjectionError('Local service exited; inspect '+str(cache/'service.log'))
            record=process_record(root,cache,session)
            if record and record['pid']==child.pid and identify(record):return {**public_record(record),'reused':False}
            time.sleep(0.05)
        # This exact Popen child is owned by this attempt; do not leave a failed startup behind.
        child.terminate();child.wait(timeout=3)
        raise D.ProjectionError('Local service did not become ready')


def stop(root,cache,session):
    with locked(cache,'lifecycle.lock'):
        record=process_record(root,cache,session)
        if not identify(record):return {'running':False,'stopped':False,'reason':'No matching live instance; no PID signaled'}
        response=request_instance(record,'stop','POST')
        if response.get('instance')!=record['instance']:raise D.ProjectionError('Stop identity mismatch')
        for _ in range(60):
            if not (cache/'process.json').exists():return {'running':False,'stopped':True}
            time.sleep(0.05)
        raise D.ProjectionError('Stop requested but cleanup not confirmed')


def add_commands(sub):
    for name in ['publish','serve','status','stop','_serve']:
        cmd=sub.add_parser(name,help='Local dashboard '+name)
        cmd.add_argument('--project',type=Path,required=True)
        cmd.add_argument('--session',required=True)
        if name=='publish':cmd.add_argument('--view',type=Path,required=True)
        if name in ('serve','_serve'):cmd.add_argument('--port',type=int,default=0)


def run_command(args):
    root,cache=cache_for(args.project,args.session)
    if args.command=='publish':result=publish(root,cache,args.session,D.load_json(args.view))
    elif args.command in ('serve','_serve'):
        if not 0<=args.port<=65535:raise D.ProjectionError('Port must be 0–65535')
        if args.command=='_serve':
            ensure_cache(cache);foreground(root,cache,args.session,args.port);return 0
        result=start(root,cache,args.session,args.port)
    elif args.command=='stop':result=stop(root,cache,args.session)
    else:
        record=process_record(root,cache,args.session)
        result={**public_record(record),'status':request_instance(record,'state')['status']} if identify(record) else {'running':False}
    print(json.dumps(result,ensure_ascii=False))
    return 0
