"""Compara o peso da primeira tela antes e depois das otimizações.

A versão anterior é lida do commit do git; a atual, do disco.
Para os arquivos de texto mostra também o tamanho com gzip, que é o que
uma hospedagem real envia.
"""
import gzip
import os
import subprocess

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMMIT = 'e8e1a51'   # último commit antes das otimizações


def do_git(caminho):
    return subprocess.run(['git', 'show', '{}:{}'.format(COMMIT, caminho)],
                          cwd=BASE, capture_output=True).stdout


def do_disco(caminho):
    with open(os.path.join(BASE, caminho), 'rb') as f:
        return f.read()


def comprimivel(caminho):
    return caminho.endswith(('.html', '.css', '.js', '.svg'))


def medir(rotulo, itens, extras):
    print('\n' + rotulo)
    bruto = gz = 0
    for nome, dados in itens:
        b = len(dados)
        g = len(gzip.compress(dados, 9)) if comprimivel(nome) else b
        bruto += b
        gz += g
        print('  {:<34} {:>7} B   gzip {:>7} B'.format(nome, b, g))
    for nome, b in extras:
        bruto += b
        gz += b
        print('  {:<34} {:>7} B   gzip {:>7} B'.format(nome, b, b))
    print('  {:<34} {:>7} B   gzip {:>7} B'.format('TOTAL', bruto, gz))
    print('  {:<34} {:>7} KB  gzip {:>7} KB'.format('', round(bruto / 1024), round(gz / 1024)))
    return bruto, gz, len(itens) + len(extras)


# ---- Antes (commit) ----
antes_itens = [
    ('index.html', do_git('index.html')),
    ('assets/css/estilos.css', do_git('assets/css/estilos.css')),
    ('assets/js/site.js', do_git('assets/js/site.js')),
    ('dra-marina-retrato.jpg', do_git('assets/img/dra-marina-retrato.jpg')),
]
antes_extras = [
    ('Google Fonts: css2', 14977),
    ('Google Fonts: cormorant 400-600', 37 * 1024),
    ('Google Fonts: cormorant italico', 23 * 1024),
    ('Google Fonts: nunito 300-600', 30 * 1024),
]

# ---- Depois (disco) ----
depois_itens = [
    ('index.html', do_disco('index.html')),
    ('assets/css/estilos.css', do_disco('assets/css/estilos.css')),
    ('assets/js/site.js', do_disco('assets/js/site.js')),
    ('dra-marina-retrato.webp', do_disco('assets/img/dra-marina-retrato.webp')),
    ('cormorant-variavel.woff2', do_disco('assets/fonts/cormorant-garamond-variavel.woff2')),
    ('cormorant-italico.woff2', do_disco('assets/fonts/cormorant-garamond-italico.woff2')),
    ('nunito-variavel.woff2', do_disco('assets/fonts/nunito-sans-variavel.woff2')),
]

a_bruto, a_gz, a_req = medir('ANTES (primeira tela)', antes_itens, antes_extras)
d_bruto, d_gz, d_req = medir('DEPOIS (primeira tela)', depois_itens, [])

print('\nRESUMO')
print('  requisições: {} -> {}'.format(a_req, d_req))
print('  bytes:       {} -> {}  ({:+.0f}%)'.format(a_bruto, d_bruto, 100 * (d_bruto / a_bruto - 1)))
print('  com gzip:    {} -> {}  ({:+.0f}%)'.format(a_gz, d_gz, 100 * (d_gz / a_gz - 1)))
print('  domínios externos: 2 -> 0')
