# Pendências — site da Dra. Marina Vale

Lista para revisar **com a Dra. Marina antes de publicar**.
No site, cada ponto pendente aparece marcado com uma etiqueta tracejada
("A confirmar" / "A preencher"). No rodapé há um botão que esconde todas
essas marcações, para apresentar o site sem elas.

---

## 1. Confirmar antes de qualquer publicação

| Item | O que está no site hoje | De onde veio |
|---|---|---|
| **WhatsApp** | `(24) 98104-0504` → `wa.me/5524981040504` | número divulgado pela própria dentista em publicações do perfil |
| **CRO** | CRO-RJ 48370 | aparece na bio e assinado em várias legendas |
| **Endereço** | Rua Coronel Manoel Bernardes, 45 — Sala 201 | publicações do perfil |
| **Cidade / UF / CEP** | não preenchido | — |

- O **número de WhatsApp precisa ser confirmado**: ele aparece em publicações
  assinadas em conjunto com outro profissional, então pode ser da clínica e não
  dela. Enquanto não houver confirmação, não divulgue o site.
- A **cidade do consultório não está confirmada**. Uma publicação está marcada em
  Paty do Alferes (RJ) e as hashtags citam também Miguel Pereira, Vassouras,
  Três Rios e Paraíba do Sul. Sem a cidade, o botão "Como chegar" pode levar ao
  endereço errado.
- **Horários de atendimento**: nada confirmado.
- **Atendimento ativo?** Há uma publicação recente em que ela fala de um período
  de recuperação. Vale confirmar se já está atendendo antes de o site convidar
  para agendar.

## 2. Conteúdo a preencher

- **Formação e trajetória** — graduação, especializações, cursos, tempo de
  atuação. Há um bloco reservado na seção "Sobre".
- **Lista definitiva de tratamentos.** Os quatro que estão no site foram
  deduzidos das legendas dela:
  1. Clareamento dental (consultório + caseiro supervisionado);
  2. Próteses sobre implantes / protocolo com carga imediata;
  3. Coroas sobre dente e sobre implante / reabilitação oral;
  4. Harmonização orofacial (preenchimento labial).
  Revisar a lista e o texto de cada um — inclusive o "Saiba mais".
- **Convênios, formas de pagamento, estacionamento e acessibilidade.**
- **Aprovação das frases citadas.** As duas citações do site são palavras dela,
  tiradas do perfil e de uma legenda:
  - "Apaixonada por elevar autoestima e autoconfiança. / Mudando realidades
    através do sorriso." (bio)
  - "A odontologia nunca vai ser só sobre dentes. É sobre devolver sorrisos,
    autoestima, segurança, função e um pouco mais de vontade de viver."
    (legenda de publicação)

## 3. Imagens

- **Retrato profissional em alta resolução.** O do site foi recortado de uma
  publicação (970 × 770 px) — serve para apresentar, mas é pouco para telas
  retina e impressão.
- **Fotos do consultório** — a galeria tem 3 espaços reservados
  (recepção, sala de atendimento, detalhe do espaço).
- **Logo**, se vier a ser criado. Enquanto isso o site usa uma assinatura
  tipográfica ("Marina Vale" + "Cirurgiã-dentista") com um arco que representa
  a curva do sorriso.
- Foto de atendimento usada na seção "Sobre": confirmar se pode ficar
  (aparecem as mãos de uma paciente, sem rosto).

## 4. Decisões

- **Seção de resultados (antes e depois): não foi incluída.** Existem fotos
  clínicas boas no perfil, mas publicá-las no site exige
  (a) autorização por escrito dos pacientes para uso no site, e
  (b) conferir as regras de publicidade do CFO / CRO-RJ para esse tipo de
  imagem. Confirmando os dois pontos, a seção é rápida de montar.
- **Depoimentos**: mesma regra — só com material real e autorizado.
- **Creditar parceiros** (por exemplo, o cirurgião responsável pela etapa
  cirúrgica nos casos de protocolo) — decidir se entra no site.
- **Domínio e hospedagem.** O site é estático: funciona em qualquer hospedagem
  simples (Netlify, Vercel, GitHub Pages, Hostinger…).
- **Perfil no Google** para o botão "Como chegar" funcionar com precisão.

## 5. Ajustes técnicos no momento da publicação

- Trocar o número: `5524981040504` aparece **16 vezes** no `index.html`,
  `(24) 98104-0504` **3 vezes** e `+55 24 98104-0504` **1 vez** (dados
  estruturados).
- Endereço: `Rua Coronel Manoel Bernardes` aparece **5 vezes**.
- Completar o bloco de dados estruturados (`application/ld+json`) com endereço
  e horários — hoje ele traz só o que está confirmado.
- Definir a URL do site e deixar `og:image` como endereço absoluto
  (hoje é um caminho relativo).
- Gerar versões `.webp` das fotos finais, se a hospedagem permitir.
