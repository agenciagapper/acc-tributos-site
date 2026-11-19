# Site ACC Tributos Contabilidade

Novo site de **acctributos.com.br**: contabilidade em Fortaleza e Região Metropolitana, focado em SEO local e captação de leads (WhatsApp e formulário).

Site estático (HTML, CSS e JS puros), gerado por um script Python a partir de arquivos de conteúdo. Não depende de framework nem de banco de dados.

## Estrutura

| Caminho | O que é |
|---|---|
| `index.html` | Home. **Fonte do topo, rodapé e bloco de contato** de todas as outras páginas. |
| `content/*.json` | Conteúdo das páginas de serviço, cidade e institucionais (formato em `content/_brief.md`). |
| `content/posts/*.json` | Artigos do blog (formato em `content/_brief-blog.md`). `"revisado": false` deixa o artigo com noindex e fora do sitemap. |
| `build.py` | Gera todas as páginas internas, `sitemap.xml` e `404.html`. |
| `quem_somos.py`, `pages_extra.py` | Layouts próprios do Quem somos, Trabalhe conosco e páginas de obrigado. |
| `check_seo.py` | Confere títulos, descrições, H1, dados estruturados, travessões e links internos. |
| `assets/` | CSS, JS, imagens e logos usados pelo site. |
| `api/form.php` | Receptor dos formulários (precisa de PHP na hospedagem). |
| `_material/` | Imagens originais e não usadas. **Não publicar.** |
| `arquitetura-seo.md` | Mapa de páginas e palavras-chave, migração do site antigo e pendências de lançamento. |
| `revisao-artigos.md` | Roteiro de revisão dos artigos do blog. |

As pastas de páginas (`servicos/`, `blog/`, `contabilidade-em-*/` etc.) são **geradas**: edite o JSON correspondente e rode o build, não o HTML.

## Como trabalhar

```bash
python build.py        # gera as páginas a partir de content/
python check_seo.py    # confere SEO e links internos
python -m http.server 5173   # visualizar em http://localhost:5173
```

Mudou CSS ou JS? Suba o número de versão (`site.css?v=`, `site.js?v=`, `forms.js?v=`) no `index.html` e rode o build, para o navegador não usar a versão antiga em cache.

## Formulários e origem dos leads

- Todo link de WhatsApp abre uma janela pedindo nome e telefone, envia para `api/form.php` e segue para `/obrigado-whatsapp/`, que abre o WhatsApp com a mensagem pronta.
- O formulário de proposta vai para `/obrigado/`; o Trabalhe conosco (com currículo) vai para `/trabalhe-conosco/obrigado/`.
- Cada envio leva a origem completa: último toque (`utm_source`, `utm_medium`, `utm_campaign`, `utm_term`, `utm_content`, `utm_id`, `landing_page`, `referrer`), primeiro toque (`primeiro_*`, guardado por 90 dias), IDs de clique (`gclid`, `gbraid`, `wbraid`, `fbclid`, `msclkid`, `ttclid`) e `fbp`, `fbc`, `ga_client_id` para integrações futuras.
- `api/form.php` grava `api/data/leads.csv`, `api/data/curriculos.csv` e os currículos em `api/data/curriculos/` (pasta bloqueada ao público e fora do git) e avisa por e-mail. **Configure os e-mails no topo do arquivo antes de publicar.**
- Para mandar os dados a um CRM ou webhook, defina `window.ACC_FORM_ENDPOINT` antes de carregar `assets/js/forms.js`.
- Eventos no `dataLayer`: `generate_lead` (campo `canal`: `whatsapp` ou `formulario`), `whatsapp_modal_open`, `curriculo_enviado`, `whatsapp_click`, `phone_click`.

## Publicação

Ver a seção 5 de `arquitetura-seo.md`. Resumo: configurar e-mails do `api/form.php`, `ErrorDocument 404 /404.html`, redirecionamentos 301 do site antigo, GA4/Ads/Pixel, atualizar o Google Business Profile com o endereço e telefones do site, enviar o sitemap no Search Console.
