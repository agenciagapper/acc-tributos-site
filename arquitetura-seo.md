# ACC Tributos · Arquitetura SEO do novo site

Objetivo: captar leads orgânicos (WhatsApp e formulário) de empresas e pessoas físicas em Fortaleza, Maracanaú, Eusébio e Aquiraz.
Canônico: `https://acctributos.com.br/` (https, sem www, com barra final).

## 1. Mapa de páginas e palavras-chave

| URL | Palavra-chave principal | Intenção | Tipo |
|---|---|---|---|
| `/` | contabilidade em Fortaleza e Maracanaú / escritório de contabilidade | Comercial | Home |
| `/servicos/` | serviços de contabilidade | Navegação | Hub |
| `/servicos/legalizacao-de-empresas/` | abrir empresa / abertura de empresa Fortaleza | Transacional | Serviço |
| `/servicos/contabilidade-empresarial/` | contabilidade empresarial | Comercial | Serviço |
| `/servicos/planejamento-tributario/` | planejamento tributário | Comercial | Serviço |
| `/servicos/departamento-pessoal/` | departamento pessoal terceirizado | Comercial | Serviço |
| `/servicos/escrituracao-fiscal/` | escrituração fiscal | Comercial | Serviço |
| `/servicos/auditoria-fiscal-digital/` | auditoria fiscal | Comercial | Serviço |
| `/servicos/imposto-de-renda/` (NOVA) | declaração de imposto de renda Fortaleza | Transacional, sazonal (mar a mai) | Serviço |
| `/servicos/calculos/` | cálculos trabalhistas / cálculos judiciais | Transacional | Serviço |
| `/servicos/certificado-digital/` (NOVA) | certificado digital Fortaleza / e-CNPJ | Transacional | Serviço |
| `/servicos/registro-de-marca/` (NOVA) | registro de marca Fortaleza / INPI | Transacional | Serviço |
| `/trocar-de-contador/` (NOVA) | trocar de contador | Transacional | Landing |
| `/contabilidade-em-fortaleza/` (NOVA) | contabilidade em Fortaleza | Local | Região |
| `/contabilidade-em-maracanau/` (NOVA) | contabilidade em Maracanaú | Local | Região |
| `/contabilidade-em-eusebio/` (NOVA) | contabilidade no Eusébio | Local | Região |
| `/contabilidade-em-aquiraz/` (NOVA) | contabilidade em Aquiraz | Local | Região |
| `/quem-somos/` | ACC Tributos (marca, E-E-A-T) | Navegação | Institucional |
| `/blog/` + posts | dúvidas de MEI, Simples, IR, DP | Informacional | Blog |
| `/contato/` | contato contabilidade Maracanaú | Navegação | Contato |
| `/obrigado/` | (noindex) | | Conversão |
| `/politica-de-privacidade/` | (legal) | | Legal |

### Fase 2: páginas serviço × região (só depois das 4 regiões indexarem)
Combinar os 3 serviços de maior volume com as 4 cidades, com conteúdo local real (prefeitura, ISS, alvará, bairros):
`/abrir-empresa-em-fortaleza/`, `/abrir-empresa-em-maracanau/`, `/imposto-de-renda-em-fortaleza/` etc. Nada de página clonada trocando só o nome da cidade: o Google trata como conteúdo raso.

## 2. O que cada página de região precisa ter
- H1 "Contabilidade em {Cidade}", NAP do escritório, distância/tempo até o Business Place.
- Particularidades locais: ISS, alvará e inscrição municipal da prefeitura, polos econômicos (Distrito Industrial de Maracanaú, Aldeota/Centro em Fortaleza, Eusébio e Aquiraz com comércio e turismo).
- Depoimento de cliente da cidade (ex.: RA Criações, Maracanaú).
- FAQ local + schema `AccountingService` com `areaServed` da cidade + `BreadcrumbList`.

## 3. Migração do site atual (WordPress)
URLs de serviço **mantidas iguais** (`/servicos/...`): sem perda.
| URL antiga | Destino (301) |
|---|---|
| `/vem-ser-cliente/` | `/contato/` |
| `/abertura-empresa/` | `/servicos/legalizacao-de-empresas/` |
| `/reduza-impostos/` | `/servicos/planejamento-tributario/` |
| `/assessoria-contabil/` | `/servicos/contabilidade-empresarial/` |
| `/quem-somos/` | mantém |
| 11 posts na raiz (`/capital-social-do-mei/` etc.) | mantidos na raiz, mesma URL (sem redirecionamento) |
| `/category/*`, `/tag/*`, `/author/*`, `/depoimentos/*` | 301 para `/blog/` ou 410 se sem tráfego |

Antes de publicar: exportar páginas com cliques do Search Console e conferir uma por uma.

## 4. Base técnica (todas as páginas)
- Site estático (HTML gerado no servidor, sem SPA). Sugestão: Astro.
- Title 50 a 60 caracteres, description 140 a 160, canonical, Open Graph.
- Schema global: `AccountingService` (LocalBusiness) com endereço, geo, telefone, horário, `areaServed`, `sameAs`; `WebSite`.
- Google Business Profile com o mesmo NAP do rodapé (crítico para o pacote local).
- GA4 + eventos: clique no WhatsApp, clique no telefone, envio de formulário. UTM e gclid guardados até o envio.

## 5. Auditoria da home (2026-11-19) e pendências de lançamento

Já resolvido na home:
- Title 50 caracteres com "Contabilidade em Fortaleza" no início; description 157; canonical; 1 H1 com a palavra-chave; palavra-chave nas primeiras 100 palavras.
- 41 imagens com alt, width e height; hero com fetchpriority; demais com lazy.
- JSON-LD válido: AccountingService (endereço, geo, hasMap, áreas atendidas, catálogo com os 10 serviços), WebSite, FAQPage.
- Imagem de compartilhamento 1200x630 (`assets/og/home.jpg`), favicon e apple-touch-icon, robots.txt.
- Imagens otimizadas: logos de ~500 KB para ~30 KB; fotos da equipe e diorama reduzidos à metade.

Pendente antes de publicar:
- [x] NAP oficial = o do site (Av. Yolanda Pontes Vidal Queiroz, 57 · (85) 3371-0502 · WhatsApp (85) 99825-0357). [ ] **Atualizar o Google Business Profile**, que ainda mostra "Avenida I" e (85) 98754-1948.
- [x] Horário seg a sex, 8h às 18h, no site e no schema.
- [x] 31 páginas internas geradas por `build.py` a partir de `content/*.json` (10 serviços, 4 regiões, trocar de contador, quem somos, contato, índice de serviços, blog, 11 artigos migrados, política de privacidade).
- [x] `sitemap.xml` (32 URLs) e `404.html` gerados. [ ] No servidor: `ErrorDocument 404 /404.html` (status 404 real).
- [ ] Hospedar as fontes no próprio servidor (WOFF2) em vez do Google Fonts.
- [ ] Instalar GA4 + Google Ads/Pixel (o site já envia eventos `whatsapp_click`, `phone_click` e `generate_lead` para o dataLayer).
- [x] Todo clique de WhatsApp pede nome e telefone, envia o contato e passa por `/obrigado-whatsapp/`, que abre o WhatsApp. Formulário de proposta vai para `/obrigado/`. Trabalhe conosco (`/trabalhe-conosco/`) envia currículo e vai para `/trabalhe-conosco/obrigado/`. Páginas de obrigado com noindex.
- [ ] **Receptor `api/form.php`:** configurar `EMAIL_LEADS`, `EMAIL_RH` e `EMAIL_FROM` no topo do arquivo e testar na hospedagem (precisa de PHP). Ele grava `api/data/leads.csv`, `api/data/curriculos.csv` e os arquivos em `api/data/curriculos/` (pasta bloqueada ao público) e manda aviso por e-mail. Para usar um CRM ou webhook no lugar, definir `window.ACC_FORM_ENDPOINT` antes de `forms.js`.
- [ ] No GA4/Ads/Pixel, marcar como conversão o evento `generate_lead` (campo `canal`: whatsapp ou formulario) ou a visita às páginas de obrigado.
- [x] Versão clara aprovada; alternador removido. (As regras da versão escura seguem no CSS como base do tema claro.)
- [ ] Redirecionamentos 301 da seção 3 testados um a um.
- [ ] PageSpeed mobile verde e Rich Results Test aprovado no domínio final.

Como regenerar as páginas: editar `content/*.json` (ou `content/posts/*.json`) e rodar `python build.py`; depois `python check_seo.py` confere títulos, descrições, H1, JSON-LD, travessões e links internos.

Conteúdo a fortalecer depois: os 11 artigos migrados são curtos (164 a 896 palavras de texto) e sem autor; vale reescrever os de maior busca (IR, MEI, regime tributário) com mais profundidade e assinatura de um dos contadores.
