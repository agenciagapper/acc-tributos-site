"""Páginas de obrigado e Trabalhe conosco. Usado por build.py."""

ESPECIALIDADES = ["Contábil", "Fiscal", "Departamento pessoal", "Societário e processos", "Tributário", "Financeiro",
                  "Atendimento e relacionamento com clientes", "Comercial", "Certificado digital", "Administrativo", "Outra área"]
FORMACAO = ["Ensino médio completo", "Técnico em contabilidade", "Graduação em andamento", "Graduação completa",
            "Pós-graduação ou MBA", "Mestrado ou doutorado"]
EXPERIENCIA = ["Sem experiência ou só estágio", "Até 1 ano", "De 1 a 3 anos", "De 3 a 5 anos", "Mais de 5 anos"]


def opts(items, placeholder):
    return f'<option value="">{placeholder}</option>' + "".join(f"<option>{i}</option>" for i in items)


def obrigado_whatsapp():
    meta = {"slug": "/obrigado-whatsapp/", "type": "institucional", "nav": "Obrigado", "kicker": "Tudo certo", "noindex": True, "no_final": True,
            "title": "Abrindo o WhatsApp | ACC Tributos",
            "description": "Recebemos seu contato. Estamos abrindo a conversa com a equipe da ACC Tributos no WhatsApp.",
            "h1": "Obrigado! Abrindo o WhatsApp", "lead": ""}
    inner = """<section class="section ty" style="padding-top:var(--s-2)"><div class="wrap ty__box">
  <div class="ty__icon" aria-hidden="true"><svg width="34" height="34"><use href="#i-wa"/></svg></div>
  <p class="ty__big">Obrigado<span id="waNome"></span>. A conversa abre em <b id="waCount">3</b> segundos.</p>
  <p>Um contador da ACC Tributos responde por lá, de segunda a sexta, das 8h às 18h. Se a conversa não abrir sozinha, use o botão.</p>
  <a class="btn" id="waGo" data-direto href="https://wa.me/558587541948"><span class="wa-dot"><svg><use href="#i-wa"/></svg></span>Abrir o WhatsApp agora</a>
</div></section>"""
    return meta, inner


def obrigado_form():
    meta = {"slug": "/obrigado/", "type": "institucional", "nav": "Obrigado", "kicker": "Recebemos seus dados", "noindex": True, "no_final": True,
            "title": "Obrigado pelo contato | ACC Tributos",
            "description": "Recebemos seus dados. Estamos abrindo a conversa com um contador da ACC Tributos no WhatsApp.",
            "h1": "Obrigado, recebemos seus dados", "lead": ""}
    inner = """<section class="section ty" style="padding-top:var(--s-2)"><div class="wrap ty__box">
  <div class="ty__icon" aria-hidden="true"><svg width="34" height="34"><use href="#i-check"/></svg></div>
  <p class="ty__big">Tudo certo<span id="waNome"></span>. A conversa no WhatsApp abre em <b id="waCount">3</b> segundos.</p>
  <p>A mensagem já vai pronta com o assunto que você escolheu, é só enviar. Se a conversa não abrir sozinha, use o botão.</p>
  <a class="btn" id="waGo" data-direto href="https://wa.me/558587541948"><span class="wa-dot"><svg><use href="#i-wa"/></svg></span>Abrir o WhatsApp agora</a>
  <ol class="ty__steps">
    <li><b>Conversa no WhatsApp</b>Um contador responde de segunda a sexta, das 8h às 18h.</li>
    <li><b>Conversa de diagnóstico</b>Entendemos atividade, faturamento e funcionários da empresa.</li>
    <li><b>Proposta</b>Você recebe a proposta com o regime tributário mais adequado ao seu caso.</li>
  </ol>
  <p class="ty__small">Enquanto isso, veja <a href="/servicos/">nossos serviços</a> ou leia <a href="/blog/">o blog</a>.</p>
</div></section>"""
    return meta, inner


def trabalhe_conosco():
    meta = {"slug": "/trabalhe-conosco/", "type": "institucional", "nav": "Trabalhe conosco", "kicker": "Trabalhe conosco", "no_final": True,
            "title": "Trabalhe Conosco: Vagas em Contabilidade | ACC Tributos",
            "description": "Quer trabalhar com contabilidade em Fortaleza e região? Envie seu currículo para a ACC Tributos e diga sua área e sua formação.",
            "h1": "Trabalhe conosco na ACC Tributos",
            "lead": "Somos mais de 30 pessoas cuidando da contabilidade de empresas em Fortaleza e na Região Metropolitana. Se você gosta de resolver problema de cliente e de estudar legislação, mande seu currículo."}
    inner = f"""<section class="section" style="padding-top:var(--s-3)"><div class="wrap tc">
  <div class="tc__info">
    <figure class="tc__foto"><img src="/assets/img/escritorio-equipe.webp" width="1280" height="500" alt="Equipe da ACC Tributos no escritório" loading="lazy"></figure>
    <h2>Como é trabalhar aqui</h2>
    <ul class="ticks">
      <li><svg><use href="#i-check"/></svg><span>Equipe dividida por área: contábil, fiscal, departamento pessoal, societário, tributário e financeiro.</span></li>
      <li><svg><use href="#i-check"/></svg><span>Rotina forte de estudo, para acompanhar as mudanças de legislação, como a reforma tributária.</span></li>
      <li><svg><use href="#i-check"/></svg><span>Contato direto com os clientes: cada empresa tem um responsável que conhece o caso.</span></li>
      <li><svg><use href="#i-check"/></svg><span>Escritório no Edifício Business Place, em Maracanaú, e parte do Grupo ACC.</span></li>
    </ul>
    <p class="tc__note">Não temos vagas abertas o tempo todo. Guardamos os currículos recebidos e chamamos quando surge uma vaga que combina com o seu perfil.</p>
  </div>

  <form class="form tc__form" id="cvForm" novalidate>
    <h2>Envie seu currículo</h2>
    <div class="field"><label for="cv-nome-in">Nome completo</label><input id="cv-nome-in" name="nome" autocomplete="name" required><span class="err">Informe seu nome.</span></div>
    <div class="tc__row">
      <div class="field"><label for="cv-email">E-mail</label><input id="cv-email" name="email" type="email" autocomplete="email" required><span class="err">Confira o e-mail.</span></div>
      <div class="field"><label for="cv-tel">Telefone com DDD</label><input id="cv-tel" name="telefone" type="tel" inputmode="tel" autocomplete="tel" placeholder="(85) 9 0000-0000" required><span class="err">Confira o número, com DDD.</span></div>
    </div>
    <div class="tc__row">
      <div class="field"><label for="cv-esp">Especialidade</label><select id="cv-esp" name="especialidade" required>{opts(ESPECIALIDADES, "Escolha a área")}</select><span class="err">Escolha uma área.</span></div>
      <div class="field"><label for="cv-form">Nível de formação</label><select id="cv-form" name="formacao" required>{opts(FORMACAO, "Escolha o nível")}</select><span class="err">Escolha seu nível de formação.</span></div>
    </div>
    <div class="tc__row">
      <div class="field"><label for="cv-curso">Curso <span class="opt">(opcional)</span></label><input id="cv-curso" name="curso" placeholder="Ex.: Ciências Contábeis"></div>
      <div class="field"><label for="cv-exp">Experiência na área</label><select id="cv-exp" name="experiencia">{opts(EXPERIENCIA, "Escolha")}</select></div>
    </div>
    <div class="tc__row">
      <div class="field"><label for="cv-crc">Registro no CRC</label><select id="cv-crc" name="crc"><option value="">Escolha</option><option>Sim, ativo</option><option>Em andamento</option><option>Não tenho</option></select></div>
      <div class="field"><label for="cv-in">LinkedIn <span class="opt">(opcional)</span></label><input id="cv-in" name="linkedin" type="url" placeholder="linkedin.com/in/seunome"></div>
    </div>
    <div class="field">
      <span class="lbl-like" id="cv-lbl">Currículo</span>
      <label class="file" for="cv-file"><svg width="20" height="20"><use href="#i-arrow"/></svg><span><b>Escolher arquivo</b><span id="cv-nome">PDF, DOC ou DOCX, até 5 MB</span></span></label>
      <input id="cv-file" name="curriculo" type="file" accept=".pdf,.doc,.docx,application/pdf,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document" required aria-labelledby="cv-lbl">
      <span class="err">Envie o currículo em PDF, DOC ou DOCX, com até 5 MB.</span>
    </div>
    <div class="field"><label for="cv-msg">Algo que queira contar <span class="opt">(opcional)</span></label><textarea id="cv-msg" name="mensagem" rows="3"></textarea></div>
    <div class="field check"><input id="cv-lgpd" name="lgpd" type="checkbox" value="sim" required><label for="cv-lgpd">Autorizo a ACC Tributos a guardar meu currículo para processos seletivos, conforme a <a href="/politica-de-privacidade/">política de privacidade</a>.</label><span class="err">Precisamos da sua autorização para guardar o currículo.</span></div>
    <input type="text" name="empresa_site" tabindex="-1" autocomplete="off" class="hp" aria-hidden="true">
    <button class="btn" type="submit"><span class="lbl">Enviar currículo</span><svg width="18" height="18"><use href="#i-arrow"/></svg></button>
  </form>
</div></section>"""
    return meta, inner


def obrigado_cv():
    meta = {"slug": "/trabalhe-conosco/obrigado/", "type": "institucional", "nav": "Currículo enviado", "kicker": "Trabalhe conosco", "noindex": True, "no_final": True,
            "title": "Currículo enviado | ACC Tributos",
            "description": "Recebemos seu currículo. Se o seu perfil combinar com uma vaga, a equipe da ACC Tributos entra em contato.",
            "h1": "Currículo recebido", "lead": ""}
    inner = """<section class="section ty" style="padding-top:var(--s-2)"><div class="wrap ty__box">
  <div class="ty__icon" aria-hidden="true"><svg width="34" height="34"><use href="#i-check"/></svg></div>
  <p class="ty__big">Obrigado por querer fazer parte da equipe.</p>
  <p>Guardamos seu currículo. Quando surgir uma vaga que combine com a sua área e a sua formação, entramos em contato pelo e-mail ou telefone que você informou.</p>
  <p class="ty__small"><a href="/quem-somos/">Conheça mais sobre a ACC Tributos</a></p>
</div></section>"""
    return meta, inner


ALL = [obrigado_whatsapp, obrigado_form, trabalhe_conosco, obrigado_cv]
