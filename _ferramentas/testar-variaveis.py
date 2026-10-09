"""Compara o que o Google Fonts devolve para pesos fixos e para faixas variáveis."""
import re
import urllib.request

UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')


def medir(rotulo, url):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    css = urllib.request.urlopen(req, timeout=30).read().decode('utf-8')
    blocos = re.findall(r'/\*\s*([\w-]+)\s*\*/\s*(@font-face\s*\{.*?\})', css, re.S)
    vistos = {}
    for subset, bloco in blocos:
        if subset != 'latin':
            continue
        url_fonte = re.search(r'url\((https://[^)]+\.woff2)\)', bloco).group(1)
        peso = re.search(r'font-weight:\s*([^;]+);', bloco).group(1).strip()
        estilo = re.search(r'font-style:\s*(\w+);', bloco).group(1)
        if url_fonte in vistos:
            vistos[url_fonte].append(peso + '/' + estilo)
            continue
        dados = urllib.request.urlopen(
            urllib.request.Request(url_fonte, headers={'User-Agent': UA}), timeout=30).read()
        vistos[url_fonte] = [peso + '/' + estilo]
        print('  {:>6} KB  {}'.format(round(len(dados) / 1024), peso + ' ' + estilo))
    print('  arquivos distintos:', len(vistos))


print('Cormorant Garamond 400..500 (faixa):')
medir('cg-var', 'https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400..500&display=swap')

print('Nunito Sans 400..600 (faixa):')
medir('ns-var', 'https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@400..600&display=swap')
