'use strict';
(() => {
  const payload = JSON.parse(document.getElementById('tie-payload').textContent);
  let {view, build} = payload;
  let M = payload.messages;
  let liveStatus = build.status ?? null;
  let revision = build.revision ?? null;
  let liveSignature = null;
  let poll = () => {};
  const $ = selector => document.querySelector(selector);
  const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const t = key => esc(M[key] ?? key);
  let records = new Map(view.records.map(r => [r.id, r]));
  let sources = new Map(view.sources.map(s => [s.id, s]));
  let citations = new Map(view.citations.map(c => [c.id, c]));
  let events = new Map(view.events.map(e => [e.id, e]));
  const categories = ['intent', 'taste', 'eval'];
  const tabs = ['content', 'relations', 'changes', 'sources'];
  const state = {page:'overview', selected:view.records[0]?.id ?? null, tab:'content', event:view.events.at(-1)?.id ?? null, query:'', filter:'active', modal:null, modalTab:'content', stack:[]};
  const match = r => [r.id,r.title,r.summary,r.implication,...r.citations.map(id => citations.get(id).excerpt)].join(' ').toLocaleLowerCase('en').includes(state.query.toLocaleLowerCase('en'));
  const filtered = () => view.records.filter(r => match(r) && (state.filter === 'all' || r.status === 'active'));
  const badge = key => `<span class="tag ${key === 'proposal' || key === 'unknown' ? 'proposal' : ''}">${t(key)}</span>`;
  const button = (action, value, label, cls='textbutton') => `<button class="${cls}" data-${action}="${esc(value)}">${label}</button>`;
  const empty = key => `<div class="empty">${t(key)}${state.query ? `<div>${button('action','clear',t('clear'),'pill')}</div>` : ''}</div>`;
  const recordButton = r => `<button class="judgment" data-record="${esc(r.id)}"><span class="jtitle"><span>${esc(r.title)}</span><span aria-hidden="true">↗</span></span>${badge(r.authority)} ${badge(r.evidence)}${r.status !== 'active' ? badge(r.status):''}</button>`;
  const linked = (r, label) => `<button class="linkedrow" data-record="${esc(r.id)}"><span class="mono ${r.category}">${esc(r.id)}</span><span class="linkbody">${esc(r.title)}<small>${t(r.category)} · ${t(r.status)}</small></span><span class="linktype">${label}</span><span aria-hidden="true">→</span></button>`;
  function sourceMarkup(ids) {
    return ids.length ? ids.map(id => {
      const c = citations.get(id), s = sources.get(c.source);
      return `<section class="source-card"><div class="eyebrow">${esc(c.anchor)}</div><div class="sourcepath">${esc(s.path)}<br><span class="muted">${t('lines')} ${c.start}–${c.end} · ${t('language')}: ${esc(s.language)}</span></div><pre class="sourceexcerpt">${esc(c.excerpt)}</pre><details><summary class="small muted">${t('fingerprint')}</summary><p class="sourcehash">${esc(s.sha256)}</p></details></section>`;
    }).join('') : empty('sourceUnavailable');
  }
  function recordHead(r) {
    return `<header class="recordhead"><div class="row between"><span class="eyebrow ${r.category}">${t(r.category)}</span><span class="mono">${t('viewId')} ${esc(r.id)}</span></div><h1>${esc(r.title)}</h1><p class="recordlead">${esc(r.summary)}</p><div class="recordmeta">${badge(r.authority)}${badge(r.evidence)}${badge(r.status)}</div></header>`;
  }
  function recordTabs(active) {
    return `<nav class="tabs rule" aria-label="${t('detailTabs')}">${tabs.map(tab => `<button data-tab="${tab}" aria-pressed="${active === tab}">${t(tab)}</button>`).join('')}</nav>`;
  }
  function recordBody(r, active) {
    const connections = view.relations.filter(x => x.from === r.id || x.to === r.id);
    if(active === 'sources') return `<p class="small muted">${t('sourceNote')}</p>${sourceMarkup(r.citations)}`;
    if(active === 'relations') return `<p class="relcaption">${t('relationNote')}</p><div class="relcenter"><span class="eyebrow">${t('focus')}</span><h3>${esc(r.title)}</h3></div><div class="relnodes">${['incoming','outgoing'].map((dir,i) => {
      const links = connections.filter(x => i === 0 ? x.to === r.id : x.from === r.id);
      return `<section class="relblock"><h3>${t(dir)}</h3>${links.length ? links.map(x => `<div>${linked(records.get(i === 0 ? x.from : x.to),t(x.kind))}<p class="small muted">${t(x.basis)} · ${esc(x.note)}</p>${x.citations.length ? `<details><summary class="small">${t('sources')}</summary>${sourceMarkup(x.citations)}</details>`:''}</div>`).join('') : `<p class="small muted">${t('noRelations')}</p>`}</section>`;
    }).join('')}</div>`;
    if(active === 'changes') {
      const related = view.events.filter(e => e.records.includes(r.id));
      return `<p class="lineage-note">${t('evolutionNote')}</p>${related.length ? related.map(e => `<div class="changeitem"><span class="mono">${esc(e.id)}</span><div class="grow"><h3>${esc(e.title)}</h3><p class="small muted">${esc(e.summary)}</p>${button('event',e.id,t('changeContext'))}</div></div>`).join('') : empty('noEvents')}`;
    }
    return `<div class="prose"><h3>${t('implication')}</h3><p>${esc(r.implication)}</p><dl class="properties"><dt>${t('scope')}</dt><dd>${esc(r.scope)}</dd><dt>${t('authority')}</dt><dd>${t(r.authority)}</dd><dt>${t('evidence')}</dt><dd>${t(r.evidence)}</dd><dt>${t('classification')}</dt><dd>${t(r.category)}<br><span class="small muted">${t('classificationNote')}</span></dd></dl><p class="small muted">${t('readOnly')}</p><h3>${t('trace')}</h3>${connections.slice(0,3).map(x => linked(records.get(x.from === r.id ? x.to : x.from),t(x.kind))).join('')}${button('tab','sources',t('sourceAction'),'pill')}</div>`;
  }
  function overview() {
    const visible = view.records.filter(r => r.status === 'active' && match(r));
    const attention = visible.filter(r => r.authority === 'unknown' || r.evidence === 'unverified');
    return `<div class="content">${view.reconciliation === 'pending' ? `<aside class="warning"><strong>${t('pending')}</strong><p>${t('pendingNote')}</p></aside>`:''}<header class="intro"><div class="eyebrow">${t('reading')} / ${esc(view.project.name)}</div><h1>${esc(view.overview.headline)}</h1><p>${esc(view.overview.summary)}</p><div class="contextline"><span>${t('session')}: ${esc(view.project.session)}</span><span>${view.records.length} ${t('recordCount')}</span><span>${t('captured')}: ${esc(view.generatedAt)}</span></div></header><div class="sectiontitle"><h2>${t('current')}</h2>${button('page','records',t('records')+' →')}</div><div class="three">${categories.map(cat => `<section class="group"><div class="grouphead row"><span class="letter ${cat}">${cat[0].toUpperCase()}</span><div><div class="eyebrow ${cat}">${t(cat)}</div><span class="small muted">${t(cat+'Question')}</span></div></div>${visible.filter(r => r.category === cat).map(recordButton).join('') || empty(state.query?'noMatches':'noRecords')}</section>`).join('')}</div><div class="below"><section><div class="sectiontitle"><h3>${t('recent')}</h3>${button('page','evolution',t('viewAll'))}</div>${view.events.slice(-3).reverse().map(e => `<button class="event-link" data-event="${esc(e.id)}"><span class="mono">${esc(e.id)}</span> &nbsp; ${esc(e.title)}<small>${esc(e.summary)}</small></button>`).join('') || empty('noEvents')}</section><aside><section class="note"><h3>${t('scope')}</h3><p>${esc(view.overview.scope)}</p><h3>${t('next')}</h3><p>${esc(view.overview.next)}</p></section>${attention.length ? `<section class="note"><h3>${t('attention')}</h3>${attention.map(r => linked(r,t(r.evidence))).join('')}</section>`:''}<section class="note"><h3>${t('coverage')}</h3><p>${esc(view.overview.coverage)}</p></section></aside></div></div>`;
  }
  function directory() {
    const list=filtered(), chosen=records.get(state.selected);
    return `<div class="outline"><aside class="explorer" aria-label="${t('recordList')}"><div class="filter" role="group" aria-label="${t('filterLabel')}">${['active','all'].map(f => `<button class="pill" data-filter="${f}" aria-pressed="${state.filter === f}">${t(f === 'all'?'allStates':'activeOnly')}</button>`).join('')}</div>${categories.map(cat => `<div class="treehead"><span>${t(cat)}</span><span>${list.filter(r=>r.category===cat).length}</span></div>${list.filter(r => r.category===cat).map(r => `<button class="treeitem ${state.selected === r.id?'active':''}" aria-pressed="${state.selected === r.id}" data-select="${esc(r.id)}"><span class="mono ${cat}">${esc(r.id)}</span><span>${esc(r.title)}</span></button>`).join('')}`).join('')}${!list.length ? empty('noMatches'):''}</aside><section class="outmain">${chosen ? recordHead(chosen)+recordTabs(state.tab)+`<div class="recordbody">${recordBody(chosen,state.tab)}</div>` : empty('noSelection')}</section></div>`;
  }
  function evolution() {
    const list=view.events.filter(e => [e.title,e.summary,e.id].join(' ').toLocaleLowerCase('en').includes(state.query.toLocaleLowerCase('en')));
    const event=list.find(e=>e.id === state.event) ?? list.at(-1);
    return `<div class="content"><header class="intro"><div class="eyebrow">${t('evolution')}</div><h1>${t('evolutionHeading')}</h1><p>${t('evolutionNote')}</p><p class="small">${esc(view.historyCoverage)}</p></header>${!event ? empty(state.query?'noEventMatches':'noEvents') : `<div class="historylayout"><aside class="versionrail" aria-label="${t('eventList')}">${list.map(e => `<button class="versionbutton ${e.id === event.id?'active':''}" data-event="${esc(e.id)}" aria-pressed="${e.id === event.id}"><span class="mono">${esc(e.id)}</span><strong>${esc(e.title)}</strong><small>${esc(e.when)}</small></button>`).join('')}</aside><section class="historypane"><span class="eyebrow">${esc(event.id)} / ${esc(event.when)}</span><h1>${esc(event.title)}</h1><p class="lead">${esc(event.summary)}</p><div class="compare"><div><h3>${t('before')}</h3><p>${event.before ? esc(event.before.text) : t('beforeMissing')}</p>${event.before?`<details><summary class="small">${t('sources')}</summary>${sourceMarkup(event.before.citations)}</details>`:''}</div><div><h3>${t('after')}</h3><p>${esc(event.after.text)}</p><details><summary class="small">${t('sources')}</summary>${sourceMarkup(event.after.citations)}</details></div></div><h3>${t('affected')}</h3><p class="lineage-note">${t('currentRecordWarning')}</p>${event.records.map(id => linked(records.get(id),t('content'))).join('')}<details class="historyquote"><summary>${t('eventEvidence')}</summary>${sourceMarkup(event.citations)}</details></section></div>`}</div>`;
  }
  function focusKey(root) {
    const a=document.activeElement;
    if(!a || !root.contains(a) || a.tagName !== 'BUTTON') return null;
    for(const key of ['page','tab','select','filter','event','record']) if(a.dataset[key]) return [key,a.dataset[key]];
    return null;
  }
  function restoreFocus(root, key) {
    if(!key) return;
    [...root.querySelectorAll('button')].find(b=>b.dataset[key[0]] === key[1])?.focus({preventScroll:true});
  }
  function render() {
    const focus=focusKey($('#app'));
    $('#navigation').innerHTML=`<div class="tabs">${['overview','records','evolution'].map(p => `<button data-page="${p}" aria-pressed="${state.page === p}">${t(p)}</button>`).join('')}</div><span class="snapshot-label">${t(build.kind === 'live' ? 'live' : 'snapshot')}</span>`;
    $('#app').innerHTML=state.page === 'overview'?overview():state.page === 'records'?directory():evolution();
    restoreFocus($('#app'),focus);
  }
  function renderModal() {
    const focus=focusKey($('#dialogcontent')), r=records.get(state.modal);
    if(!r) return;
    $('#dialogcontent').innerHTML=recordHead(r)+recordTabs(state.modalTab)+`<div class="recordbody">${recordBody(r,state.modalTab)}</div>`;
    $('#detail [data-action="back"]').disabled=!state.stack.length;
    restoreFocus($('#dialogcontent'),focus);
  }
  function openRecord(id) {
    if(!records.has(id)) return;
    if(state.modal && state.modal !== id) state.stack.push({id:state.modal,tab:state.modalTab,scroll:$('#detail').scrollTop});
    state.selected=id; state.modal=id;state.modalTab='content';renderModal();
    if(!$('#detail').open) $('#detail').showModal();
    $('#detail').scrollTop=0;
    renderLiveStatus();
  }
  function closeRecord() { if($('#detail').open) $('#detail').close(); state.modal=null;state.stack=[]; }
  document.addEventListener('click', e => {
    const b=e.target.closest('button');if(!b) return;const d=b.dataset;
    if(d.page) {closeRecord();state.page=d.page;render();$('#navigation').querySelector(`[data-page="${d.page}"]`).focus();}
    else if(d.select) {state.selected=d.select;state.tab='content';render();}
    else if(d.record) openRecord(d.record);
    else if(d.tab) {if(b.closest('#detail')){state.modalTab=d.tab;renderModal();}else{state.tab=d.tab;render();}}
    else if(d.filter) {state.filter=d.filter;render();}
    else if(d.event) {closeRecord();state.page='evolution';state.event=d.event;state.query='';$('#search').value='';render();$('#app').focus({preventScroll:true});}
    else if(d.action === 'back' && state.stack.length) {const old=state.stack.pop();state.modal=old.id;state.modalTab=old.tab;state.selected=old.id;renderModal();$('#detail').scrollTop=old.scroll;}
    else if(d.action === 'close') closeRecord();
    else if(d.action === 'about') $('#about').showModal();
    else if(d.action === 'close-about') $('#about').close();
    else if(d.action === 'recheck') poll(false);
    else if(d.action === 'clear') {state.query='';$('#search').value='';render();$('#search').focus();}
  });
  $('#search').addEventListener('input',e=>{state.query=e.target.value;render();});
  $('#detail').addEventListener('close',()=>{state.modal=null;state.stack=[];if(state.page==='records')render();});
  function localizeChrome() {
    document.documentElement.lang=view.uiLocale;
    $('#brand-label').textContent=M.brand;
    $('#project-label').textContent=`${view.project.name} / ${view.project.session}`;
    $('#search').placeholder=M.search;$('#search').setAttribute('aria-label',M.searchLabel);
    $('#about-button').textContent=M.about;$('#detail-label').textContent=M.detail;
    $('#detail').setAttribute('aria-label',M.detail);$('#detail [data-action="back"]').textContent=M.back;
    $('#detail [data-action="close"]').setAttribute('aria-label',M.close);
    $('#about [data-action="close-about"]').setAttribute('aria-label',M.close);
    $('#about-title').textContent=M.aboutTitle;
    $('#navigation').setAttribute('aria-label',M.navLabel);$('.skip').textContent=M.skip;
  }
  localizeChrome();
  function renderAbout() {
  $('#about-content').innerHTML=`<p>${t('aboutText')}</p><p class="snapshot-banner">${t(build.kind === 'live' ? 'liveNote' : 'snapshotNote')}</p><dl class="about-grid"><dt>${t('sourceRoot')}</dt><dd class="mono">${esc(build.projectRoot)}</dd><dt>${t('session')}</dt><dd>${esc(view.project.session)}</dd><dt>${t('captured')}</dt><dd>${esc(view.generatedAt)}</dd><dt>${t('checked')}</dt><dd>${esc(build.checkedAt)}</dd><dt>${t('historyCoverage')}</dt><dd>${esc(view.historyCoverage)}</dd><dt>${t('sourcesIncluded')}</dt><dd>${view.sources.map(s=>`<div class="mono">${esc(s.path)}</div>`).join('')}</dd></dl><p class="lineage-note">${t('hostSummary')}</p>`;
  }
  renderAbout();
  function renderFooter() {
    $('#footer').innerHTML=`<span>${t(build.kind === 'live' ? 'live' : 'snapshot')} · ${esc(build.checkedAt)}<br>${t(build.kind === 'live' ? 'liveNote' : 'snapshotNote')}</span><span>${t('readOnly')}</span>`;
  }
  function renderLiveStatus() {
    if(build.kind !== 'live') return;
    const status=liveStatus?.state ?? 'disconnected';
    const key=status === 'current' ? 'source_current' : status;
    const title=t(key), note=t(status+'Note');
    const signature=JSON.stringify([view.uiLocale,status,liveStatus?.issues ?? []]);
    if(signature === liveSignature) {
      $('#last-source-check').textContent=liveStatus?.checkedAt ?? build.checkedAt;
      return;
    }
    liveSignature=signature;
    const restoreCheckFocus=document.activeElement?.dataset?.action === 'recheck';
    $('#live-status').hidden=false;
    $('#live-status').dataset.state=status;
    $('#live-status').innerHTML=`<div class="grow"><strong>${title}</strong><p>${note}</p>${liveStatus?.issues?.length ? `<p class="mono">${t('changedSources')}: ${liveStatus.issues.map(i=>esc(i.path)).join(' · ')}</p>`:''}<span class="small muted" aria-live="off">${t('checked')}: <span id="last-source-check">${esc(liveStatus?.checkedAt ?? build.checkedAt)}</span></span></div>${button('action','recheck',t('recheck'),'pill')}`;
    if(restoreCheckFocus) $('#live-status [data-action="recheck"]').focus({preventScroll:true});
    $('#detail-freshness').hidden=status==='current';
    $('#detail-freshness').textContent=M[key]+' — '+M[status+'Note'];
  }
  function applySnapshot(snapshot) {
    if(!snapshot || !snapshot.status || !snapshot.view || typeof snapshot.revision !== 'string') throw new Error('Invalid update');
    const allowed=['current','stale','source_unavailable','pending','projection_error'];
    if(!allowed.includes(snapshot.status.state)) throw new Error('Invalid status');
    if(snapshot.view.project.session !== view.project.session) throw new Error('Session changed');
    if(!['en','zh-CN'].includes(snapshot.view.uiLocale)) throw new Error('Unsupported UI locale');
    const messages=snapshot.messages ?? (snapshot.view.uiLocale === view.uiLocale ? M : null);
    if(!messages || Object.keys(M).some(key=>typeof messages[key] !== 'string' || !messages[key].trim())) throw new Error('Missing locale messages');
    liveStatus=snapshot.status;
    build.checkedAt=snapshot.status.checkedAt;
    if(snapshot.revision !== revision) {
      const scroll={x:window.scrollX,y:window.scrollY,dialog:$('#detail').scrollTop};
      const navFocus=focusKey($('#navigation'));
      const expanded=[...$('#app').querySelectorAll('details')].map(d=>d.open);
      const expandedDialog=[...$('#dialogcontent').querySelectorAll('details')].map(d=>d.open);
      view=snapshot.view;M=messages;revision=snapshot.revision;
      localizeChrome();
      records=new Map(view.records.map(r=>[r.id,r]));sources=new Map(view.sources.map(r=>[r.id,r]));
      citations=new Map(view.citations.map(r=>[r.id,r]));events=new Map(view.events.map(r=>[r.id,r]));
      if(!records.has(state.selected)) state.selected=view.records[0]?.id ?? null;
      state.stack=state.stack.filter(r=>records.has(r.id));
      if(state.modal && !records.has(state.modal)) closeRecord();
      if(!events.has(state.event)) state.event=view.events.at(-1)?.id ?? null;
      render();if(state.modal)renderModal();
      restoreFocus($('#navigation'),navFocus);
      [...$('#app').querySelectorAll('details')].forEach((d,i)=>d.open=expanded[i]??false);
      [...$('#dialogcontent').querySelectorAll('details')].forEach((d,i)=>d.open=expandedDialog[i]??false);
      $('#detail').scrollTop=scroll.dialog;window.scrollTo(scroll.x,scroll.y);
      $('#project-label').textContent=`${view.project.name} / ${view.project.session}`;
      document.title=`${view.project.name} · ${M.brand}`;
      renderAbout();
    }
    build.checkedAt=snapshot.status.checkedAt;
    renderFooter();renderLiveStatus();
  }
  renderFooter();
  document.title=`${view.project.name} · ${M.brand}`;
  render();
  renderLiveStatus();
  if(build.kind === 'live') {
    poll=window.createTiePolling(applySnapshot,()=>{
      liveStatus={state:'disconnected',issues:[],checkedAt:new Date().toISOString()};renderLiveStatus();
    });
    poll();
  }
})();
