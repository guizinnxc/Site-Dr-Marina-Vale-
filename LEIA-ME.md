# Site da Dra. Marina Vale

Site institucional de uma página, em HTML, CSS e JavaScript puros —
sem framework, sem build, sem dependências externas além das fontes do Google.

## Arquivos

```
site-marina-vale/
├─ index.html                     página única com todas as seções
├─ assets/
│  ├─ css/estilos.css             identidade visual completa
│  ├─ js/site.js                  menu, âncoras, galeria, botão fixo
│  └─ img/
│     ├─ dra-marina-retrato.jpg       abertura (970 × 770)
│     ├─ dra-marina-atendimento.jpg   seção "Sobre" (800 × 1000)
│     └─ favicon.svg                  ícone (arco do sorriso)
├─ PENDENCIAS.md                  o que falta confirmar com a dentista
└─ LEIA-ME.md                     este arquivo
```

## Como abrir

Basta abrir `index.html` no navegador. Para testar como ficará publicado:

```bash
python -m http.server 8787 --directory site-marina-vale
```

## Como editar o essencial

| O quê | Onde |
|---|---|
| WhatsApp | `index.html`, procure por `5524981040504` e `(24) 98104-0504` |
| Mensagem inicial do WhatsApp | parte `?text=` de cada link `wa.me` |
| Endereço | procure por `Coronel Manoel Bernardes` |
| Cores | `assets/css/estilos.css`, bloco `:root` no topo |
| Tratamentos | `index.html`, seção `<section id="tratamentos">` |
| Perguntas frequentes | `<section id="perguntas">` |

### Marcações de pendência

Tudo que ainda não foi confirmado aparece com uma etiqueta tracejada.
No rodapé há o botão **"Ocultar marcações de pendência"** — útil para
apresentar o site à cliente sem as etiquetas. A escolha fica guardada
no navegador de quem clicou.

Para remover definitivamente, apague do HTML os `<span class="pendente">…</span>`
e os elementos com a classe `pendente-bloco`.

### Trocar as fotos

Substitua os arquivos em `assets/img/` mantendo os nomes **e atualize os
atributos `width` e `height`** nas tags `<img>` do `index.html` — eles reservam
o espaço da imagem e evitam que o texto "pule" durante o carregamento.

Na galeria do consultório, cada espaço reservado é assim:

```html
<figure class="galeria__slide" aria-label="1 de 3">
  <div class="espaco-foto"> … </div>
  <figcaption class="pendente-bloco">…</figcaption>
</figure>
```

Troque o `<div class="espaco-foto">` por:

```html
<img src="assets/img/consultorio-1.jpg" width="1200" height="900"
     loading="lazy" decoding="async" alt="Descreva a foto em poucas palavras.">
```

e apague o `<figcaption>`. A navegação por setas, teclado e deslizar
continua funcionando.

## Decisões técnicas

- **Sem JavaScript o site continua inteiro**: o menu de telas pequenas é o
  único recurso que depende do script; as perguntas e o "Saiba mais" usam
  `<details>` nativo, e todos os links funcionam sozinhos.
- **Movimento reduzido** (`prefers-reduced-motion`) é respeitado: as transições
  praticamente desaparecem e nada depende de animação para ser lido.
- **Hover só em quem tem mouse** (`@media (hover: hover)`), para o estado não
  "grudar" depois do toque no celular.
- **Fontes**: Cormorant Garamond (títulos) e Nunito Sans (texto), carregadas do
  Google Fonts com `display=swap`. Para deixar o site 100% independente,
  baixe os `.woff2` e troque o `<link>` por `@font-face`.
- **Imagens**: a da abertura carrega com prioridade; a de "Sobre" carrega sob
  demanda (`loading="lazy"`).
