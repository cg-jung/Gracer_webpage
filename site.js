// Watch page: embeds the channel's "uploads" playlist (channel ID UCxxx -> playlist UUxxx).
// New videos appear automatically; no API key or server needed.
async function loadJSON(p){const r=await fetch(p);return r.json()}
const player=document.getElementById('player');
if(player){loadJSON('config.json').then(c=>{
  const f=document.createElement('iframe');f.className='video';f.allowFullscreen=true;f.loading='lazy';
  f.title='Church YouTube channel';
  f.src='https://www.youtube-nocookie.com/embed/videoseries?list=UU'+c.youtubeChannelId.slice(2);
  player.replaceChildren(f)})}
// Gallery: self-hosted photos listed in gallery/photos.json (see tools/make_manifest.py)
const grid=document.getElementById('photos');
if(grid){const lb=document.getElementById('lb');
  loadJSON('gallery/photos.json').then(list=>{
    if(!list.length)grid.textContent='Photos coming soon.';
    for(const p of list){const i=document.createElement('img');i.src='gallery/photos/'+p.file;i.alt=p.caption||'';i.loading='lazy';
      i.onclick=()=>{lb.querySelector('img').src=i.src;lb.querySelector('p').textContent=p.caption||'';lb.showModal()};grid.append(i)}});
  lb.onclick=()=>lb.close()}
