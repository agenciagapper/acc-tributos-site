(function(){
  var d=document, root=d.documentElement;
  root.classList.remove('no-js');

  // menu mobile
  var header=d.getElementById('header'), toggle=d.querySelector('.menu-toggle');
  toggle&&toggle.addEventListener('click',function(){
    var open=header.classList.toggle('open');
    root.classList.toggle('menu-open',open);
    toggle.setAttribute('aria-expanded',open);
    toggle.setAttribute('aria-label',open?'Fechar menu':'Abrir menu');
  });

  // mega menus
  var btns=d.querySelectorAll('.nav button[aria-controls]');
  function closeAll(except){btns.forEach(function(b){if(b!==except){b.setAttribute('aria-expanded','false');d.getElementById(b.getAttribute('aria-controls')).classList.remove('open');}});}
  btns.forEach(function(b){
    b.addEventListener('click',function(e){
      e.stopPropagation();
      var m=d.getElementById(b.getAttribute('aria-controls')), open=b.getAttribute('aria-expanded')!=='true';
      closeAll(b); b.setAttribute('aria-expanded',open); m.classList.toggle('open',open);
    });
  });
  d.addEventListener('click',function(e){if(!e.target.closest('.nav'))closeAll();});
  d.addEventListener('keydown',function(e){if(e.key==='Escape')closeAll();});

  // carrossel de depoimentos
  var track=d.getElementById('track');
  d.querySelectorAll('.arrows button').forEach(function(b){
    b.addEventListener('click',function(){
      var card=track.querySelector('.gcard,.quote');
      track.scrollBy({left:(card.offsetWidth+16)*+b.dataset.dir,behavior:'smooth'});
    });
  });

  // mapa sob demanda (não pesa no carregamento)
  var mapBtn=d.getElementById('loadMap');
  mapBtn&&mapBtn.addEventListener('click',function(){
    var f=d.createElement('iframe');
    f.title='Mapa do escritório da ACC Tributos no Business Place, Maracanaú';
    f.loading='lazy'; f.referrerPolicy='no-referrer-when-downgrade';
    f.src='https://www.google.com/maps?q=Av.+Yolanda+Pontes+Vidal+Queiroz,+57,+Maracana%C3%BA+-+CE,+61900-410&output=embed';
    mapBtn.replaceWith(f);
  });

  // UTMs e origem: capturados em forms.js (atribuição primeiro e último toque)

  // eventos (GA4 entra aqui quando estiver instalado)
  function track(name,data){window.dataLayer=window.dataLayer||[];window.dataLayer.push(Object.assign({event:name},data||{}));}
  d.addEventListener('click',function(e){
    var a=e.target.closest('[data-track]'); if(a)track(a.dataset.track+'_click',{link_url:a.href,page:location.pathname});
  });

  // formulários: ver o módulo "ACC forms" no fim deste arquivo

  var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // barra de leitura
  var bar=d.getElementById('progress');
  if(bar){var onScroll=function(){var h=root.scrollHeight-innerHeight;bar.style.setProperty('--p',h>0?(scrollY/h).toFixed(4):0);};addEventListener('scroll',onScroll,{passive:true});onScroll();}

  // palco do hero: parallax pelo mouse
  var stage=d.getElementById('stage');
  if(stage){
    stage.querySelectorAll('[data-depth]').forEach(function(el){el.style.setProperty('--d',el.dataset.depth);});
    if(!reduce&&matchMedia('(pointer:fine)').matches){
      var hero=stage.closest('.hero');
      hero.addEventListener('pointermove',function(e){
        var r=hero.getBoundingClientRect();
        stage.style.setProperty('--mx',((e.clientX-r.left)/r.width-.5).toFixed(3));
        stage.style.setProperty('--my',((e.clientY-r.top)/r.height-.5).toFixed(3));
      });
      hero.addEventListener('pointerleave',function(){stage.style.setProperty('--mx',0);stage.style.setProperty('--my',0);});
    }
  }

  // holofote nos cards escuros
  d.querySelectorAll('.ch').forEach(function(c){
    c.addEventListener('pointermove',function(e){var r=c.getBoundingClientRect();c.style.setProperty('--sx',(e.clientX-r.left)+'px');c.style.setProperty('--sy',(e.clientY-r.top)+'px');});
  });

  // títulos de seção palavra por palavra
  if(!reduce){
    d.querySelectorAll('.section__head h2, .reviews__top h2, .team h2, .faq h2').forEach(function(h){
      var i=0;
      h.innerHTML=h.textContent.trim().split(/\s+/).map(function(w){return '<span class="w"><span style="--i:'+(i++)+'">'+w+'</span></span>';}).join(' ');
      h.classList.add('split');
    });
  }

  // contadores
  function fmt(n){return n.toLocaleString('pt-BR');}
  function count(el){
    var end=+el.dataset.count,pre=el.dataset.prefix||'',suf=el.dataset.suffix||'',t0=null,dur=1400;
    function step(t){t0=t0||t;var p=Math.min((t-t0)/dur,1),e=1-Math.pow(1-p,3);el.textContent=pre+fmt(Math.round(end*e))+suf;if(p<1)requestAnimationFrame(step);}
    requestAnimationFrame(step);
    setTimeout(function(){el.textContent=pre+fmt(end)+suf;},dur+400);
  }
  var nums=d.querySelectorAll('[data-count]');
  if(!reduce&&'IntersectionObserver' in window){
    var cio=new IntersectionObserver(function(en){en.forEach(function(x){if(x.isIntersecting){count(x.target);cio.unobserve(x.target);}});},{threshold:.6});
    nums.forEach(function(n){cio.observe(n);});
  }

  // revelação ao rolar, com failsafe
  var els=d.querySelectorAll('.reveal');
  if(reduce||!('IntersectionObserver' in window)){els.forEach(function(el){el.classList.add('in');});return;}
  var io=new IntersectionObserver(function(en){en.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target);}});},{rootMargin:'0px 0px -8% 0px'});
  els.forEach(function(el){io.observe(el);});
  setTimeout(function(){els.forEach(function(el){el.classList.add('in');});},3500);
})();
