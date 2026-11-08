# Assistente de Segurança Digital

MVP AI4Good em português brasileiro para ajudar pessoas a reconhecer sinais de phishing em mensagens e URLs. O resultado explica os sinais encontrados e oferece próximos passos simples.

**Limite importante:** esta versão usa heurísticas determinísticas, **não usa LLM** e **não garante segurança**. A ausência de sinais conhecidos não prova que o conteúdo seja confiável. A ferramenta é educativa e não substitui confirmação pelos canais oficiais.

## Privacidade

- Não cria conta, banco de dados, histórico ou log do conteúdo enviado no código do aplicativo.
- Processa apenas o trecho submetido e não o devolve na página de resultado.
- **Nunca acessa, resolve por DNS ou visita as URLs informadas.** Só interpreta o texto localmente.
- Recomenda remover dados pessoais e limita a entrada a 1.000 caracteres.
- Em hospedagens de terceiros, infraestrutura e servidor web podem manter registros próprios; configure-os conforme sua política de privacidade.

## Rodar localmente

Requer Python compatível com Django 6.1 (testado com Python 3.15).

```bash
python -m venv .venv
# Ative o ambiente virtual conforme seu sistema
python -m pip install -r requirements.txt
python manage.py runserver
```

Acesse `http://127.0.0.1:8000/`. Não há migrações nem banco de dados no MVP.

## Testes

```bash
python manage.py test
python manage.py check --deploy
```

Casos de exemplo:

| Entrada | Esperado |
| --- | --- |
| `Urgente: sua conta será bloqueada. Informe sua senha agora.` | Atenção elevada, com explicações de urgência e pedido sensível |
| `http://usuario@203.0.113.7:8080/login` | Alerta sobre HTTP, `@`, IP e porta incomum |
| `Nossa reunião será amanhã às 14h.` | Segurança não confirmada; nenhum sinal conhecido |

## Hospedagem

Configure `DJANGO_SECRET_KEY` com valor aleatório, `DJANGO_ALLOWED_HOSTS` com os domínios públicos e `DJANGO_CSRF_TRUSTED_ORIGINS` com as origens HTTPS. Use `DJANGO_DEBUG=0` e HTTPS. Exemplo de processo:

```bash
python manage.py collectstatic --noinput
gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000}
```

Para servir arquivos estáticos em hospedagem simples, configure WhiteNoise ou sirva `staticfiles/` no proxy. Não use o servidor `runserver` para produção.

## Licença

MIT. Veja [LICENSE](LICENSE).
