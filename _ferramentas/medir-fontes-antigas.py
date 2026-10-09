"""Mede o que a versão anterior (Google Fonts) baixava de verdade no subset latino."""
import re
import urllib.request

UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')

URL = ('https://fonts.googleapis.com/css2'
       '?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400'
       '&family=Nunito+Sans:wght@300;400;600'
       '&display=swap')

req = urllib.request.Request(URL, headers={'User-Agent': UA})
css = urllib.request.urlopen(req, timeout=30).read()
print('CSS do Google Fonts: {} bytes'.format(len(css)))

blocos = re.findall(r'/\*\s*([\w-]+)\s*\*/\s*(@font-face\s*\{.*?\})', css.decode('utf-8'), re.S)
arquivos = {}
for subset, bloco in blocos:
    if subset != 'latin':
        continue
    url = re.search(r'url\((https://[^)]+\.woff2)\)', bloco).group(1)
    peso = re.search(r'font-weight:\s*([^;]+);', bloco).group(1).strip()
    estilo = re.search(r'font-style:\s*(\w+);', bloco).group(1)
    arquivos.setdefault(url, []).append(peso + ' ' + estilo)

total = len(css)
for url, usos in arquivos.items():
    dados = urllib.request.urlopen(
        urllib.request.Request(url, headers={'User-Agent': UA}), timeout=30).read()
    total += len(dados)
    print('  {:>6} KB  {}'.format(round(len(dados) / 1024), ', '.join(usos)))

print('arquivos distintos:', len(arquivos))
print('total de fontes na versão anterior: {} KB em {} requisições'.format(
    round(total / 1024), len(arquivos) + 1))
