"""Aplica a revisão de texto no index.html. Cada troca é conferida antes de gravar."""
import io
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAMINHO = os.path.join(BASE, 'index.html')

TROCAS = [
    # 1. Regência: "o cuidado que o seu sorriso precisa" (precisar exige "de")
    ('Converse com a Dra. Marina Vale sobre o cuidado que o seu sorriso precisa.',
     'Fale com a Dra. Marina Vale e entenda as opções para o seu caso.'),

    # 2. Padroniza o tratamento da profissional
    ('Marina Vale é cirurgiã-dentista inscrita no CRO-RJ sob o número 48370.',
     'A Dra. Marina Vale é cirurgiã-dentista, inscrita no CRO-RJ sob o número 48370.'),

    # 3. "quem está na cadeira" soa informal demais
    ('será feito e decide o caminho junto com quem está na cadeira.',
     'será feito e decide o caminho junto com o paciente.'),

    # 4. "divulgados pela própria dentista" fala do bastidor do site, não com a paciente
    ('Abaixo, os tratamentos já divulgados',
     'Veja abaixo os cuidados que a Dra. Marina realiza'),
    ('pela própria dentista.\n        </p>',
     'no consultório.\n        </p>'),

    # 5. Clareza: é a cor das coroas que acompanha o novo tom
    ('para que a cor final acompanhe o novo tom dos dentes.',
     'para que a cor das coroas acompanhe o novo tom dos dentes.'),

    # 6. Artigos faltando
    ('define\n                número de implantes, etapas e prazos.',
     'define\n                o número de implantes, as etapas e os prazos.'),

    # 7. Termos técnicos sem explicação (arco do cupido, comissuras)
    ('O objetivo é respeitar o desenho natural dos lábios e do rosto: volume adequado,',
     'O objetivo é respeitar o desenho natural dos lábios e do rosto, com volume na medida'),
    ('arco do cupido preservado e comissuras em proporção. A conversa anterior ao',
     'e contorno preservado. A conversa feita antes do procedimento alinha o que se'),
    ('procedimento define expectativas e limites de cada caso.',
     'espera do resultado e os limites de cada caso.'),

    # 8. Fecho mais claro
    ('conferindo o resultado junto com o paciente antes de finalizar.',
     'conferindo o resultado junto com o paciente antes da etapa final.'),

    # 9. Mesma questão do item 4, na seção de resultados
    ('Imagens reais, publicadas pela própria dentista com autorização dos pacientes.',
     'Casos reais, publicados com autorização dos pacientes.'),

    # 10. "entregue" é jargão de consultório
    ('Caso concluído e entregue no consultório, devolvendo forma e função ao sorriso.',
     'Tratamento concluído, devolvendo forma e função ao sorriso.'),

    # 11. Convite mais direto
    ('Quer saber se o seu caso tem indicação parecida?',
     'Quer saber se o seu caso tem indicação parecida? É só perguntar.'),
]

texto = io.open(CAMINHO, encoding='utf-8').read()

for antigo, novo in TROCAS:
    n = texto.count(antigo)
    if n != 1:
        raise SystemExit('ERRO: {} ocorrência(s) de: {!r}'.format(n, antigo[:60]))
    texto = texto.replace(antigo, novo)

io.open(CAMINHO, 'w', encoding='utf-8').write(texto)
print('{} trechos revisados'.format(len(TROCAS)))
