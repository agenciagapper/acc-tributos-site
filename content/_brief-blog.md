# Brief de artigos do blog · ACC Tributos

Leia também `content/_brief.md` (fatos da empresa e regras de escrita). Tudo de lá vale aqui, especialmente: **não inventar números, alíquotas, prazos, valores de multa, limites, estatísticas ou depoimentos**; sem travessão (— ou –); sem clichês de IA; português do Brasil correto.

## Diferença dos artigos
Artigos respondem a uma dúvida de quem busca no Google (topo e meio de funil) e levam para uma página de serviço. Tom: um contador experiente explicando para um dono de pequena empresa, com exemplos concretos do dia a dia. Nada de vender no meio do texto; a chamada para a ACC fica só no fim, em um parágrafo.

## Pesquisa e fontes (obrigatório)
- Use WebSearch/WebFetch para checar regras, procedimentos e nomes de órgãos/sistemas antes de afirmar. Prefira fontes oficiais: gov.br, Receita Federal, Portal do Empreendedor, Sefaz-CE, Jucec, prefeituras (fortaleza.ce.gov.br, maracanau.ce.gov.br, eusebio.ce.gov.br, aquiraz.ce.gov.br), INPI, eSocial, Planalto (leis).
- Se não conseguir confirmar um detalhe local (nome do sistema da prefeitura, documento exigido, prazo), escreva de forma geral ("pelo sistema de licenciamento da prefeitura", "a prefeitura informa os documentos exigidos para cada atividade") em vez de chutar.
- Coloque de 2 a 5 fontes consultadas no campo `fontes`.
- Datas: hoje é novembro de 2026. Cuidado com regras que mudaram (Reforma Tributária: Lei Complementar 214/2025, CBS e IBS em fase de testes a partir de 2026). Se citar, confirme na fonte.

## Formato: um arquivo por artigo em `content/posts/<slug>.json` (UTF-8)
```json
{
  "slug": "/blog/como-abrir-empresa-em-fortaleza/",
  "type": "post",
  "categoria": "Abertura de empresa",          // uma de: Abertura de empresa, Impostos e tributação, Departamento pessoal, Imposto de Renda, Gestão e rotina contábil, Certificado e marca, Notícias e legislação
  "nav": "Como abrir empresa em Fortaleza",   // título curto
  "title": "Como Abrir Empresa em Fortaleza em 2026 | ACC Tributos",   // 45 a 60 caracteres
  "h1": "Como abrir empresa em Fortaleza: passo a passo, documentos e custos",
  "description": "140 a 160 caracteres, responde a busca e chama para ler",
  "keyword": "abrir empresa em Fortaleza",
  "date": "2026-11-19",
  "modified": "2026-11-19",
  "revisado": false,
  "servico": "/servicos/legalizacao-de-empresas/",   // página de serviço mais ligada ao tema
  "related_posts": [],                                 // deixe vazio; o gerador preenche
  "fontes": [{"titulo": "Portal do Empreendedor (gov.br)", "url": "https://..."}],
  "body": "<p>...</p><h2>...</h2><p>...</p><ul><li>...</li></ul>"
}
```
Regras do `body`:
- HTML simples, só estas tags: p, h2, h3, ul, ol, li, strong, em, a, table, thead, tbody, tr, th, td. Sem classes, sem estilos, sem h1.
- 900 a 1.400 palavras. Primeiro parágrafo responde a pergunta em 2 a 3 frases e contém a palavra-chave.
- 4 a 7 H2 em forma de pergunta ou tarefa ("Quanto custa...", "Quais documentos...").
- Pelo menos 2 links internos com âncora descritiva: para a página de serviço (`servico`) e para uma página de cidade ou outro serviço (URLs da lista do `_brief.md`). Links externos só para fontes oficiais.
- Uma seção "Perguntas frequentes" no fim como H2, com 3 perguntas em H3 e respostas curtas.
- Último parágrafo: chamada simples para falar com a ACC pelo WhatsApp, sem exagero.

Valide cada arquivo: `python -I -c "import json,sys;json.load(open(sys.argv[1],encoding='utf-8'))" <arquivo>`.
Confira que não há travessão: o texto não pode conter os caracteres — nem –.
