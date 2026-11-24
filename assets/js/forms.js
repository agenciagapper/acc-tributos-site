/* =========================================================
   ACC forms
   - todo link de WhatsApp abre uma janela pedindo nome e telefone,
     envia o contato e segue para /obrigado-whatsapp/, que abre o WhatsApp
   - formulário padrão (#leadForm) envia e vai para /obrigado/
   - Trabalhe conosco (#cvForm) envia com o currículo e vai para /trabalhe-conosco/obrigado/
   Destino dos dados: window.ACC_FORM_ENDPOINT (padrão /api/form.php)
   ========================================================= */
(function(){
  var d=document, ENDPOINT=window.ACC_FORM_ENDPOINT||'/api/form.php', WA_NUM='5585998250357';
  function track(name,data){window.dataLayer=window.dataLayer||[];window.dataLayer.push(Object.assign({event:name},data||{}));}
  /* ---------- atribuição: primeiro e último toque ----------
     Um "toque" é registrado quando a pessoa chega de fora do site (com UTM, ID de clique
     ou vinda de outro site). A navegação interna não muda nada.
     Primeiro toque: guardado por 90 dias. Último toque: o mais recente. */
  var UTM=['utm_source','utm_medium','utm_campaign','utm_term','utm_content','utm_id'];
  var IDS=['gclid','gbraid','wbraid','fbclid','msclkid','ttclid'];
  var DAY=864e5, TTL=90*DAY;
  function lsGet(k){try{return JSON.parse(localStorage.getItem(k)||'null');}catch(e){return null;}}
  function lsSet(k,v){try{localStorage.setItem(k,JSON.stringify(v));}catch(e){}}
  function classify(host,q){
    if(q.gclid||q.gbraid||q.wbraid)return ['google','cpc'];
    if(q.msclkid)return ['bing','cpc'];
    if(q.ttclid)return ['tiktok','cpc'];
    if(!host)return ['(direto)','(nenhum)'];
    var h=host.replace(/^www\.|^m\.|^l\.|^lm\./,'');
    var busca={'google.':'google','bing.com':'bing','yahoo.':'yahoo','duckduckgo.com':'duckduckgo','ecosia.org':'ecosia'};
    for(var k in busca)if(h.indexOf(k)>-1)return [busca[k],'organic'];
    var social={'facebook.com':'facebook','instagram.com':'instagram','linkedin.com':'linkedin','t.co':'x','twitter.com':'x','x.com':'x','youtube.com':'youtube','tiktok.com':'tiktok','whatsapp.com':'whatsapp','wa.me':'whatsapp'};
    for(var s in social)if(h===s||h.slice(-s.length-1)==='.'+s)return [social[s],q.fbclid?'social':'social'];
    return [h,'referral'];
  }
  (function capture(){
    var p=new URLSearchParams(location.search), q={}, any=false;
    UTM.concat(IDS).forEach(function(k){var v=p.get(k); if(v){q[k]=v.slice(0,200); any=true;}});
    var refHost=''; try{if(d.referrer){var r=new URL(d.referrer); if(r.host!==location.host)refHost=r.host;}}catch(e){}
    var now=Date.now(), first=lsGet('acc_first');
    if(first&&now-first.ts>TTL)first=null;
    if(!any&&!refHost&&first)return; // navegação interna ou retorno direto: mantém o que já existe
    var c=classify(refHost,q);
    var t={source:q.utm_source||c[0], medium:q.utm_medium||c[1], campaign:q.utm_campaign||'', term:q.utm_term||'', content:q.utm_content||'', utm_id:q.utm_id||'',
           landing:location.pathname, referrer:refHost?(d.referrer.split('?')[0]).slice(0,300):'', ts:now};
    if(!first)lsSet('acc_first',t);
    if(any||refHost||!lsGet('acc_last'))lsSet('acc_last',t);
    var ids=lsGet('acc_ids')||{}; IDS.forEach(function(k){if(q[k])ids[k]={v:q[k],ts:now};}); lsSet('acc_ids',ids);
  })();
  function cookie(n){var m=d.cookie.match(new RegExp('(?:^|; )'+n+'=([^;]*)'));return m?decodeURIComponent(m[1]):'';}
  function iso(ts){try{return new Date(ts).toISOString();}catch(e){return '';}}
  function attribution(){
    var f=lsGet('acc_first')||{}, l=lsGet('acc_last')||f, ids=lsGet('acc_ids')||{}, o={}, now=Date.now();
    o.utm_source=l.source||''; o.utm_medium=l.medium||''; o.utm_campaign=l.campaign||''; o.utm_term=l.term||''; o.utm_content=l.content||''; o.utm_id=l.utm_id||'';
    o.landing_page=l.landing||''; o.referrer=l.referrer||''; o.ultimo_toque_em=l.ts?iso(l.ts):'';
    o.primeiro_source=f.source||''; o.primeiro_medium=f.medium||''; o.primeiro_campaign=f.campaign||''; o.primeiro_term=f.term||''; o.primeiro_content=f.content||'';
    o.primeiro_landing=f.landing||''; o.primeiro_referrer=f.referrer||''; o.primeiro_toque_em=f.ts?iso(f.ts):'';
    IDS.forEach(function(k){o[k]=(ids[k]&&now-ids[k].ts<TTL)?ids[k].v:'';});
    // para integrações futuras: Meta (fbc/fbp) e GA4 (client id)
    o.fbp=cookie('_fbp'); o.fbc=cookie('_fbc')||(ids.fbclid&&now-ids.fbclid.ts<TTL?'fb.1.'+ids.fbclid.ts+'.'+ids.fbclid.v:'');
    var ga=cookie('_ga'); o.ga_client_id=ga?ga.split('.').slice(-2).join('.'):'';
    return o;
  }
  function origem(){var a=attribution();return [a.utm_source,a.utm_medium,a.utm_campaign].filter(Boolean).join(' / ');}
  function digits(v){return (v||'').replace(/\D/g,'');}
  function phoneOk(v){var n=digits(v);return n.length>=10&&n.length<=13;}
  function emailOk(v){return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test((v||'').trim());}
  function maskPhone(el){
    el.addEventListener('input',function(){
      var n=digits(el.value).slice(0,11),o=n;
      if(n.length>2)o='('+n.slice(0,2)+') '+n.slice(2);
      if(n.length>6)o='('+n.slice(0,2)+') '+n.slice(2,n.length-4)+'-'+n.slice(-4);
      el.value=o;
    });
  }
  function setErr(el,bad){el.setAttribute('aria-invalid',bad?'true':'false');return bad?0:1;}
  // envia sem prender o visitante por mais de 4 segundos
  function send(fd){
    fd.append('pagina',location.pathname); fd.append('origem',origem());
    var a=attribution(); for(var k in a)fd.append(k,a[k]);
    var ctrl=('AbortController' in window)?new AbortController():null;
    var t=setTimeout(function(){if(ctrl)ctrl.abort();},4000);
    return fetch(ENDPOINT,{method:'POST',body:fd,signal:ctrl?ctrl.signal:undefined})
      .then(function(r){clearTimeout(t);return r.ok;})
      .catch(function(){clearTimeout(t);return false;});
  }
  function saved(){try{return JSON.parse(sessionStorage.getItem('acc_contato')||'{}');}catch(e){return {};}}
  function save(o){try{sessionStorage.setItem('acc_contato',JSON.stringify(o));}catch(e){}}

  /* ---------- janela do WhatsApp ---------- */
  var dlg=d.createElement('dialog'); dlg.className='wa-modal'; dlg.setAttribute('aria-labelledby','wa-modal-t');
  dlg.innerHTML='<form class="wa-modal__box" novalidate>'+
    '<button type="button" class="wa-modal__x" aria-label="Fechar">&times;</button>'+
    '<p class="wa-modal__k"><svg width="18" height="18"><use href="#i-wa"/></svg>Atendimento pelo WhatsApp</p>'+
    '<h2 id="wa-modal-t">Antes de abrir a conversa</h2>'+
    '<p class="wa-modal__s">Assim o contador já sabe com quem está falando e retorna se a conversa cair.</p>'+
    '<div class="field"><label for="wm-nome">Seu nome</label><input id="wm-nome" name="nome" autocomplete="name" required><span class="err">Diga como podemos chamar você.</span></div>'+
    '<div class="field"><label for="wm-tel">Telefone com DDD</label><input id="wm-tel" name="telefone" type="tel" inputmode="tel" autocomplete="tel" placeholder="(85) 9 0000-0000" required><span class="err">Confira o número, com DDD.</span></div>'+
    '<input type="text" name="empresa_site" tabindex="-1" autocomplete="off" class="hp" aria-hidden="true">'+
    '<button class="btn" type="submit"><span class="wa-dot"><svg><use href="#i-wa"/></svg></span>Abrir o WhatsApp</button>'+
    '<small>Seus dados são usados só para este atendimento. <a href="/politica-de-privacidade/">Política de privacidade</a></small>'+
    '</form>';
  d.body.appendChild(dlg);
  var wf=dlg.querySelector('form'), pending=null;
  maskPhone(wf.telefone);
  dlg.querySelector('.wa-modal__x').addEventListener('click',function(){dlg.close();});
  dlg.addEventListener('click',function(e){if(e.target===dlg)dlg.close();});

  /* ---------- botão flutuante do WhatsApp (todas as páginas) ---------- */
  var WA_TXT='Olá! Vim pelo site e quero falar com um contador.';
  var fab=d.createElement('div'); fab.className='wa-fab';
  fab.innerHTML='<div class="wa-fab__tip" role="status" hidden>'+
      '<button type="button" class="wa-fab__close" aria-label="Fechar aviso">&times;</button>'+
      '<a href="https://wa.me/'+WA_NUM+'?text='+encodeURIComponent(WA_TXT)+'" data-track="whatsapp" data-wa data-titulo="Fale agora com a ACC">'+
        '<b>Fale agora com a ACC</b><span>Um contador responde no WhatsApp</span></a>'+
    '</div>'+
    '<a class="wa-fab__btn" href="https://wa.me/'+WA_NUM+'?text='+encodeURIComponent(WA_TXT)+'" data-track="whatsapp" data-wa data-titulo="Fale agora com a ACC" aria-label="Fale agora com a ACC pelo WhatsApp">'+
      '<svg width="30" height="30" aria-hidden="true"><use href="#i-wa"/></svg></a>';
  d.body.appendChild(fab);
  var tip=fab.querySelector('.wa-fab__tip');
  function tipOff(){tip.hidden=true; try{sessionStorage.setItem('acc_fab_tip','0');}catch(e){}}
  fab.querySelector('.wa-fab__close').addEventListener('click',tipOff);
  var tipSeen=''; try{tipSeen=sessionStorage.getItem('acc_fab_tip')||'';}catch(e){}
  if(tipSeen!=='0')setTimeout(function(){tip.hidden=false;},tipSeen?400:3500);
  try{sessionStorage.setItem('acc_fab_tip',tipSeen||'1');}catch(e){}

  var dlgT=dlg.querySelector('#wa-modal-t'), dlgTDefault=dlgT.textContent;

  function msgFrom(href){try{return new URL(href).searchParams.get('text')||'';}catch(e){return '';}}

  d.addEventListener('click',function(e){
    var a=e.target.closest('a[href*="wa.me/"]'); if(!a||a.hasAttribute('data-direto'))return;
    if(!dlg.showModal)return; // navegador sem suporte a dialog: segue direto
    e.preventDefault(); e.stopPropagation();
    pending={msg:msgFrom(a.href)||'Olá! Vim pelo site e quero falar com um contador.'};
    dlgT.textContent=a.dataset.titulo||dlgTDefault;
    if(a.closest('.wa-fab'))tipOff();
    var s=saved(); if(s.nome)wf.nome.value=s.nome; if(s.telefone)wf.telefone.value=s.telefone;
    wf.querySelectorAll('[aria-invalid]').forEach(function(x){x.removeAttribute('aria-invalid');});
    wf.querySelector('button[type=submit]').disabled=false;
    dlg.showModal(); (s.nome?wf.telefone:wf.nome).focus();
    track('whatsapp_modal_open',{page:location.pathname});
  },true);

  wf.addEventListener('submit',function(e){
    e.preventDefault();
    var ok=setErr(wf.nome,!wf.nome.value.trim()) & setErr(wf.telefone,!phoneOk(wf.telefone.value));
    if(!ok){wf.querySelector('[aria-invalid="true"]').focus();return;}
    wf.querySelector('button[type=submit]').disabled=true;
    var nome=wf.nome.value.trim(), tel=wf.telefone.value.trim();
    save({nome:nome,telefone:tel});
    try{sessionStorage.setItem('acc_wa_msg',(pending&&pending.msg)||'');}catch(err){}
    var fd=new FormData(wf); fd.append('tipo','whatsapp'); fd.append('mensagem',(pending&&pending.msg)||'');
    track('generate_lead',{canal:'whatsapp',page:location.pathname,origem:origem()});
    send(fd).then(function(){location.href='/obrigado-whatsapp/';});
  });

  /* ---------- formulário padrão ---------- */
  var lf=d.getElementById('leadForm');
  if(lf){
    if(lf.whatsapp)maskPhone(lf.whatsapp);
    lf.addEventListener('submit',function(e){
      e.preventDefault();
      var ok=setErr(lf.nome,!lf.nome.value.trim()) & setErr(lf.whatsapp,!phoneOk(lf.whatsapp.value)) & (lf.email?setErr(lf.email,!emailOk(lf.email.value)):1);
      if(!ok){lf.querySelector('[aria-invalid="true"]').focus();return;}
      lf.querySelector('button[type=submit]').disabled=true;
      save({nome:lf.nome.value.trim(),telefone:lf.whatsapp.value.trim()});
      var fd=new FormData(lf); fd.append('tipo','formulario');
      track('generate_lead',{canal:'formulario',assunto:lf.assunto?lf.assunto.value:'',origem:origem()});
      send(fd).then(function(){location.href='/obrigado/';});
    });
  }

  /* ---------- trabalhe conosco ---------- */
  var cf=d.getElementById('cvForm');
  if(cf){
    maskPhone(cf.telefone);
    var file=cf.curriculo, MAX=5*1024*1024, ext=/\.(pdf|doc|docx)$/i;
    file.addEventListener('change',function(){
      var f=file.files[0], out=d.getElementById('cv-nome');
      if(out)out.textContent=f?f.name+' · '+Math.ceil(f.size/1024)+' KB':'Nenhum arquivo escolhido';
      if(f)setErr(file,!ext.test(f.name)||f.size>MAX);
    });
    cf.addEventListener('submit',function(e){
      e.preventDefault();
      var f=file.files[0];
      var ok=setErr(cf.nome,!cf.nome.value.trim()) & setErr(cf.email,!emailOk(cf.email.value)) & setErr(cf.telefone,!phoneOk(cf.telefone.value))
        & setErr(cf.especialidade,!cf.especialidade.value) & setErr(cf.formacao,!cf.formacao.value)
        & setErr(file,!f||!ext.test(f.name)||f.size>MAX) & setErr(cf.lgpd,!cf.lgpd.checked);
      if(!ok){cf.querySelector('[aria-invalid="true"]').focus();return;}
      var btn=cf.querySelector('button[type=submit]'); btn.disabled=true; btn.querySelector('.lbl').textContent='Enviando…';
      var fd=new FormData(cf); fd.append('tipo','curriculo');
      track('curriculo_enviado',{especialidade:cf.especialidade.value});
      send(fd).then(function(){location.href='/trabalhe-conosco/obrigado/';});
    });
  }

  /* ---------- página /obrigado-whatsapp/ ---------- */
  var go=d.getElementById('waGo');
  if(go){
    var s=saved(), msg=''; try{msg=sessionStorage.getItem('acc_wa_msg')||'';}catch(e){}
    var corpo=msg.replace(/^Olá!\s*/,'')||'Vim pelo site e quero falar com um contador.';
    var text=(s.nome?'Olá! Sou '+s.nome+'. ':'Olá! ')+corpo;
    var url='https://wa.me/'+WA_NUM+'?text='+encodeURIComponent(text);
    go.href=url;
    var nm=d.getElementById('waNome'); if(nm&&s.nome)nm.textContent=', '+s.nome.split(' ')[0];
    var c=d.getElementById('waCount'), n=3;
    var iv=setInterval(function(){n--; if(c)c.textContent=String(Math.max(n,0)); if(n<=0){clearInterval(iv); location.href=url;}},1000);
  }
  var nm2=d.getElementById('obNome'); if(nm2){var s2=saved(); if(s2.nome)nm2.textContent=', '+s2.nome.split(' ')[0];}
})();
