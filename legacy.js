// Old WordPress addresses -> new pages (used by the 404 page). Unknown addresses just show the help page.
const MAP={'/services':'/worship.html','/home/about_church':'/education.html','/home/about_crc':'/mission.html','/home/about_ministers':'/about.html',
 '/home/교회-연혁':'/crc.html','/home/교회-연혁-2':'/about.html#history','/sermon-2':'/watch.html','/sermon-2/강희진-목사-설교':'/watch.html',
 '/교회갤러리':'/gallery.html','/home-2/maps':'/visit.html','/home-2/contact-us':'/visit.html','/한울-한국-학교':'/education.html','/home':'/index.html','/home-2':'/index.html'};
function legacyTarget(path){let p;try{p=decodeURIComponent(path)}catch(e){p=path}p=p.split('?')[0].split('#')[0].replace(/\/+$/,'').toLowerCase();return MAP[p]||null}
window.legacyTarget=legacyTarget;
const t=legacyTarget(location.pathname);if(t&&!/404\.html$/.test(location.pathname))location.replace(t);
