# Site da Dra. Marina Vale

Site institucional de uma página, em HTML, CSS e JavaScript puros —
sem framework, sem build e **sem nenhuma dependência externa**: fontes e
imagens são servidas pelo próprio site.

## Arquivos

```
site-marina-vale/
├─ index.html                     página única com todas as seções
├─ assets/
│  ├─ css/estilos.css             identidade visual + @font-face
│  ├─ js/site.js                  menu, âncoras, galeria, botão fixo
│  ├─ fonts/                      3 arquivos .woff2 (subset latino)
│  └─ img/                        cada foto em .webp e .jpg
├─ _ferramentas/                  scripts usados na preparação (não vão para o ar)
├─ PENDENCIAS.md                  o que falta confirmar com a dentista
└─ LEIA-ME.md                     este arquivo
```

Para publicar, suba tudo **menos** a pasta `_ferramentas/`.

## Como abrir

Duplo clique no `index.html` já funciona. Para testar como ficará publicado:

```bash
python -m http.server 8790
```

## Como editar o essencial

| O quê | Onde |
|---|---|
| WhatsApp | `index.html`, procure por `5524981040504` e `(24) 98104-0504` |
| Mensagem inicial do WhatsApp | parte `?text=` de cada link `wa.me` |
| Endereço | procure por `Coronel Manoel Bernardes` |
| Cores | `assets/css/estilos.css`, bloco `:root` no topo |
| Tratamentos | `<section id="tratamentos">` |
| Resultados (antes e depois) | `<section id="resultados">` |
| Perguntas frequentes | `<section id="perguntas">` |

### Marcações de pendência

Tudo que ainda não foi confirmado aparece com uma etiqueta tracejada.
No rodapé há o botão **"Ocultar marcações de pendência"** — útil para
apresentar o site à cliente sem as etiquetas. A escolha fica guardada
no navegador de quem clicou.

Para remover definitivamente, apague do HTML os `<span class="pendente">…</span>`
e os elementos com a classe `pendente-bloco`.

### Trocar ou acrescentar fotos

Cada foto existe em dois formatos: `.webp` (usado por todos os navegadores
atuais) e `.jpg` (reserva). O HTML já traz os dois:

```html
<picture>
  <source srcset="assets/img/nome.webp" type="image/webp">
  <img src="assets/img/nome.jpg" width="760" height="760"
       loading="lazy" decoding="async" alt="Descreva a foto.">
</picture>
```

Para gerar o par a partir de uma foto nova, ajuste a lista em
`_ferramentas/otimizar-imagens.py` e rode:

```bash
python _ferramentas/otimizar-imagens.py
```

**Sempre atualize `width` e `height`** no HTML: são eles que reservam o espaço
da imagem e evitam que o texto "pule" durante o carregamento.

Na galeria do consultório os três espaços reservados são assim:

```html
<figure class="galeria__slide" aria-label="1 de 3">
  <div class="espaco-foto"> … </div>
  <figcaption class="pendente-bloco">…</figcaption>
</figure>
```

Troque o `<div class="espaco-foto">` pelo `<picture>` da foto e apague o
`<figcaption>`. A navegação por setas, teclado e deslizar continua funcionando.

## Decisões técnicas

- **Sem JavaScript o site continua inteiro**: o menu de telas pequenas é o
  único recurso que depende do script; as perguntas e o "Saiba mais" usam
  `<details>` nativo, e todos os links funcionam sozinhos.
- **Fontes hospedadas aqui**: Cormorant Garamond (títulos) e Nunito Sans
  (texto), em versão variável e com subset latino — 3 arquivos, 69 KB no total,
  nenhuma conexão com o Google. Para regerá-las:
  `python _ferramentas/baixar-fontes.py && python _ferramentas/reduzir-fontes.py`
  (precisa de `pillow`, `fonttools` e `brotli`).
- **Movimento reduzido** (`prefers-reduced-motion`) é respeitado: as transições
  praticamente desaparecem e nada depende de animação para ser lido.
- **Hover só em quem tem mouse** (`@media (hover: hover)`), para o estado não
  "grudar" depois do toque no celular.
- **Menu horizontal a partir de 1000 px**; abaixo disso, menu em painel e botão
  fixo de WhatsApp.
- **Imagens abaixo da primeira tela carregam sob demanda** (`loading="lazy"`);
  a da abertura tem prioridade alta e é pré-carregada.
