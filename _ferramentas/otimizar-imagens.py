"""Gera as imagens do site em WebP (principal) e JPEG (reserva), já no tamanho de exibição."""
import os
from PIL import Image

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESTINO = os.path.join(BASE, 'assets', 'img')
FONTE = r'C:\Users\Guilherme\Downloads\resultado 1_files'

# (origem, nome final, recorte (x, y, largura, altura) ou None, largura final)
TRABALHOS = [
    (os.path.join(FONTE, '624721697_18069666323408446_3989040278953219899_n.jpg'),
     'dra-marina-retrato', (55, 0, 970, 770), 970),
    (os.path.join(FONTE, '468046235_17911181694029370_2293691519627241639_n.jpg'),
     'dra-marina-atendimento', (71, 0, 894, 1118), 800),
    (os.path.join(FONTE, '519321639_17937837201029370_7554433189331731292_n.jpg'),
     'resultado-clareamento', None, 760),
    (os.path.join(FONTE, '477177723_17920831206029370_8111775288373336433_n.jpg'),
     'resultado-naturalidade', None, 760),
    (os.path.join(FONTE, '491440472_17927829681029370_4862627603969823386_n.jpg'),
     'resultado-transformacao', None, 760),
]

total_webp = 0
total_jpg = 0

for origem, nome, recorte, largura in TRABALHOS:
    img = Image.open(origem).convert('RGB')
    if recorte:
        x, y, w, h = recorte
        img = img.crop((x, y, x + w, y + h))
    altura = round(largura * img.height / img.width)
    img = img.resize((largura, altura), Image.LANCZOS)

    caminho_jpg = os.path.join(DESTINO, nome + '.jpg')
    caminho_webp = os.path.join(DESTINO, nome + '.webp')
    img.save(caminho_jpg, 'JPEG', quality=78, optimize=True, progressive=True)
    img.save(caminho_webp, 'WEBP', quality=76, method=6)

    kb_jpg = os.path.getsize(caminho_jpg) / 1024
    kb_webp = os.path.getsize(caminho_webp) / 1024
    total_jpg += kb_jpg
    total_webp += kb_webp
    print('{:<26} {}x{}  jpg {:>5.0f} KB   webp {:>5.0f} KB'.format(
        nome, largura, altura, kb_jpg, kb_webp))

print('total jpg: {:.0f} KB | total webp: {:.0f} KB'.format(total_jpg, total_webp))
