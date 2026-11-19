"""Página Quem somos (layout próprio). Usada por build.py."""
import html

e = lambda s: html.escape(str(s), quote=True)

MISSAO = "Fornecer soluções contábeis com excelência, garantindo a tranquilidade de nossos clientes e parceiros."
VISAO = "Ser uma das melhores empresas de contabilidade e gestão da atualidade."
VALORES = ["Compromisso", "Responsabilidade", "Relacionamento", "Ambiente positivo", "Ética", "Transparência"]

SOCIOS = [
    {"nome": "Joel Mendonça", "crc": "CRC/CE 25911", "foto": "/assets/img/joel-mendonca.webp", "w": 1100, "h": 1356,
     "papel": "Sócio e contador",
     "bio": "MBA em Direito Tributário e 12 anos como assessor e consultor de empresas. Também é professor de gestão financeira e empresarial, e leva essa visão de gestão para a rotina dos clientes."},
    {"nome": "Alyson Xavier", "crc": "CRC/CE 27954", "foto": "/assets/img/alyson-xavier.webp", "w": 1100, "h": 1247,
     "papel": "Sócio e contador",
     "bio": "Contador e sócio da ACC Tributos. Acompanha de perto a equipe e as empresas atendidas, para que cada cliente tenha resposta de quem conhece o caso."},
]

AREAS = [
    ("Contábil", "Raul Medeiros", "Registros, balanço e demonstrativos."),
    ("Fiscal", "Jardel Freitas", "Notas, apurações e SPED no prazo."),
    ("Departamento pessoal", "Rerison Xavier", "Folha, admissões, férias e eSocial."),
    ("Societário e processos", "Joyce Lopes", "Abertura, alterações e baixa de empresas."),
    ("Tributário", None, "Regime tributário e planejamento."),
    ("Financeiro", None, "Contas a pagar e receber, conciliação."),
]

GRUPO = [
    {"nome": "ACC Tributos", "faz": "Contabilidade, impostos, departamento pessoal e abertura de empresas.", "logo": "/assets/logos/simbolo-azul.webp", "aqui": True, "url": "/servicos/"},
    {"nome": "ACC Gestão", "faz": "Gestão financeira: contas a pagar e a receber e conciliação bancária.", "logo": "/assets/logos/grupo-acc-azul.webp", "url": None},
    {"nome": "Prime Certificação", "faz": "Certificado digital e-CNPJ e e-CPF.", "logo": "/assets/logos/prime.webp", "url": "/servicos/certificado-digital/"},
    {"nome": "Regularize Marcas", "faz": "Pesquisa e registro de marca no INPI.", "logo": "/assets/logos/regularize.webp", "url": "/servicos/registro-de-marca/"},
]

REVIEWS = [
    ("Jackson Soler Alves dos Santos", "5 avaliações · um mês atrás", "Ótimo atendimento e bons profissionais.", "#1E8E3E"),
    ("vitoria", "3 avaliações · um ano atrás", "A equipe da ACC Tributos Contabilidade é excelente! Sempre muito atenciosos, ágeis e profissionais.", "#A142F4"),
    ("Bluesena SK", "Local Guide · um ano atrás", "Super indico, uma equipe incrível. Hoje toda minha empresa está na mão deles.", "#E8710A"),
]
GMAPS = "https://www.google.com/maps/place/ACC+TRIBUTOS+CONTABILIDADE/data=!4m2!3m1!1s0x0:0xbfcc2a5d8438b3f3"


def render(p, crumb_html, wa, faq_block, final_block):
    socios = "".join(f"""
      <article class="qs-socio reveal">
        <figure class="qs-socio__foto"><img src="{s['foto']}" width="{s['w']}" height="{s['h']}" alt="{e(s['nome'])}, {e(s['papel'].lower())} da ACC Tributos" loading="lazy"></figure>
        <div class="qs-socio__txt">
          <p class="qs-mono">{e(s['crc'])}</p>
          <h3>{e(s['nome'])}</h3>
          <p class="qs-socio__papel">{e(s['papel'])}</p>
          <p>{e(s['bio'])}</p>
        </div>
      </article>""" for s in SOCIOS)

    areas = "".join(f"""<li><span class="qs-area__n">{e(a)}</span>{f'<span class="qs-area__lider">{e(l)}</span>' if l else ''}<span class="qs-area__d">{e(d)}</span></li>""" for a, l, d in AREAS)

    grupo = "".join(f"""
        <{'a href="' + g['url'] + '"' if g['url'] else 'div'} class="qs-emp{' qs-emp--aqui' if g.get('aqui') else ''}">
          <img src="{g['logo']}" alt="" width="48" height="48" loading="lazy">
          <span><b>{e(g['nome'])}</b>{e(g['faz'])}</span>
          {'<em>Você está aqui</em>' if g.get('aqui') else ''}
        </{'a' if g['url'] else 'div'}>""" for g in GRUPO)

    stars = '<span class="stars" aria-label="5 de 5 estrelas"><i></i><i></i><i></i><i></i><i></i></span>'
    reviews = "".join(f"""
        <article class="gcard"><header><span class="gav" style="--c:{c}">{n[0].upper()}</span><div><strong>{e(n)}</strong><span>{e(m)}</span></div><svg class="gmark" viewBox="0 0 48 48" aria-hidden="true"><use href="#i-google"/></svg></header><div class="gmeta">{stars}</div><p>{e(t)}</p></article>""" for n, m, t, c in REVIEWS)

    return f"""<main id="conteudo">
<div class="wrap">{crumb_html}</div>

<section class="qs-hero">
  <div class="wrap">
    <p class="entry">Quem somos</p>
    <h1>Somos a ACC Tributos: a contabilidade que atende você <span>pelo nome</span>.</h1>
    <div class="qs-hero__row">
      <p class="qs-hero__lead">Há 6 anos cuidamos da contabilidade de empresas e pessoas em Fortaleza e na Região Metropolitana. São mais de 30 pessoas, dois sócios contadores e um jeito simples de trabalhar: você sabe quem cuida da sua empresa e fala com essa pessoa pelo WhatsApp.</p>
      <div class="qs-hero__ctas">
        <a class="btn" href="{e(wa)}" data-track="whatsapp" data-wa><span class="wa-dot"><svg><use href="#i-wa"/></svg></span>Falar com a equipe</a>
        <a class="link" href="/contato/">Como chegar ao escritório <svg width="18" height="18"><use href="#i-arrow"/></svg></a>
      </div>
    </div>
  </div>
  <div class="qs-film" aria-label="Fotos do escritório da ACC Tributos">
    <figure class="qs-film__a"><img src="/assets/img/escritorio-equipe.webp" width="1280" height="500" alt="Equipe da ACC Tributos reunida no hall do escritório" fetchpriority="high"><figcaption class="qs-mono">A equipe</figcaption></figure>
    <figure class="qs-film__b"><img src="/assets/img/escritorio-mesas.webp" width="1280" height="500" alt="Contadores da ACC Tributos trabalhando nas estações do escritório" loading="lazy"><figcaption class="qs-mono">O dia a dia</figcaption></figure>
    <figure class="qs-film__c"><img src="/assets/img/escritorio-atendimento.webp" width="1280" height="500" alt="Colaboradores da ACC Tributos atendendo clientes no escritório" loading="lazy"><figcaption class="qs-mono">O atendimento</figcaption></figure>
  </div>
  <div class="wrap">
    <dl class="qs-nums">
      <div><dt>Empresas abertas</dt><dd data-count="1200" data-prefix="+">+1.200</dd></div>
      <div><dt>Clientes atendidos</dt><dd data-count="1000" data-prefix="+">+1.000</dd></div>
      <div><dt>Colaboradores</dt><dd data-count="30" data-prefix="+">+30</dd></div>
      <div><dt>Nota no Google</dt><dd>4,8 <small>199 avaliações</small></dd></div>
    </dl>
  </div>
</section>

<section class="section qs-crencas" aria-labelledby="t-crencas">
  <div class="wrap qs-crencas__grid">
    <div class="reveal">
      <p class="entry">Missão</p>
      <h2 id="t-crencas" class="qs-missao">{e(MISSAO)}</h2>
    </div>
    <div class="qs-crencas__side reveal">
      <div><p class="entry">Visão</p><p class="qs-visao">{e(VISAO)}</p></div>
      <div><p class="entry">Valores</p><ul class="qs-valores">{''.join(f'<li>{e(v)}</li>' for v in VALORES)}</ul></div>
    </div>
  </div>
</section>

<section class="section qs-socios" aria-labelledby="t-socios">
  <div class="wrap">
    <div class="section__head reveal"><div><p class="entry">Os sócios</p><h2 id="t-socios">Dois contadores com CRC respondendo pelo trabalho.</h2></div><p>Toda empresa atendida tem responsabilidade técnica assinada por um contador registrado no Conselho Regional de Contabilidade do Ceará.</p></div>
    <div class="qs-socios__grid">{socios}
    </div>
  </div>
</section>

<section class="section qs-equipe" aria-labelledby="t-equipe">
  <div class="wrap qs-equipe__grid">
    <div class="reveal">
      <p class="entry">A equipe</p>
      <h2 id="t-equipe">Cada parte da sua empresa tem um time que entende dela.</h2>
      <p>Nossa equipe é formada por profissionais com experiência em áreas específicas e uma rotina forte de estudo, para acompanhar as mudanças na legislação antes que elas virem problema para o cliente.</p>
    </div>
    <ul class="qs-areas reveal">{areas}</ul>
  </div>
</section>

<section class="section qs-grupo" aria-labelledby="t-grupo">
  <div class="wrap">
    <div class="section__head reveal"><div><p class="entry">Grupo ACC</p><h2 id="t-grupo">Uma casa, quatro empresas.</h2></div><p>A ACC Tributos faz parte do Grupo ACC. Quando sua empresa precisa de algo além da contabilidade, o serviço já está aqui dentro, com o mesmo atendimento.</p></div>
    <div class="qs-grupo__map reveal">
      <img class="qs-grupo__hex" src="/assets/img/simbolo-3d.webp" width="600" height="703" alt="" aria-hidden="true" loading="lazy">
      {grupo}
    </div>
  </div>
</section>

<section class="section qs-reviews" aria-labelledby="t-qsrev">
  <div class="wrap">
    <div class="reviews__top reveal"><div><p class="entry">Avaliações no Google</p><h2 id="t-qsrev">4,8 de nota, em 199 avaliações.</h2></div><a class="link" href="{GMAPS}" target="_blank" rel="noopener">Ver todas no Google <svg width="18" height="18"><use href="#i-arrow"/></svg></a></div>
    <div class="qs-reviews__grid reveal">{reviews}
    </div>
  </div>
</section>
{faq_block}
{final_block}
</main>"""
