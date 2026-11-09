// Watch page: embeds the channel's "uploads" playlist (channel ID UCxxx -> playlist UUxxx).
// New videos appear automatically; no API key or server needed.
async function loadJSON(p){const r=await fetch(p,{cache:'no-cache'});if(!r.ok)throw new Error(p+' '+r.status);return r.json()}
const player=document.getElementById('player');
if(player){loadJSON('config.json').then(c=>{
  const f=document.createElement('iframe');f.className='video';f.allowFullscreen=true;f.loading='lazy';
  f.title='Church YouTube channel';
  f.src='https://www.youtube-nocookie.com/embed/videoseries?list=UU'+c.youtubeChannelId.slice(2);
  player.replaceChildren(f)})}
// Gallery: albums listed in gallery/albums.json (run tools/make_manifest.py). Each album has its own link: gallery.html#<album-id>
const aEl=document.getElementById('albums');
if(aEl){let albums=[],cur=[],idx=0,shown=0;const PAGE=60,more=document.getElementById('more');const lb=document.getElementById('lb'),photos=document.getElementById('photos'),sec=document.getElementById('album'),msg=document.getElementById('msg');
  const el=(t,p={},...k)=>{const e=document.createElement(t);Object.assign(e,p);e.append(...k);return e};
  const show=i=>{idx=(i+cur.length)%cur.length;const p=cur[idx];lb.querySelector('img').src=p.src;lb.querySelector('img').alt=p.cap;const q=lb.querySelector('p');q.textContent=p.cap;if(p.link)q.append(' · ',el('a',{href:p.link,target:'_blank',rel:'noopener noreferrer'},'Flickr'));if(!lb.open)lb.showModal()};
  function render(){const id=decodeURIComponent(location.hash.slice(1));const a=albums.find(x=>x.id===id);
    sec.hidden=!a;aEl.hidden=!!a;msg.textContent='';
    if(!a){document.title='갤러리 · 주은혜 교회';return}
    document.title=a.title+' · 주은혜 교회';document.getElementById('atitle').textContent=a.title+(a.title_en?' · '+a.title_en:'');
    cur=a.photos.map(p=>{const c=p.caption||a.title;if(a.remote)return{src:p.url,thumb:p.thumb,link:p.link,cap:c};const u='gallery/albums/'+a.id+'/'+p.file;return{src:u,thumb:u,cap:c}});const fl=document.getElementById('flink');fl.hidden=!a.link;if(a.link)fl.href=a.link;
    photos.replaceChildren();shown=0;addMore();window.scrollTo(0,0)}
  function addMore(){const n=Math.min(shown+PAGE,cur.length);photos.append(...cur.slice(shown,n).map((p,k)=>{const i=shown+k,im=el('img',{src:p.thumb,alt:p.cap,loading:'lazy'});im.onclick=()=>show(i);return im}));shown=n;more.hidden=shown>=cur.length;more.textContent='더 보기 · Show more ('+(cur.length-shown)+')'}
  more.onclick=addMore;
  loadJSON('gallery/albums.json').then(list=>{albums=list;
    if(list.length)aEl.replaceChildren(...list.map(a=>{const l=el('a',{href:'#'+a.id,className:'card album'},
      el('img',{src:a.remote?a.cover:'gallery/albums/'+a.id+'/'+a.cover,alt:'',loading:'lazy'}),el('b',{},a.title),el('small',{},a.photos.length+' 장 · photos'+(a.date?' · '+a.date:'')));return l}));
    render()});
  addEventListener('hashchange',render);
  document.getElementById('share').onclick=async()=>{const url=location.href,t=document.getElementById('atitle').textContent;
    try{if(navigator.share){await navigator.share({title:t,url});return}await navigator.clipboard.writeText(url);msg.textContent='링크가 복사되었습니다 · Link copied'}catch(e){msg.textContent=url}};
  document.getElementById('prev').onclick=()=>show(idx-1);document.getElementById('next').onclick=()=>show(idx+1);document.getElementById('close').onclick=()=>lb.close();
  lb.addEventListener('keydown',e=>{if(e.key==='ArrowLeft')show(idx-1);if(e.key==='ArrowRight')show(idx+1)})}

// Home page: 3 newest albums
const rec=document.getElementById('recent');
if(rec){loadJSON('gallery/albums.json').then(list=>{
  const top=[...list].sort((a,b)=>(b.date||'').localeCompare(a.date||'')).slice(0,3);
  if(!top.length){rec.textContent='사진을 준비 중입니다. · Photos coming soon.';return}
  rec.replaceChildren(...top.map(a=>{const l=document.createElement('a');l.href='gallery.html#'+encodeURIComponent(a.id);l.className='card album';
    const i=document.createElement('img');i.src=a.remote?a.cover:'gallery/albums/'+a.id+'/'+a.cover;i.alt='';i.loading='lazy';
    const t=document.createElement('b');t.textContent=a.title;const s=document.createElement('small');s.textContent=a.photos.length+' 장 · photos'+(a.date?' · '+a.date:'');
    l.append(i,t,s);return l}))}).catch(()=>{rec.textContent='사진을 불러올 수 없습니다. · Could not load photos.'})}
