"""Check local rendered targets/fragments and unique IDs of the fresh site."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit,unquote
class Page(HTMLParser):
    def __init__(self):
        super().__init__();self.ids=set();self.links=[]
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if 'id' in attrs:
            assert attrs['id'] not in self.ids,('duplicate id',attrs['id'])
            self.ids.add(attrs['id'])
        if tag=='a' and 'href' in attrs:self.links.append(attrs['href'])
root=Path('site').resolve();pages={}
for p in root.rglob('*.html'):
    parsed=Page();parsed.feed(p.read_text());pages[p]=parsed
for source,page in pages.items():
    for href in page.links:
        u=urlsplit(href)
        if u.scheme or u.netloc:continue
        path=unquote(u.path)
        if path.startswith('/modern-quantum-computing/'):path=path[len('/modern-quantum-computing/'):]
        target=((root/path.lstrip('/')) if path.startswith('/') else (source.parent/path)).resolve() if path else source
        if target.is_dir():target=target/'index.html'
        assert target.exists(),(source,href,target)
        if u.fragment and target in pages:
            assert unquote(u.fragment) in pages[target].ids,(source,href)
print(f'Checked {len(pages)} freshly rendered pages:all local links/fragments resolve;IDs unique.')
