"""Monta a versão de prévia para o GitHub Pages em _site/.

- Copia só o que o site usa (sem _material/, content/, scripts e documentos internos).
- Prefixa os caminhos absolutos com a subpasta do Pages (ex.: /acc-tributos-site/).
- Marca todas as páginas como noindex e bloqueia robôs: é uma prévia, não o site oficial.

Uso: python deploy_pages.py /acc-tributos-site
"""
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "_site")
BASE = (sys.argv[1] if len(sys.argv) > 1 else "/acc-tributos-site").rstrip("/")

SKIP_DIRS = {".git", ".github", ".claude", "_material", "content", "__pycache__", "_site", "api"}
SKIP_FILES = {"build.py", "check_seo.py", "deploy_pages.py", "quem_somos.py", "pages_extra.py",
              "README.md", "arquitetura-seo.md", "revisao-artigos.md", ".gitignore"}

if os.path.isdir(OUT):
    shutil.rmtree(OUT)

# caminhos internos que começam com "/" (não "//", que é outro domínio)
ATTR = re.compile(r'''((?:href|src|action)=["'])/(?!/)''')
CSS_URL = re.compile(r'''url\((["']?)/(?!/)''')
JS_PATHS = re.compile(r'''(['"])/(obrigado-whatsapp/|obrigado/|trabalhe-conosco/obrigado/|api/form\.php|politica-de-privacidade/)''')
NOINDEX = '<meta name="robots" content="noindex, nofollow">'

def fix_html(s):
    s = re.sub(r'<meta name="robots" content="[^"]*">\n?', "", s)
    s = s.replace("<head>", "<head>\n" + NOINDEX, 1)
    s = ATTR.sub(lambda m: m.group(1) + BASE + "/", s)
    s = CSS_URL.sub(lambda m: "url(" + m.group(1) + BASE + "/", s)
    # o JSON-LD e o canonical continuam apontando para acctributos.com.br (domínio oficial)
    return s

for dirpath, dirnames, filenames in os.walk(ROOT):
    rel = os.path.relpath(dirpath, ROOT)
    parts = [] if rel == "." else rel.split(os.sep)
    if parts and parts[0] in SKIP_DIRS:
        dirnames[:] = []
        continue
    dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
    for fn in filenames:
        if not parts and fn in SKIP_FILES:
            continue
        src = os.path.join(dirpath, fn)
        dst = os.path.join(OUT, rel, fn) if parts else os.path.join(OUT, fn)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if fn.endswith(".html"):
            open(dst, "w", encoding="utf-8").write(fix_html(open(src, encoding="utf-8").read()))
        elif fn.endswith(".css"):
            open(dst, "w", encoding="utf-8").write(CSS_URL.sub(lambda m: "url(" + m.group(1) + BASE + "/", open(src, encoding="utf-8").read()))
        elif fn.endswith(".js"):
            s = open(src, encoding="utf-8").read()
            s = JS_PATHS.sub(lambda m: m.group(1) + BASE + "/" + m.group(2), s)
            open(dst, "w", encoding="utf-8").write(s)
        else:
            shutil.copy2(src, dst)

# prévia: nada de indexação
open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8").write("User-agent: *\nDisallow: /\n")
if os.path.exists(os.path.join(OUT, "sitemap.xml")):
    os.remove(os.path.join(OUT, "sitemap.xml"))
# GitHub Pages: sem Jekyll, e 404 próprio
open(os.path.join(OUT, ".nojekyll"), "w").close()

n = sum(len(f) for _, _, f in os.walk(OUT))
print(f"_site pronto com {n} arquivos, base {BASE}/")
