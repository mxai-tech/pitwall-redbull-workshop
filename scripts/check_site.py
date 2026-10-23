"""Comprueba archivos y fragmentos enlazados en el sitio compilado, sin acceso a red."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import sys

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / '_site'
BASE = '/pitwall-redbull-workshop'
class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path, self.links, self.ids = path, [], set()
        self.feed(path.read_text())
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs: self.ids.add(attrs['id'])
        for key in ('href', 'src'):
            if key in attrs: self.links.append(attrs[key])

pages = {p: Page(p) for p in SITE.rglob('*.html')}
errors, count = [], 0
for path, page in pages.items():
    for href in page.links:
        url = urlsplit(href)
        if url.scheme or url.netloc: continue
        target = unquote(url.path)
        if target.startswith('/'):
            if BASE and not (target == BASE or target.startswith(BASE + '/')):
                errors.append(f'{path.relative_to(SITE)}: ruta fuera de baseurl: {href}')
                continue
            dest = SITE / target[len(BASE):].lstrip('/')
        elif target:
            dest = path.parent / target
        else:
            dest = path
        if dest.is_dir(): dest /= 'index.html'
        count += 1
        if not dest.is_file(): errors.append(f'{path.relative_to(SITE)}: falta {href}')
        elif url.fragment and dest in pages and unquote(url.fragment) not in pages[dest].ids:
            errors.append(f'{path.relative_to(SITE)}: fragmento ausente {href}')
for error in errors: print(error)
print(f'{len(pages)} páginas; {count} enlaces internos; {len(errors)} errores')
sys.exit(bool(errors))
