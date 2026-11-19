<?php
/**
 * Receptor dos formulários do site ACC Tributos.
 * Recebe: contato do WhatsApp, formulário de proposta e currículos (Trabalhe conosco).
 * Guarda em api/data/ (bloqueado para acesso público) e avisa por e-mail.
 *
 * CONFIGURAR ANTES DE PUBLICAR: os e-mails abaixo.
 */
const EMAIL_LEADS = 'CONFIGURAR@acctributos.com.br';      // recebe contatos de WhatsApp e do formulário
const EMAIL_RH    = 'CONFIGURAR@acctributos.com.br';      // recebe avisos de currículo
const EMAIL_FROM  = 'site@acctributos.com.br';            // remetente (precisa existir no domínio)
const MAX_CV      = 5 * 1024 * 1024;                      // 5 MB

header('Content-Type: application/json; charset=utf-8');
header('X-Robots-Tag: noindex, nofollow');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') { http_response_code(405); exit('{"ok":false}'); }

// aceita só envios do próprio site
$host = $_SERVER['HTTP_HOST'] ?? '';
$ref  = parse_url($_SERVER['HTTP_ORIGIN'] ?? ($_SERVER['HTTP_REFERER'] ?? ''), PHP_URL_HOST);
if ($ref && $host && strcasecmp($ref, $host) !== 0) { http_response_code(403); exit('{"ok":false}'); }

// robô preencheu o campo escondido: finge sucesso e descarta
if (!empty($_POST['empresa_site'])) { exit('{"ok":true}'); }

function campo($k, $max = 300) {
    $v = trim((string)($_POST[$k] ?? ''));
    $v = preg_replace('/[\r\n\t]+/', ' ', $v);
    return mb_substr(strip_tags($v), 0, $max);
}

$tipo = campo('tipo', 20);
if (!in_array($tipo, ['whatsapp', 'formulario', 'curriculo'], true)) { http_response_code(400); exit('{"ok":false}'); }

$dados = [
    'data'          => date('Y-m-d H:i:s'),
    'tipo'          => $tipo,
    'nome'          => campo('nome', 120),
    'telefone'      => campo('telefone', 30) ?: campo('whatsapp', 30),
    'email'         => campo('email', 160),
    'assunto'       => campo('assunto', 120),
    'mensagem'      => campo('mensagem', 1500),
    'especialidade' => campo('especialidade', 80),
    'formacao'      => campo('formacao', 80),
    'curso'         => campo('curso', 120),
    'experiencia'   => campo('experiencia', 60),
    'crc'           => campo('crc', 40),
    'linkedin'      => campo('linkedin', 200),
    'pagina'        => campo('pagina', 200),
    'origem'        => campo('origem', 200),
    'arquivo'       => '',
];

// origem do contato: último toque (utm_*), primeiro toque (primeiro_*), IDs de clique e identificadores de mídia
$atribuicao = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'utm_id',
               'landing_page', 'referrer', 'ultimo_toque_em',
               'primeiro_source', 'primeiro_medium', 'primeiro_campaign', 'primeiro_term', 'primeiro_content',
               'primeiro_landing', 'primeiro_referrer', 'primeiro_toque_em',
               'gclid', 'gbraid', 'wbraid', 'fbclid', 'msclkid', 'ttclid', 'fbp', 'fbc', 'ga_client_id'];
foreach ($atribuicao as $k) { $dados[$k] = campo($k, 300); }

$digitos = preg_replace('/\D/', '', $dados['telefone']);
if ($dados['nome'] === '' || strlen($digitos) < 10 || strlen($digitos) > 13) { http_response_code(422); exit('{"ok":false,"erro":"dados"}'); }
if ($dados['email'] !== '' && !filter_var($dados['email'], FILTER_VALIDATE_EMAIL)) { http_response_code(422); exit('{"ok":false,"erro":"email"}'); }

$base = __DIR__ . '/data';
if (!is_dir($base)) { mkdir($base, 0750, true); }
if (!file_exists("$base/.htaccess")) { file_put_contents("$base/.htaccess", "Require all denied\nDeny from all\n"); }

// currículo
if ($tipo === 'curriculo') {
    if ($dados['email'] === '' || empty($_FILES['curriculo']) || $_FILES['curriculo']['error'] !== UPLOAD_ERR_OK) {
        http_response_code(422); exit('{"ok":false,"erro":"arquivo"}');
    }
    $f = $_FILES['curriculo'];
    $ext = strtolower(pathinfo($f['name'], PATHINFO_EXTENSION));
    $mimes = ['pdf' => 'application/pdf', 'doc' => 'application/msword',
              'docx' => 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    $mime = function_exists('finfo_open') ? finfo_file(finfo_open(FILEINFO_MIME_TYPE), $f['tmp_name']) : '';
    $mimeOk = !$mime || in_array($mime, array_merge(array_values($mimes), ['application/zip', 'application/octet-stream']), true);
    if (!isset($mimes[$ext]) || !$mimeOk || $f['size'] > MAX_CV) { http_response_code(422); exit('{"ok":false,"erro":"arquivo"}'); }
    $dir = "$base/curriculos";
    if (!is_dir($dir)) { mkdir($dir, 0750, true); }
    $nomeArq = date('Ymd-His') . '-' . bin2hex(random_bytes(4)) . '.' . $ext;
    if (!move_uploaded_file($f['tmp_name'], "$dir/$nomeArq")) { http_response_code(500); exit('{"ok":false}'); }
    $dados['arquivo'] = "curriculos/$nomeArq";
}

// planilha (CSV abre no Excel)
$csv = "$base/" . ($tipo === 'curriculo' ? 'curriculos.csv' : 'leads.csv');
$novo = !file_exists($csv);
$fh = fopen($csv, 'a');
if ($fh) {
    flock($fh, LOCK_EX);
    if ($novo) { fwrite($fh, "\xEF\xBB\xBF"); fputcsv($fh, array_keys($dados), ';'); }
    fputcsv($fh, array_values($dados), ';');
    flock($fh, LOCK_UN);
    fclose($fh);
}

// aviso por e-mail
$para = $tipo === 'curriculo' ? EMAIL_RH : EMAIL_LEADS;
if (strpos($para, 'CONFIGURAR') === false) {
    $titulos = ['whatsapp' => 'Novo contato pelo WhatsApp', 'formulario' => 'Novo pedido de proposta', 'curriculo' => 'Novo currículo recebido'];
    $corpo = '';
    foreach ($dados as $k => $v) { if ($v !== '') { $corpo .= ucfirst($k) . ': ' . $v . "\n"; } }
    $assunto = '=?UTF-8?B?' . base64_encode($titulos[$tipo] . ' · ' . $dados['nome']) . '?=';
    $cab = "From: Site ACC Tributos <" . EMAIL_FROM . ">\r\nContent-Type: text/plain; charset=UTF-8\r\n";
    if ($dados['email'] !== '') { $cab .= "Reply-To: " . $dados['email'] . "\r\n"; }
    @mail($para, $assunto, $corpo, $cab);
}

echo '{"ok":true}';
