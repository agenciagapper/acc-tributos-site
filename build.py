"""Gera as páginas internas do site ACC Tributos.

Fonte da verdade do topo, rodapé e bloco de contato: index.html.
Conteúdo de cada página: content/*.json (formato em content/_brief.md).
Uso: python build.py
"""
import glob
import sys
import html
import json
import os
import re
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
SITE = "https://acctributos.com.br"
WA = "5585987541948"
TODAY = date.today().isoformat()
GMAPS = "https://www.google.com/maps/place/ACC+TRIBUTOS+CONTABILIDADE/data=!4m2!3m1!1s0x0:0xbfcc2a5d8438b3f3"

src = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()


def between(a, b, include_a=True):
    i = src.index(a)
    j = src.index(b, i)
    return src[i if include_a else i + len(a):j]


TOP = between("<body>", '<main id="conteudo">', include_a=False)
BOTTOM = src[src.index("</main>") + len("</main>"):src.index("</body>")]
FINAL = between("<!-- CTA FINAL -->", "</main>")
CSS_V = re.search(r"site\.css\?v=(\d+)", src).group(1)
ORG_ID = SITE + "/#empresa"
TAGS = between("<!-- TAGS", "<!-- /TAGS -->") + "<!-- /TAGS -->\n"

e = lambda s: html.escape(str(s), quote=True)


def wa_link(text):
    from urllib.parse import quote
    return f"https://wa.me/{WA}?text={quote(text)}"


def head(p, schema):
    url = SITE + p["slug"]
    robots = '<meta name="robots" content="noindex, follow">\n' if p.get("noindex") else ""
    return f"""<!doctype html>
<html lang="pt-BR" class="no-js" data-tema="claro">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(p['title'])}</title>
<meta name="description" content="{e(p['description'])}">
{robots}<link rel="canonical" href="{url}">
<meta name="theme-color" content="#1326E8">
<meta property="og:type" content="website">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="ACC Tributos">
<meta property="og:title" content="{e(p['title'])}">
<meta property="og:description" content="{e(p['description'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/og/home.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{SITE}/assets/og/home.jpg">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon-32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:wght@500;600;700;800&family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/site.css?v={CSS_V}">
<script type="application/ld+json">
{json.dumps(schema, ensure_ascii=False, indent=1)}
</script>
{TAGS}</head>
<body>"""


def crumbs(p):
    items = [("Início", "/")]
    if p["type"] == "servico":
        items.append(("Serviços", "/servicos/"))
    elif p["type"] == "post":
        items.append(("Blog", "/blog/"))
    items.append((p["nav"], None))
    lis = "".join(
        f'<li><a href="{u}">{e(n)}</a></li>' if u else f'<li aria-current="page">{e(n)}</li>' for n, u in items
    )
    ld = {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + (u or p["slug"])} for i, (n, u) in enumerate(items)]}
    return f'<nav class="crumbs" aria-label="Você está em"><ol>{lis}</ol></nav>', ld


def faq_title(p):
    if p["type"] == "servico":
        return "Dúvidas sobre " + p["nav"][0].lower() + p["nav"][1:] if not p["nav"].startswith(("Imposto", "Certificado", "Registro")) else "Dúvidas sobre " + p["nav"]
    if p["type"] == "regiao":
        return "Dúvidas sobre contabilidade " + ("no " if p["city"] == "Eusébio" else "em ") + p["city"]
    return "Dúvidas frequentes"


def faq_html(faq):
    out = []
    for i, f in enumerate(faq):
        op = " open" if i == 0 else ""
        out.append(f'<details{op}><summary>{e(f["q"])}<i></i></summary><div class="ans"><p>{e(f["a"])}</p></div></details>')
    return "\n        ".join(out)


def section_html(s):
    paras = "".join(f"<p>{e(x)}</p>" for x in s.get("paragraphs", []))
    bullets = ""
    if s.get("bullets"):
        bullets = '<ul class="ticks">' + "".join(f'<li><svg><use href="#i-check"/></svg><span>{e(b)}</span></li>' for b in s["bullets"]) + "</ul>"
    return f'<section class="prose__block reveal"><h2>{e(s["h2"])}</h2>{paras}{bullets}</section>'


ICONS = ["/assets/img/passo-conversa.webp", "/assets/img/passo-proposta.webp", "/assets/img/passo-assume.webp"]


def steps_html(steps):
    lis = "".join(
        f'<li class="step"><span class="k" aria-hidden="true">{i + 1:02d}</span><div class="step__card">'
        f'<figure class="step__icon"><img src="{ICONS[i % 3]}" width="120" height="110" alt="" loading="lazy"></figure>'
        f'<h3><span class="sr">Passo {i + 1}: </span>{e(s["title"])}</h3><p>{e(s["text"])}</p></div></li>'
        for i, s in enumerate(steps[:3]))
    return f"""<section class="section page-steps" aria-labelledby="t-steps">
  <div class="wrap">
    <div class="section__head reveal"><div><p class="entry">Como funciona</p><h2 id="t-steps">Do primeiro contato até a gente assumir.</h2></div><p>Sem burocracia para você. Cada etapa tem um responsável com nome.</p></div>
    <ol class="steps reveal" style="list-style:none;margin:0;padding:0">{lis}</ol>
  </div>
</section>"""


def related_html(urls, pages):
    cards = []
    for u in urls:
        r = pages.get(u)
        if not r:
            continue
        cards.append(f'<a class="rel" href="{u}"><span class="km">{e(r["kicker"])}</span><h3>{e(r["nav"])}</h3><p>{e(r["description"])}</p><span class="link">Ver página <svg width="18" height="18"><use href="#i-arrow"/></svg></span></a>')
    if not cards:
        return ""
    return f"""<section class="section related" aria-labelledby="t-rel">
  <div class="wrap">
    <p class="entry">Veja também</p>
    <h2 id="t-rel" class="related__h">Serviços que costumam andar juntos</h2>
    <div class="related__grid">{''.join(cards)}</div>
  </div>
</section>"""


def page(p, pages):
    url = SITE + p["slug"]
    crumb_html, crumb_ld = crumbs(p)
    graph = [crumb_ld, {"@type": "WebPage", "@id": url + "#pagina", "url": url, "name": p["title"], "description": p["description"],
                        "inLanguage": "pt-BR", "isPartOf": {"@id": SITE + "/#site"}, "about": {"@id": ORG_ID}, "dateModified": TODAY}]
    if p["type"] in ("servico", "regiao"):
        svc = {"@type": "Service", "name": p["h1"] if p["type"] == "regiao" else p["nav"], "serviceType": p["nav"], "url": url,
               "provider": {"@type": "AccountingService", "@id": ORG_ID, "name": "ACC Tributos", "telephone": "+55-85-98754-1948",
                            "address": {"@type": "PostalAddress", "streetAddress": "Av. Yolanda Pontes Vidal Queiroz, 57, Edifício Business Place, Torre I, Sala 1103",
                                        "addressLocality": "Maracanaú", "addressRegion": "CE", "postalCode": "61900-410", "addressCountry": "BR"}},
               "areaServed": [{"@type": "City", "name": p["city"]}] if p["type"] == "regiao" else
               [{"@type": "City", "name": c} for c in ("Fortaleza", "Maracanaú", "Eusébio", "Aquiraz")]}
        graph.append(svc)
    if p.get("faq"):
        graph.append({"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in p["faq"]]})
    schema = {"@context": "https://schema.org", "@graph": graph}

    wa = wa_link(p.get("wa_text") or "Olá! Vim pelo site e quero falar com um contador.")
    hl = "".join(f'<li><svg><use href="#i-check"/></svg>{e(h)}</li>' for h in p.get("highlights", []))
    second = ('<a class="btn btn--ghost" href="/#servicos">Ver todos os serviços</a>' if p["type"] == "servico"
              else '<a class="btn btn--ghost" href="/#servicos">Ver os serviços</a>')

    local = ""
    if p["type"] == "regiao":
        chips = "".join(f"<li>{e(a)}</li>" for a in p.get("areas", []))
        notes = "".join(f'<li><svg><use href="#i-pin"/></svg><span>{e(n)}</span></li>' for n in p.get("local_notes", []))
        local = f"""<section class="prose__block reveal local">
          <h2>Onde atendemos em {e(p['city'])}</h2>
          <ul class="areas-chips">{chips}</ul>
          <ul class="ticks ticks--pin">{notes}</ul>
        </section>"""

    body_sections = "\n        ".join(section_html(s) for s in p["sections"])
    steps = steps_html(p["steps"]) if p.get("steps") else ""

    main = f"""<main id="conteudo">
<div class="wrap">{crumb_html}</div>
<section class="phero">
  <div class="wrap phero__grid">
    <div>
      <a class="hero__kicker" href="/#avaliacoes"><svg viewBox="0 0 48 48" aria-hidden="true"><use href="#i-google"/></svg><b>4,8</b><span class="stars" aria-hidden="true"><i></i><i></i><i></i><i></i><i class="half"></i></span><span>199 avaliações no Google</span></a>
      <p class="entry">{e(p['kicker'])}</p>
      <h1>{e(p['h1'])}</h1>
      <p class="phero__lead">{e(p['lead'])}</p>
      <ul class="phero__hl">{hl}</ul>
      <div class="hero__ctas">
        <a class="btn" href="{e(wa)}" data-track="whatsapp" data-wa><span class="wa-dot"><svg><use href="#i-wa"/></svg></span>Falar com um contador</a>
        {second}
      </div>
    </div>
    <aside class="phero__card" aria-label="Sócios da ACC Tributos">
      <div class="phero__photo"><img src="/assets/img/socios-dupla.webp" width="921" height="927" alt="Alyson Xavier e Joel Mendonça, sócios da ACC Tributos" fetchpriority="high"></div>
      <div class="phero__people"><span><b>Joel Mendonça</b>CRC/CE 25911</span><span><b>Alyson Xavier</b>CRC/CE 27954</span></div>
      <p class="phero__note">+1.200 empresas abertas e +30 colaboradores. Atendimento presencial ou 100% online, de segunda a sexta, 8h às 18h.</p>
    </aside>
  </div>
</section>

<section class="section prose-wrap">
  <div class="wrap prose">
    <article class="prose__main">
        {body_sections}
        {local}
    </article>
    <aside class="prose__side">
      <div class="side-card">
        <p class="side-card__t">Fale com um contador</p>
        <p>Resposta no mesmo dia útil, sem compromisso.</p>
        <a class="btn" href="{e(wa)}" data-track="whatsapp" data-wa><span class="wa-dot"><svg><use href="#i-wa"/></svg></span>WhatsApp</a>
        <hr>
        <p class="side-card__s">Edifício Business Place, Torre I, Sala 1103<br>Av. Yolanda Pontes Vidal Queiroz, 57<br>Jereissati I, Maracanaú, CE</p>
        <p class="side-card__s">Segunda a sexta, 8h às 18h</p>
      </div>
    </aside>
  </div>
</section>
{steps}
<section class="section" style="background:var(--paper-2)" aria-labelledby="t-faq">
  <div class="wrap faq">
    <aside class="reveal">
      <p class="entry">Perguntas frequentes</p>
      <h2 id="t-faq">{e(faq_title(p))}</h2>
      <p>Não achou sua dúvida? Um contador responde no WhatsApp, normalmente no mesmo dia.</p>
      <a class="btn" href="{e(wa)}" data-track="whatsapp" data-wa><span class="wa-dot"><svg><use href="#i-wa"/></svg></span>Tirar minha dúvida</a>
    </aside>
    <div class="qa reveal">
        {faq_html(p.get('faq', []))}
    </div>
  </div>
</section>
{related_html(p.get('related', []), pages)}
{FINAL}
</main>"""
    return head(p, schema) + TOP + main + BOTTOM + "</body>\n</html>\n"


def qs_page(p):
    import quem_somos
    url = SITE + p["slug"]
    crumb_html, crumb_ld = crumbs(p)
    graph = [crumb_ld, {"@type": "AboutPage", "@id": url + "#pagina", "url": url, "name": p["title"], "description": p["description"],
                        "inLanguage": "pt-BR", "isPartOf": {"@id": SITE + "/#site"}, "about": {"@id": ORG_ID}, "dateModified": TODAY},
             {"@type": "Organization", "@id": ORG_ID, "name": "ACC Tributos Assessoria e Consultoria Contábil",
              "employee": [{"@type": "Person", "name": "Joel Mendonça", "jobTitle": "Sócio e contador", "identifier": "CRC/CE 25911"},
                           {"@type": "Person", "name": "Alyson Xavier", "jobTitle": "Sócio e contador", "identifier": "CRC/CE 27954"}],
              "parentOrganization": {"@type": "Organization", "name": "Grupo ACC"}}]
    if p.get("faq"):
        graph.append({"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in p["faq"]]})
    wa = wa_link(p.get("wa_text") or "Olá! Vim pela página Quem somos e quero falar com a equipe.")
    faq_block = f"""<section class="section" style="background:var(--paper-2)" aria-labelledby="t-faq">
  <div class="wrap faq">
    <aside class="reveal"><p class="entry">Perguntas frequentes</p><h2 id="t-faq">Dúvidas sobre a ACC Tributos</h2><p>Não achou sua dúvida? A equipe responde no WhatsApp, normalmente no mesmo dia.</p></aside>
    <div class="qa reveal">
        {faq_html(p.get('faq', []))}
    </div>
  </div>
</section>"""
    main = quem_somos.render(p, crumb_html, wa, faq_block, FINAL)
    return head(p, {"@context": "https://schema.org", "@graph": graph}) + TOP + main + BOTTOM + "</body>\n</html>\n"


def write(slug, html_text):
    out = os.path.join(ROOT, slug.strip("/").replace("/", os.sep), "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(html_text)
    return out


def simple_page(p, inner, schema_extra=None):
    crumb_html, crumb_ld = crumbs(p)
    graph = [crumb_ld, {"@type": "WebPage", "url": SITE + p["slug"], "name": p["title"], "inLanguage": "pt-BR", "isPartOf": {"@id": SITE + "/#site"}}]
    graph += schema_extra or []
    main = f"""<main id="conteudo">
<div class="wrap">{crumb_html}</div>
<section class="phero phero--simple"><div class="wrap"><p class="entry">{e(p['kicker'])}</p><h1>{e(p['h1'])}</h1><p class="phero__lead">{e(p['lead'])}</p></div></section>
{inner}
{FINAL if not p.get('no_final') else ''}
</main>"""
    return head(p, {"@context": "https://schema.org", "@graph": graph}) + TOP + main + BOTTOM + "</body>\n</html>\n"


OLD_POSTS = [
    ("quem-precisa-declarar-imposto-de-renda", "Quem precisa declarar Imposto de Renda"),
    ("qual-o-melhor-regime-tributario-para-sua-empresa", "Qual o melhor regime tributário para sua empresa"),
    ("notificacao-simples-nacional", "Notificação do Simples Nacional: o que fazer"),
    ("principais-tipos-de-contratos-de-trabalho", "Principais tipos de contratos de trabalho"),
    ("capital-social-do-mei", "Capital social do MEI"),
    ("nao-posso-ser-mei-o-que-vem-depois", "Não posso ser MEI: o que vem depois"),
    ("mei-transportador-autonomo-de-cargas", "MEI transportador autônomo de cargas"),
    ("cabeleireiro-pode-ser-mei", "Cabeleireiro pode ser MEI?"),
    ("o-que-e-gestao-financeira", "O que é gestão financeira"),
    ("refissaude", "Refis da Saúde"),
    ("empresasdesucesso", "Empresas de sucesso"),
]


def build():
    pages = {}
    for f in sorted(glob.glob(os.path.join(ROOT, "content", "*.json"))):
        p = json.load(open(f, encoding="utf-8"))
        pages[p["slug"]] = p
    made = []
    for p in pages.values():
        made.append(write(p["slug"], qs_page(p) if p["slug"] == "/quem-somos/" else page(p, pages)))

    # índice de serviços
    svc = [p for p in pages.values() if p["type"] == "servico"]
    order = ["legalizacao-de-empresas", "contabilidade-empresarial", "planejamento-tributario", "departamento-pessoal", "imposto-de-renda",
             "escrituracao-fiscal", "auditoria-fiscal-digital", "calculos", "certificado-digital", "registro-de-marca"]
    svc.sort(key=lambda p: next((i for i, o in enumerate(order) if o in p["slug"]), 99))
    rows = "".join(f'<a href="{p["slug"]}"><span class="n">{i + 1:02d}</span><h3>{e(p["nav"])}</h3><p>{e(p["description"])}</p><span class="go"><svg><use href="#i-arrow"/></svg></span></a>' for i, p in enumerate(svc))
    sp = {"slug": "/servicos/", "type": "institucional", "nav": "Serviços", "kicker": "Serviços contábeis",
          "title": "Serviços de Contabilidade em Fortaleza | ACC Tributos",
          "description": "Abertura de empresa, contabilidade, planejamento tributário, departamento pessoal, Imposto de Renda e mais. Atendimento em Fortaleza e região.",
          "h1": "Serviços de contabilidade em Fortaleza e região",
          "lead": "Tudo o que sua empresa precisa num escritório só, com um contador dedicado e resposta pelo WhatsApp. Escolha o serviço para ver como funciona."}
    made.append(write(sp["slug"], simple_page(sp, f'<section class="section" style="padding-top:var(--s-3)"><div class="wrap"><nav class="ledger" aria-label="Serviços">{rows}</nav></div></section>')))

    # artigos do blog (antigos migrados do WordPress na raiz; novos em /blog/)
    OLD_CAT = {"quem-precisa-declarar-imposto-de-renda": "Imposto de Renda", "qual-o-melhor-regime-tributario-para-sua-empresa": "Impostos e tributação",
               "notificacao-simples-nacional": "Impostos e tributação", "principais-tipos-de-contratos-de-trabalho": "Departamento pessoal",
               "capital-social-do-mei": "Abertura de empresa", "nao-posso-ser-mei-o-que-vem-depois": "Abertura de empresa",
               "mei-transportador-autonomo-de-cargas": "Abertura de empresa", "cabeleireiro-pode-ser-mei": "Abertura de empresa",
               "o-que-e-gestao-financeira": "Gestão e rotina contábil", "refissaude": "Impostos e tributação", "empresasdesucesso": "Gestão e rotina contábil"}
    SVC_NAME = {u: pg["nav"] for u, pg in pages.items() if pg["type"] == "servico"}
    SVC_NAME["/trocar-de-contador/"] = "Troca de contador"
    plist = [json.load(open(f, encoding="utf-8")) for f in glob.glob(os.path.join(ROOT, "content", "posts", "*.json"))]
    for po in plist:
        po.setdefault("categoria", OLD_CAT.get(po["slug"].strip("/"), "Gestão e rotina contábil"))
        po["kicker"] = po["categoria"]
        po["description"] = po["description"][:1].upper() + po["description"][1:]
        po["lead"] = ""
        if " | " not in po["title"] and len(po["title"]) <= 44:
            po["title"] = po["title"] + " | ACC Tributos"
        if po.get("revisado") is False:
            po["noindex"] = True
    plist.sort(key=lambda x: (x["date"], x["slug"]), reverse=True)

    def card(x):
        dt = "/".join(reversed(x["date"].split("-")))
        return (f'<a class="rel" href="{x["slug"]}"><span class="km">{e(x["categoria"])} · {dt}</span><h3>{e(x["h1"])}</h3>'
                f'<p>{e(x["description"])}</p><span class="link">Ler artigo <svg width="18" height="18"><use href="#i-arrow"/></svg></span></a>')

    for po in plist:
        art = {"@type": "BlogPosting", "headline": po["h1"], "datePublished": po["date"], "dateModified": po["modified"], "inLanguage": "pt-BR",
               "articleSection": po["categoria"], "author": {"@type": "Organization", "name": "ACC Tributos", "url": SITE + "/"}, "publisher": {"@id": ORG_ID},
               "image": SITE + "/assets/og/home.jpg", "mainEntityOfPage": SITE + po["slug"]}
        d = "/".join(reversed(po["date"].split("-")))
        fontes = ""
        if po.get("fontes"):
            fontes = ('<aside class="post-fontes"><p class="qs-mono">Fontes consultadas</p><ul>'
                      + "".join(f'<li><a href="{e(f["url"])}" target="_blank" rel="noopener nofollow">{e(f["titulo"])}</a></li>' for f in po["fontes"])
                      + "</ul></aside>")
        svc = po.get("servico")
        svc_box = ""
        if svc and svc in SVC_NAME:
            svc_box = (f'<a class="post-svc" href="{svc}"><span class="qs-mono">Serviço relacionado</span><b>{e(SVC_NAME[svc])}</b>'
                       f'<span>Veja como a ACC Tributos cuida disso para sua empresa</span><svg width="20" height="20"><use href="#i-arrow"/></svg></a>')
        rel = [x for x in plist if x is not po and x["categoria"] == po["categoria"]][:3]
        if len(rel) < 3:
            rel += [x for x in plist if x is not po and x not in rel][:3 - len(rel)]
        rel_html = ('<section class="section related" aria-labelledby="t-lt"><div class="wrap"><p class="entry">Leia também</p>'
                    f'<h2 id="t-lt" class="related__h">Mais sobre {e(po["categoria"].lower())}</h2><div class="related__grid">'
                    + "".join(card(x) for x in rel) + "</div></div></section>")
        side_svc = f'<a class="side-card__tel" href="{svc}">Ver o serviço</a>' if svc else '<a class="side-card__tel" href="/servicos/">Ver serviços</a>'
        wa = wa_link("Olá! Li o artigo " + po["h1"] + " e tenho uma dúvida.")
        inner = (f'<section class="section" style="padding-top:var(--s-2)"><div class="wrap prose"><div><article class="post-body">{po["body"]}</article>{svc_box}{fontes}</div>'
                 f'<aside class="prose__side"><div class="side-card"><p class="side-card__t">Ficou com dúvida?</p><p>Um contador responde no WhatsApp, normalmente no mesmo dia.</p>'
                 f'<a class="btn" href="{e(wa)}" data-track="whatsapp" data-wa><span class="wa-dot"><svg><use href="#i-wa"/></svg></span>WhatsApp</a>{side_svc}</div></aside></div></section>'
                 + rel_html)
        upd = ""
        if po["modified"] != po["date"]:
            upd = " · Atualizado em " + "/".join(reversed(po["modified"].split("-")))
        html_text = simple_page(po, inner, [art]).replace('<p class="phero__lead"></p>', f'<p class="post-meta">Publicado em {d}{upd} · Equipe ACC Tributos</p>', 1)
        made.append(write(po["slug"], html_text))
        pages[po["slug"]] = po

    # blog: agrupado por categoria
    cats = ["Notícias e legislação", "Abertura de empresa", "Impostos e tributação", "Imposto de Renda", "Departamento pessoal", "Gestão e rotina contábil", "Certificado e marca"]
    cats = [c for c in cats if any(x["categoria"] == c for x in plist)]
    nav = ('<nav class="blog-cats" aria-label="Categorias">'
           + "".join(f'<a class="chip" href="#cat-{i}">{e(c)} <span>{sum(1 for x in plist if x["categoria"] == c)}</span></a>' for i, c in enumerate(cats))
           + "</nav>")
    groups = "".join(
        f'<section class="blog-cat" id="cat-{i}" aria-labelledby="h-cat-{i}"><h2 id="h-cat-{i}">{e(c)}</h2><div class="related__grid">'
        + "".join(card(x) for x in plist if x["categoria"] == c) + "</div></section>"
        for i, c in enumerate(cats))
    bp = {"slug": "/blog/", "type": "institucional", "nav": "Blog", "kicker": "Blog",
          "title": "Blog de Contabilidade para Empresas | ACC Tributos",
          "description": "Artigos sobre abertura de empresa, MEI, impostos, reforma tributária, Imposto de Renda e departamento pessoal em Fortaleza e região.",
          "h1": "Blog de contabilidade para quem empreende em Fortaleza e região",
          "lead": "Respostas diretas para as dúvidas que mais chegam ao nosso WhatsApp, e as notícias de legislação que mexem com a sua empresa."}
    made.append(write(bp["slug"], simple_page(bp, f'<section class="section" style="padding-top:var(--s-3)"><div class="wrap">{nav}{groups}</div></section>')))

    # obrigado e trabalhe conosco
    import pages_extra
    for fn in pages_extra.ALL:
        meta, inner = fn()
        made.append(write(meta["slug"], simple_page(meta, inner)))
        if not meta.get("noindex"):
            pages[meta["slug"]] = meta

    # política de privacidade (rascunho para revisão jurídica)
    pp = {"slug": "/politica-de-privacidade/", "type": "institucional", "nav": "Política de privacidade", "kicker": "LGPD",
          "title": "Política de Privacidade | ACC Tributos Contabilidade",
          "description": "Como a ACC Tributos coleta, usa e protege os dados pessoais enviados pelo site, WhatsApp e formulários, conforme a Lei Geral de Proteção de Dados.",
          "h1": "Política de privacidade", "lead": "Como tratamos os dados que você envia pelo site, conforme a Lei Geral de Proteção de Dados (Lei 13.709/2018).", "no_final": True}
    blocks = [
        ("Quem somos", "ACC Tributos Assessoria e Consultoria Contábil, com escritório no Edifício Business Place, Torre I, Sala 1103, Av. Yolanda Pontes Vidal Queiroz, 57, Jereissati I, Maracanaú, CE, CEP 61900-410. Somos a controladora dos dados enviados por este site."),
        ("Quais dados coletamos", "Nome, telefone de WhatsApp, e-mail e o assunto que você escolhe no formulário. Também registramos dados de navegação, como páginas visitadas e origem do acesso, por meio de ferramentas de análise."),
        ("Para que usamos", "Para responder seu contato, enviar a proposta que você pediu e entender quais páginas ajudam mais quem nos procura. Não vendemos nem cedemos seus dados para terceiros fora dessas finalidades."),
        ("Por quanto tempo guardamos", "Pelo tempo necessário para o atendimento e para cumprir obrigações legais e contábeis. Depois disso, os dados são excluídos ou anonimizados."),
        ("Seus direitos", "Você pode pedir acesso, correção, exclusão ou portabilidade dos seus dados, ou retirar o consentimento, pelo WhatsApp (85) 98754-1948."),
        ("Cookies", "Usamos cookies para medir o uso do site e melhorar o atendimento. Você pode bloqueá-los nas configurações do seu navegador."),
    ]
    inner = '<section class="section" style="padding-top:var(--s-3)"><div class="wrap"><article class="prose__main prose__main--narrow">' + "".join(
        f'<section class="prose__block"><h2>{e(h)}</h2><p>{e(t)}</p></section>' for h, t in blocks) + f'<p class="muted">Atualizada em {date.today().strftime("%d/%m/%Y")}.</p></article></div></section>'
    made.append(write(pp["slug"], simple_page(pp, inner)))

    # 404
    nf = {"slug": "/404/", "type": "institucional", "nav": "Página não encontrada", "kicker": "Erro 404", "noindex": True,
          "title": "Página não encontrada | ACC Tributos", "description": "A página que você procurou não existe ou mudou de endereço.",
          "h1": "Essa página não existe ou mudou de endereço", "lead": "Use os atalhos abaixo ou fale direto com um contador pelo WhatsApp."}
    links = "".join(f'<a class="chip" href="{u}">{n} <svg><use href="#i-arrow"/></svg></a>' for n, u in
                    [("Página inicial", "/"), ("Serviços", "/servicos/"), ("Contabilidade em Fortaleza", "/contabilidade-em-fortaleza/"), ("Abrir empresa", "/servicos/legalizacao-de-empresas/"), ("Contato", "/contato/")])
    open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8").write(
        simple_page(nf, f'<section class="section" style="padding-top:var(--s-3)"><div class="wrap"><div class="chips" style="justify-content:flex-start">{links}</div></div></section>'))

    # sitemap: só páginas que existem
    urls = ["/"] + sorted(({"/servicos/", "/blog/", "/politica-de-privacidade/"} | set(pages)) - {u for u, pg in pages.items() if pg.get("noindex")})
    prio = lambda u: "1.0" if u == "/" else ("0.9" if "contabilidade-em" in u or u.startswith("/servicos/") else "0.6")
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
        f"  <url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod><priority>{prio(u)}</priority></url>\n" for u in urls) + "</urlset>\n"
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write(sm)
    print(f"{len(made)} páginas geradas, 404.html e sitemap.xml com {len(urls)} URLs")


if __name__ == "__main__":
    build()
