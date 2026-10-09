"""Reduz os woff2 para o conjunto de caracteres que um site em português precisa."""
import glob
import os
from fontTools import subset

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA = os.path.join(BASE, 'assets', 'fonts')

# ASCII + Latin-1 (acentos do português) + aspas, travessões e reticências tipográficas
UNICODES = (
    'U+0020-007E,'      # básico
    'U+00A0-00FF,'      # á à â ã ç é ê í ó ô õ ú ü ñ °
    'U+0152-0153,'      # Œ œ
    'U+2010-2015,'      # hífens e travessões
    'U+2018-201A,'      # aspas simples
    'U+201C-201E,'      # aspas duplas
    'U+2026,'           # …
    'U+2022,'           # •
    'U+00B7,'           # ·
    'U+20AC,'           # €
    'U+2122'            # ™
)

total_antes = 0
total_depois = 0

for caminho in sorted(glob.glob(os.path.join(PASTA, '*.woff2'))):
    if caminho.endswith('.orig.woff2'):
        continue
    antes = os.path.getsize(caminho)
    original = caminho.replace('.woff2', '.orig.woff2')
    if not os.path.exists(original):
        os.replace(caminho, original)

    subset.main([
        original,
        '--output-file=' + caminho,
        '--flavor=woff2',
        '--unicodes=' + UNICODES,
        '--layout-features=kern,liga,clig,calt,ccmp,locl,mark,mkmk',
        '--no-hinting',
        '--desubroutinize',
        '--name-IDs=1,2,3,4,6',
        '--drop-tables+=DSIG',
    ])

    depois = os.path.getsize(caminho)
    total_antes += antes
    total_depois += depois
    print('{:<40} {:>5} KB -> {:>5} KB  (-{:.0f}%)'.format(
        os.path.basename(caminho), round(antes / 1024), round(depois / 1024),
        100 * (1 - depois / antes)))
    os.remove(original)

print('total: {} KB -> {} KB'.format(round(total_antes / 1024), round(total_depois / 1024)))
