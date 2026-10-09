"""Baixa do Google Fonts só o necessário (fontes variáveis, subset latino) e gera o CSS local.

Resultado: 3 arquivos woff2 em assets/fonts/ e as regras @font-face em _ferramentas/fontes.css.
"""
import os
import re
import urllib.request

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA = os.path.join(BASE, 'assets', 'fonts')
os.makedirs(PASTA, exist_ok=True)

UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')

# Uma fonte variável por família cobre todos os pesos usados no site.
PEDIDOS = [
    ('cormorant-garamond-variavel',
     'https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400..500&display=swap'),
    ('cormorant-garamond-italico',
     'https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@1,400&display=swap'),
    ('nunito-sans-variavel',
     'https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@400..600&display=swap'),
]


def baixar(url):
    return urllib.request.urlopen(
        urllib.request.Request(url, headers={'User-Agent': UA}), timeout=30).read()


regras = []
total = 0

for nome, url in PEDIDOS:
    css = baixar(url).decode('utf-8')
    blocos = re.findall(r'/\*\s*([\w-]+)\s*\*/\s*(@font-face\s*\{.*?\})', css, re.S)
    bloco = next(b for s, b in blocos if s == 'latin')   # português cabe no subset latin

    familia = re.search(r"font-family:\s*'([^']+)'", bloco).group(1)
    peso = re.search(r'font-weight:\s*([^;]+);', bloco).group(1).strip()
    estilo = re.search(r'font-style:\s*(\w+);', bloco).group(1)
    faixa = re.search(r'unicode-range:\s*([^;]+);', bloco).group(1)
    url_fonte = re.search(r'url\((https://[^)]+\.woff2)\)', bloco).group(1)

    arquivo = nome + '.woff2'
    dados = baixar(url_fonte)
    with open(os.path.join(PASTA, arquivo), 'wb') as f:
        f.write(dados)
    total += len(dados)
    print('  {:<36} {:>5} KB   peso {} {}'.format(arquivo, round(len(dados) / 1024), peso, estilo))

    regras.append(
        "@font-face {{\n"
        "  font-family: '{familia}';\n"
        "  font-style: {estilo};\n"
        "  font-weight: {peso};\n"
        "  font-display: swap;\n"
        "  src: url('../fonts/{arquivo}') format('woff2');\n"
        "  unicode-range: {faixa};\n"
        "}}".format(familia=familia, estilo=estilo, peso=peso, arquivo=arquivo, faixa=faixa))

with open(os.path.join(BASE, '_ferramentas', 'fontes.css'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(regras) + '\n')

print('total baixado:', round(total / 1024), 'KB em', len(PEDIDOS), 'arquivos')
