// Included only in the local live page; static exports contain no network client.
window.createTiePolling = (onSnapshot, onFailure) => {
  let active=false, timer=null;
  const poll=async () => {
    if(active)return;
    clearTimeout(timer);active=true;
    const controller=new AbortController();
    const timeout=setTimeout(()=>controller.abort(),4000);
    try {
      const response=await fetch('state',{cache:'no-store',signal:controller.signal});
      if(!response.ok)throw new Error('Service unavailable');
      onSnapshot(await response.json());
    } catch (_) {onFailure();}
    finally {clearTimeout(timeout);active=false;timer=setTimeout(poll,2000);}
  };
  return poll;
};
