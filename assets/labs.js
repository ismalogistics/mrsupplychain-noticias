/* Mr. Supply Chain® M\u00e9xico Labs — workspace shell behaviour (v1.0 · 2026-10)
   Load at the END of <body>, after the tool's own script. Depends on nothing. */
(function(){
  var d=document,b=d.body;if(!b)return;
  var isApp=b.classList.contains('labs-app'),isIndex=b.classList.contains('labs-index');
  if(!isApp&&!isIndex)return;
  function $(s,r){return (r||d).querySelector(s);}
  function $$(s,r){return Array.prototype.slice.call((r||d).querySelectorAll(s));}
  function ES(){return d.documentElement.classList.contains('msc-es');}
  function L(en,es){return ES()?es:en;}

  /* ---------- toast ---------- */
  var toastEl,toastT;
  window.lbToast=function(msg){
    if(!toastEl){toastEl=d.createElement('div');toastEl.className='lb-toast';d.body.appendChild(toastEl);}
    toastEl.textContent=msg;toastEl.classList.add('on');clearTimeout(toastT);
    toastT=setTimeout(function(){toastEl.classList.remove('on');},2200);
  };

  /* ---------- tool switcher ---------- */
  $$('.tb-switch').forEach(function(sw){
    var btn=$('button',sw);if(!btn)return;
    btn.addEventListener('click',function(e){e.stopPropagation();var o=sw.classList.toggle('open');btn.setAttribute('aria-expanded',o);});
    d.addEventListener('click',function(e){if(!sw.contains(e.target)){sw.classList.remove('open');btn.setAttribute('aria-expanded','false');}});
  });

  /* ---------- help drawer (#howTo) ---------- */
  var help=$('#howTo');
  if(help){
    var scrim=d.createElement('div');scrim.className='lb-scrim';d.body.appendChild(scrim);
    help.setAttribute('role','dialog');help.setAttribute('aria-modal','false');
    help.classList.add('collapsed'); /* always start closed: help is on demand */
    function openHelp(){help.classList.remove('collapsed');scrim.classList.add('on');b.classList.add('lb-help-open');}
    function closeHelp(){help.classList.add('collapsed');scrim.classList.remove('on');b.classList.remove('lb-help-open');}
    window.toggleHowTo=function(){if(help.classList.contains('collapsed'))openHelp();else closeHelp();};
    window.lbHelp={open:openHelp,close:closeHelp};
    scrim.addEventListener('click',closeHelp);
    var hb=$('#howToBtn');if(hb){hb.setAttribute('aria-label',L('Close guide','Cerrar guía'));hb.innerHTML='';}
    var head=$('.how-to-head',help);if(head){head.removeAttribute('onclick');head.onclick=null;}
    if(hb){hb.addEventListener('click',function(e){e.stopPropagation();closeHelp();});}
    /* footer with the privacy promise */
    if(!$('.how-to-foot',help)){
      var f=d.createElement('div');f.className='how-to-foot';
      f.innerHTML='<span><span class="msc-en">Your data is processed in this browser and is not uploaded.</span><span class="msc-es">Tus datos se procesan en este navegador y no se suben.</span></span><span><span class="kbd">Esc</span></span>';
      help.appendChild(f);
    }
    d.addEventListener('keydown',function(e){
      if(e.key==='Escape'&&!help.classList.contains('collapsed')){closeHelp();}
      if(e.key==='?'&&!/INPUT|SELECT|TEXTAREA/.test((e.target||{}).tagName||'')){e.preventDefault();window.toggleHowTo();}
    });
    /* the tool's own init may have set "collapsed" from localStorage — fine; we never auto-open */
  }

  /* ---------- keyboard: "/" focuses the first search box ---------- */
  d.addEventListener('keydown',function(e){
    if(e.key==='/'&&!/INPUT|SELECT|TEXTAREA/.test((e.target||{}).tagName||'')){var s=$('input[type=search]');if(s){e.preventDefault();s.focus();s.select();}}
  });

  /* ---------- export buttons in the tool bar: delegate to the tool's own export ---------- */
  $$('[data-lb-export]').forEach(function(btn){
    btn.addEventListener('click',function(){
      var fn=btn.getAttribute('data-lb-export');
      if(typeof window[fn]==='function'){window[fn]();}
    });
  });

  /* ---------- Warehouse: show a generated plan immediately ---------- */
  if(b.getAttribute('data-tool')==='warehouse'&&typeof window.generate==='function'){
    var og=$('#outputGrid');
    if(og&&og.style.display==='none'){try{window.generate();}catch(e){}}
  }

  /* ---------- KPI Library: sidebar index, search, tier filter ---------- */
  if(b.getAttribute('data-tool')==='kpi'){
    var tree=$('#treeWrap'),nav=$('#kpiNav'),search=$('#kpiSearch'),count=$('#kpiCount'),filters=$$('#kpiTier .svc-chip');
    var tier='all',q='';
    function slug(s){return (s||'').toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');}
    function decorate(){
      if(!tree)return;
      /* "All domains" view: domain headers are inline-styled divs → tag them */
      Array.prototype.forEach.call(tree.children,function(el){
        if(!el.classList.contains('kpi-section')&&!el.classList.contains('kpi-empty')){el.classList.add('kpi-domain-head');}
      });
      var i=0;
      $$('.kpi-domain-head',tree).forEach(function(h){if(!h.id)h.id='dom-'+(i++)+'-'+slug(h.textContent).slice(0,40);});
      $$('.kpi-section',tree).forEach(function(s){var t=$('.kpi-section-title',s);if(!s.id)s.id='sec-'+(i++)+'-'+slug(t?t.textContent:'').slice(0,40);});
    }
    function apply(){
      if(!tree)return;
      var shown=0,total=0,ql=q.trim().toLowerCase();
      $$('.kpi-card',tree).forEach(function(c){
        total++;
        var lvl=($('.kpi-level',c)||{}).textContent||'';
        var okTier=tier==='all'||lvl.indexOf(tier)===0;
        var okQ=!ql||c.textContent.toLowerCase().indexOf(ql)>=0;
        var ok=okTier&&okQ;c.classList.toggle('dim',!ok);if(ok)shown++;
      });
      $$('.kpi-section',tree).forEach(function(s){var vis=$$('.kpi-card:not(.dim)',s).length;s.classList.toggle('dim',vis===0);var n=$('.kpi-section-count',s);});
      /* hide domain heads whose sections are all hidden */
      $$('.kpi-domain-head',tree).forEach(function(h){
        var n=h.nextElementSibling,any=false;
        while(n&&!n.classList.contains('kpi-domain-head')){if(n.classList.contains('kpi-section')&&!n.classList.contains('dim'))any=true;n=n.nextElementSibling;}
        h.style.display=any?'':'none';
      });
      var empty=$('.kpi-empty',tree);
      if(shown===0){if(!empty){empty=d.createElement('div');empty.className='kpi-empty';tree.appendChild(empty);}empty.innerHTML=L('No KPI matches “'+q+'”. Try another term or clear the filter.','Ningún KPI coincide con “'+q+'”. Prueba otro término o limpia el filtro.');}
      else if(empty){empty.parentNode.removeChild(empty);}
      if(count)count.innerHTML='<b>'+shown+'</b> / '+total+' KPIs';
      buildNav();
    }
    function buildNav(){
      if(!nav||!tree)return;
      var html='<div class="kn-h">'+L('Index','Índice')+'</div>';
      var items=Array.prototype.filter.call(tree.children,function(el){return (el.classList.contains('kpi-domain-head')&&el.style.display!=='none')||(el.classList.contains('kpi-section')&&!el.classList.contains('dim'));});
      if(!items.length){nav.innerHTML=html+'<div class="kn-empty">—</div>';return;}
      items.forEach(function(el){
        if(el.classList.contains('kpi-domain-head')){
          var t=el.lastElementChild?el.lastElementChild.textContent:el.textContent;
          html+='<a class="dom" href="#'+el.id+'">'+t+'</a>';
        }else{
          var tt=($('.kpi-section-title',el)||{}).textContent||'',n=$$('.kpi-card:not(.dim)',el).length;
          html+='<a href="#'+el.id+'">'+tt+'<span class="n">'+n+'</span></a>';
        }
      });
      nav.innerHTML=html;
    }
    /* active section on scroll */
    var ticking=false;
    function spy(){
      if(!nav||!tree)return;
      var links=$$('a',nav);if(!links.length)return;
      var top=(parseInt(getComputedStyle(d.documentElement).getPropertyValue('--lb-hd'))||52)+50+24;
      var cur=null;
      links.forEach(function(a){var el=d.getElementById(a.getAttribute('href').slice(1));if(el&&el.getBoundingClientRect().top<=top+8)cur=a;});
      links.forEach(function(a){a.classList.toggle('on',a===cur);});
    }
    window.addEventListener('scroll',function(){if(!ticking){ticking=true;requestAnimationFrame(function(){spy();ticking=false;});}},{passive:true});
    if(tree){
      new MutationObserver(function(){decorate();apply();}).observe(tree,{childList:true});
      decorate();apply();
    }
    if(search){search.addEventListener('input',function(){q=search.value;apply();});}
    filters.forEach(function(ch){ch.addEventListener('click',function(){filters.forEach(function(x){x.classList.remove('on');});ch.classList.add('on');tier=ch.getAttribute('data-tier')||'all';apply();});});
    /* keep the count + nav in the right language */
    new MutationObserver(function(){setTimeout(function(){decorate();apply();},50);}).observe(d.documentElement,{attributes:true,attributeFilter:['class']});
  }

  /* ---------- Labs index: category filter + search ---------- */
  if(isIndex){
    var fbtns=$$('.lx-filters button'),s=$('#lxSearch'),cards=$$('.lx-card'),secs=$$('.lx-sec'),emptyEl=$('#lxEmpty');
    var cat='all',qq='';
    function run(){
      var ql=qq.trim().toLowerCase(),n=0;
      cards.forEach(function(c){
        var okC=cat==='all'||(c.getAttribute('data-cat')||'').split(' ').indexOf(cat)>=0;
        var okQ=!ql||c.textContent.toLowerCase().indexOf(ql)>=0;
        var ok=okC&&okQ;c.classList.toggle('dim',!ok);if(ok)n++;
      });
      secs.forEach(function(sec){sec.classList.toggle('dim',$$('.lx-card:not(.dim)',sec).length===0);});
      if(emptyEl)emptyEl.style.display=n?'none':'';
    }
    fbtns.forEach(function(bt){bt.addEventListener('click',function(){fbtns.forEach(function(x){x.classList.remove('on');});bt.classList.add('on');cat=bt.getAttribute('data-cat')||'all';run();});});
    if(s){s.addEventListener('input',function(){qq=s.value;run();});}
    /* deep link: /labs/#cat=design */
    var m=location.hash.match(/cat=([a-z-]+)/);if(m){var bt=fbtns.filter(function(x){return x.getAttribute('data-cat')===m[1];})[0];if(bt)bt.click();}
  }
})();
