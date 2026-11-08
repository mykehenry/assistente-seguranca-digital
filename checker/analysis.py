"""Regras locais e determinísticas. Nenhuma URL é acessada."""

import ipaddress
import re
from dataclasses import dataclass
from urllib.parse import urlsplit


URL_RE = re.compile(r"https?://[^\s<>\"']+", re.IGNORECASE)
BARE_URL_RE = re.compile(r"\b(?:[a-z0-9-]+\.)+[a-z]{2,}(?:/[^\s<>\"']*)?", re.IGNORECASE)
SUSPICIOUS_TLDS = {"zip", "mov", "top", "click", "work", "xyz"}
URGENT = re.compile(r"\b(?:urgente|imediat[oa]|agora|última chance|ultima chance|24 horas|bloquead[oa]|suspens[oa])\b", re.I)
SECRET = re.compile(r"\b(?:senha|código de verificação|codigo de verificacao|token|dados bancários|dados bancarios|cpf)\b", re.I)
PAYMENT = re.compile(r"\b(?:pix|boleto|pagamento|transferência|transferencia)\b", re.I)


@dataclass(frozen=True)
class Finding:
    title: str
    explanation: str
    points: int


@dataclass(frozen=True)
class Result:
    level: str
    summary: str
    findings: tuple[Finding, ...]
    advice: tuple[str, ...]
    urls_found: int


def _urls(text: str) -> list[str]:
    explicit = [match.rstrip(".,;:!?)]}") for match in URL_RE.findall(text)]
    if explicit:
        return explicit[:5]
    return ["https://" + match.rstrip(".,;:!?)]}") for match in BARE_URL_RE.findall(text)[:5]]


def analyze(text: str) -> Result:
    """Analyze up to 1,000 characters without network, persistence or external services."""
    if not isinstance(text, str) or not text.strip() or len(text) > 1000:
        raise ValueError("Informe um texto de até 1.000 caracteres.")

    findings: list[Finding] = []
    urls = _urls(text)
    if URGENT.search(text):
        findings.append(Finding("Pressão para agir rápido", "A mensagem usa termos de urgência ou ameaça de bloqueio.", 2))
    if SECRET.search(text):
        findings.append(Finding("Pedido de informação sensível", "Há menção a senha, código ou dado pessoal. Confirme o pedido por outro canal.", 3))
    if PAYMENT.search(text):
        findings.append(Finding("Pedido ou assunto financeiro", "Há menção a pagamento ou transferência. Confira o destinatário no canal oficial.", 2))

    for raw in urls:
        try:
            parsed = urlsplit(raw)
            hostname = parsed.hostname or ""
            port = parsed.port
        except ValueError:
            findings.append(Finding("Endereço malformado", "O endereço não pôde ser interpretado com segurança.", 3))
            continue
        if not hostname:
            findings.append(Finding("Endereço incompleto", "Não foi possível identificar o domínio.", 2))
            continue
        if parsed.scheme == "http":
            findings.append(Finding("Conexão sem HTTPS", "O endereço começa com http://. Evite informar dados nele.", 2))
        if "@" in parsed.netloc:
            findings.append(Finding("Domínio disfarçado", "O símbolo @ pode esconder o destino real do endereço.", 4))
        try:
            ipaddress.ip_address(hostname)
            findings.append(Finding("Endereço por IP", "O link usa um número de IP no lugar de um domínio reconhecível.", 2))
        except ValueError:
            labels = hostname.lower().split(".")
            if len(labels) > 4:
                findings.append(Finding("Muitos subdomínios", "Várias partes antes do domínio podem dificultar a leitura do destino.", 2))
            if labels[-1] in SUSPICIOUS_TLDS:
                findings.append(Finding("Extensão que merece atenção", "A extensão do domínio aparece em campanhas de abuso, mas também pode ter usos legítimos.", 2))
            if hostname.startswith("xn--") or ".xn--" in hostname:
                findings.append(Finding("Domínio internacionalizado", "O endereço usa codificação que pode imitar letras conhecidas.", 2))
        if port is not None and port not in (80, 443):
            findings.append(Finding("Porta incomum", "O link informa uma porta diferente das usuais para navegação.", 2))

    score = sum(item.points for item in findings)
    if score >= 5:
        level, summary = "alto", "Há vários sinais de atenção. Evite interagir até confirmar a origem."
    elif score >= 2:
        level, summary = "moderado", "Há sinais que merecem verificação antes de agir."
    else:
        level, summary = "indefinido", "Não encontramos sinais nas regras atuais. Isso não confirma que seja seguro."
    advice = (
        "Não clique no link recebido; abra o aplicativo ou digite o endereço oficial por conta própria.",
        "Confirme a mensagem com a organização por um canal que você já conhece.",
        "Não envie senha, código de verificação ou dados bancários por mensagem.",
    )
    return Result(level, summary, tuple(findings), advice, len(urls))
