# Brief de conteúdo · site ACC Tributos

Você escreve o conteúdo das páginas internas do novo site da ACC Tributos Contabilidade. Cada página vira um arquivo JSON em `content/` (um arquivo por página). Um gerador em Python transforma o JSON em HTML; você NÃO escreve HTML.

## Objetivo
Captar leads orgânicos (Google) de empresas e pessoas físicas em **Fortaleza e Região Metropolitana** (Maracanaú, Eusébio, Aquiraz). CTA principal: WhatsApp. Cada página precisa responder a intenção de busca melhor que os concorrentes (Contabilizei, Conta Azul, escritórios locais).

## Fatos da empresa (use só estes; não invente outros)
- Nome: ACC Tributos Assessoria e Consultoria Contábil ("ACC Tributos"). Faz parte do **Grupo ACC**, que também tem: ACC Gestão (gestão financeira/BPO), **Prime Certificação** (certificado digital), **Regularize Marcas** (registro de marca no INPI).
- 6 anos de escritório. +30 colaboradores. +1.000 clientes atendidos. +1.200 empresas abertas.
- Nota **4,8 no Google com 199 avaliações**.
- Sócios: **Joel Mendonça** (contador, CRC/CE 25911, MBA em Direito Tributário, 12 anos como assessor e consultor, professor de gestão financeira e empresarial) e **Alyson Xavier** (contador, CRC/CE 27954).
- Escritório: Edifício Business Place, Torre I, Sala 1103, Av. Yolanda Pontes Vidal Queiroz, 57, Jereissati I, Maracanaú, CE, CEP 61900-410. Atende presencialmente ou 100% online (WhatsApp, videochamada, plataforma).
- Horário: segunda a sexta, 8h às 18h. Telefone (85) 3371-0502. WhatsApp (85) 99825-0357.
- Abertura de empresa: CNPJ, contrato social e inscrições municipal e estadual (quando obrigatórias) em **até 24 horas** após receber os documentos. Custo de abertura de **R$ 500 a R$ 1.200**, conforme contrato social, porte e modelo societário. Licenças e alvarás à parte (dependem da prefeitura e atividade).
- Mensalidade: NÃO cite valores. Diga que depende de regime, faturamento, funcionários e plano, e que a proposta é enviada pelo WhatsApp.
- Troca de contador: a ACC pede ao escritório anterior documentação e acessos, revisa a situação fiscal e assume as obrigações; o cliente não precisa intermediar.
- Atendimento: contador dedicado que conhece a empresa pelo nome; WhatsApp respondido pelo time contábil (não robô); guias enviadas com antecedência e conferidas.
- Serviços (URL · resumo):
  - `/servicos/legalizacao-de-empresas/` Abertura e legalização de empresas: abertura, alteração contratual, baixa, regularização, licenças.
  - `/servicos/contabilidade-empresarial/` Contabilidade empresarial: registros, balanço, demonstrativos, obrigações acessórias.
  - `/servicos/planejamento-tributario/` Planejamento tributário: comparar Simples Nacional, Lucro Presumido e Lucro Real para pagar menos dentro da lei.
  - `/servicos/departamento-pessoal/` Departamento pessoal: folha, admissões, férias, 13º, rescisões, eSocial.
  - `/servicos/imposto-de-renda/` Imposto de Renda pessoa física: declaração, sócios, autônomos, profissionais liberais, malha fina, declarações atrasadas.
  - `/servicos/escrituracao-fiscal/` Escrituração fiscal: notas de entrada e saída, SPED, apurações.
  - `/servicos/auditoria-fiscal-digital/` Auditoria fiscal digital: cruzar o que o Fisco já sabe, identificar riscos e créditos.
  - `/servicos/calculos/` Cálculos: trabalhistas, judiciais, extrajudiciais, multas.
  - `/servicos/certificado-digital/` Certificado digital: e-CNPJ e e-CPF, emitidos com a Prime Certificação (Grupo ACC).
  - `/servicos/registro-de-marca/` Registro de marca no INPI com a Regularize Marcas (Grupo ACC): pesquisa de viabilidade e registro.
- Regiões: `/contabilidade-em-fortaleza/`, `/contabilidade-em-maracanau/`, `/contabilidade-em-eusebio/`, `/contabilidade-em-aquiraz/`.
- Outras páginas: `/trocar-de-contador/`, `/quem-somos/`, `/contato/`, `/blog/`, `/politica-de-privacidade/`.

## Regras de escrita (obrigatórias)
- Português do Brasil, com acentuação correta. Tom: claro, direto, próximo, de quem entende de contabilidade e fala com dono de pequena e média empresa. Frases curtas. Nada de juridiquês.
- **Proibido travessão (— ou –)** em qualquer texto. Use vírgula, ponto ou dois-pontos.
- Proibido clichê de IA: "no mundo atual", "cenário cada vez mais", "não é apenas X, é Y", "descubra como", "potencialize", "alavancar", "jornada", "solução completa e inovadora", "seu parceiro ideal", emojis.
- **Não invente números, percentuais, alíquotas, prazos legais, valores de multas, limites de faturamento, estatísticas ou depoimentos.** Se um dado legal mudar com frequência (limite do MEI, alíquotas, faixas do Simples, datas de entrega do IR), fale de forma geral ("dentro do limite de faturamento vigente", "no prazo definido pela Receita a cada ano").
- Não invente nomes de clientes, casos ou endereços de órgãos públicos. Pode citar órgãos de forma genérica e correta (Receita Federal, Junta Comercial do Ceará (Jucec), prefeitura do município, Sefaz-CE, INPI, eSocial).
- Palavra-chave principal no H1, no title, na description e nas primeiras 100 palavras; variações naturais no corpo. Sem repetir a palavra-chave de forma forçada.
- Cada página: 600 a 1.000 palavras somando lead + seções + FAQ.

## Formato do JSON (um arquivo por página: `content/<nome>.json`, UTF-8)
```json
{
  "slug": "/servicos/planejamento-tributario/",
  "type": "servico",                     // "servico" | "regiao" | "institucional"
  "nav": "Planejamento tributário",      // nome curto para menus e breadcrumb
  "title": "Planejamento Tributário em Fortaleza | ACC Tributos",   // 50 a 60 caracteres
  "description": "140 a 160 caracteres, benefício + chamada",
  "keyword": "planejamento tributário em Fortaleza",
  "kicker": "Serviço",                   // rótulo curto acima do H1
  "h1": "Planejamento tributário em Fortaleza para pagar menos imposto dentro da lei",
  "lead": "2 a 3 frases que respondem a busca e contêm a palavra-chave.",
  "wa_text": "Mensagem pré-preenchida do WhatsApp, em primeira pessoa do cliente.",
  "highlights": ["3 a 4 bullets curtos de benefício, até 60 caracteres cada"],
  "sections": [
    {"h2": "Título com variação da palavra-chave", "paragraphs": ["..."], "bullets": ["opcional"]}
  ],                                      // 3 a 5 seções
  "steps": [{"title": "...", "text": "..."}],   // opcional, 3 passos de como funciona
  "faq": [{"q": "Pergunta real de quem busca", "a": "Resposta direta em 2 a 4 frases"}],  // 4 a 6
  "related": ["/servicos/...", "/servicos/...", "/contabilidade-em-fortaleza/"]          // 3 URLs internas
}
```
Campos extras só para `type: "regiao"`:
```json
  "city": "Fortaleza",
  "areas": ["bairros ou localidades reais e conhecidas da cidade, 6 a 10"],
  "local_notes": ["2 a 4 observações locais verdadeiras e genéricas, ex.: inscrição municipal e alvará são feitos na prefeitura do município; perfil econômico conhecido da cidade"]
```
Valide cada arquivo com `python -I -c "import json,sys;json.load(open(sys.argv[1],encoding='utf-8'))" <arquivo>` antes de terminar.
