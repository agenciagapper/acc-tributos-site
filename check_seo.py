"""Checagem de SEO das páginas geradas (uso: python check_seo.py)."""
import glob, json, os, re, collections

ROOT = os.path.dirname(os.path.abspath(__file__))
files = [os.path.join(ROOT, "index.html")] + [f for f in glob.glob(os.path.join(ROOT, "**", "index.html"), recursive=True) if os.path.dirname(f) != ROOT]
titles, descs, problems = collections.Counter(), collections.Counter(), []
def exists(href):
    path = href.split("#")[0].split("?")[0]
    if path in ("", "/"): return True
    p = os.path.join(ROOT, path.strip("/").replace("/", os.sep))
    return os.path.isfile(p) or os.path.isfile(os.path.join(p, "index.html"))
rows = []
for f in sorted(files):
    s = open(f, encoding="utf-8").read()
    rel = "/" + os.path.relpath(os.path.dirname(f), ROOT).replace(os.sep, "/").strip(".") + "/"
    rel = rel.replace("//", "/")
    t = re.search(r"<title>(.*?)</title>", s).group(1)
    d = re.search(r'<meta name="description" content="(.*?)"', s).group(1)
    titles[t] += 1; descs[d] += 1
    h1 = re.findall(r"<h1[^>]*>", s)
    words = len(re.sub(r"<script.*?</script>|<style.*?</style>|<[^>]+>", " ", s, flags=re.S).split())
    noidx = 'name="robots" content="noindex' in s
    if not noidx and not 30 <= len(t) <= 62: problems.append(f"{rel} title com {len(t)} caracteres")
    if not noidx and not 110 <= len(d) <= 165: problems.append(f"{rel} description com {len(d)} caracteres")
    if len(h1) != 1: problems.append(f"{rel} tem {len(h1)} H1")
    if "—" in s or "–" in s: problems.append(f"{rel} contém travessão")
    for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try: json.loads(m)
        except Exception as ex: problems.append(f"{rel} JSON-LD inválido: {ex}")
    for h in set(re.findall(r'href="(/[^"]*)"', s)):
        if not exists(h): problems.append(f"{rel} link quebrado {h}")
    rows.append((rel, len(t), len(d), words))
for t, n in titles.items():
    if n > 1: problems.append(f"title repetido {n}x: {t}")
for d, n in descs.items():
    if n > 1: problems.append(f"description repetida {n}x: {d[:60]}")
for r in rows: print(f"{r[0]:<58} title {r[1]:>3}  desc {r[2]:>3}  palavras {r[3]:>5}")
print("\nPROBLEMAS:" if problems else "\nSem problemas.")
for p in sorted(set(problems)): print(" -", p)
