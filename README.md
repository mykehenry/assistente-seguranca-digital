# Assistente de Segurança Digital

Uma ferramenta educativa do projeto **AI4Good** para ajudar pessoas no Brasil a reconhecer sinais comuns de phishing em mensagens e links. Você cola um trecho, recebe uma avaliação explicada e vê o que fazer antes de clicar, responder ou pagar.

> **Estado do projeto:** MVP funcional. [Experimente a demonstração pública](https://assistente-seguranca-digital.onrender.com/). O serviço gratuito pode demorar a iniciar após ficar inativo.

## O que a ferramenta faz

O aplicativo usa regras determinísticas para apontar:

| Sinal | Por que merece atenção |
| --- | --- |
| Urgência ou ameaça de bloqueio | Golpes costumam pressionar para impedir uma conferência cuidadosa. |
| Menção a senha, código ou dado pessoal | Pedidos desse tipo exigem confirmação por um canal oficial. |
| Menção a Pix, boleto ou transferência | É importante conferir destinatário e cobrança fora da mensagem recebida. |
| Link com `http://`, `@`, IP, porta incomum, muitos subdomínios, domínio codificado ou certas extensões | Esses padrões podem dificultar a identificação do destino ou justificar uma verificação adicional. |

Cada sinal vem com uma explicação. O resultado indica **atenção elevada**, **atenção recomendada** ou **segurança não confirmada**. A classificação vem da soma de pontos das regras (`2–4` por sinal; `5` ou mais gera atenção elevada). Ela não é uma probabilidade estatística.

### Como interpretar o resultado

- **Atenção elevada:** há vários sinais ou uma combinação forte. Não interaja antes de confirmar a origem.
- **Atenção recomendada:** há ao menos um sinal que precisa ser conferido.
- **Segurança não confirmada:** nenhuma regra atual identificou um sinal. **Isso não quer dizer que seja seguro.**

Mesmo quando o resultado parece tranquilo, abra o aplicativo oficial ou digite você mesmo o endereço conhecido da organização. Não use o link recebido para verificar a própria mensagem.

## Exemplos para experimentar

Use somente exemplos fictícios; não envie credenciais reais.

| Entrada | Resultado esperado |
| --- | --- |
| `Urgente: sua conta será bloqueada. Informe sua senha agora.` | Atenção elevada; urgência e pedido sensível. |
| `http://usuario@203.0.113.7:8080/login` | Atenção elevada; HTTP, `@`, IP e porta incomum. |
| `Nossa reunião será amanhã às 14h.` | Segurança não confirmada; nenhum sinal conhecido. |

## Privacidade e limites

- Cole **apenas o trecho necessário** e remova nomes, CPF, senhas, códigos e dados bancários. A entrada é limitada a 1.000 caracteres.
- O texto é enviado ao servidor Django para análise durante a solicitação. Este aplicativo não cria conta, banco de dados ou histórico de análises e não devolve o texto enviado na página de resultado.
- As URLs recebidas são tratadas como texto: o aplicativo **não as visita, não faz requisições HTTP e não resolve seus domínios por DNS**.
- Uma hospedagem ou proxy externo pode manter registros próprios. Quem implantar o projeto deve revisar a configuração de logs e a política de privacidade da infraestrutura.
- A versão inicial usa **heurísticas, não um modelo de linguagem (LLM)**. Há falsos positivos e falsos negativos; o serviço **não garante segurança** e não substitui a confirmação por canais oficiais.

## Executar no computador

Requer Python compatível com Django 6.1 (testado com Python 3.15).

Se quiser isolar as dependências, crie um ambiente com `python -m venv .venv` e ative-o **antes** da instalação (`.venv\Scripts\Activate.ps1` no PowerShell; `source .venv/bin/activate` no macOS/Linux).

```bash
python -m pip install -r requirements.txt
python manage.py runserver
```

Abra `http://127.0.0.1:8000/`. O MVP não precisa de banco de dados nem de migrações.

## Testes

```bash
python manage.py test
python manage.py check
```

Os testes cobrem exemplos com e sem sinais, validação da entrada, resultado HTTP, proteção contra exibir novamente o texto enviado e a ausência de chamadas de rede durante a análise.

## Hospedagem

Para publicar em um serviço que execute Python/Django, configure:

| Variável | Uso |
| --- | --- |
| `DJANGO_SECRET_KEY` | Segredo aleatório e privado para produção. |
| `DJANGO_ALLOWED_HOSTS` | Domínios públicos separados por vírgula. |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Origens HTTPS completas, separadas por vírgula. |
| `DJANGO_DEBUG=0` | Desativa páginas de depuração. |
| `DJANGO_HTTPS=1` | Ativa redirecionamento HTTPS, cookies seguros e HSTS. |

O repositório inclui [`render.yaml`](render.yaml) com um serviço web gratuito, instalação de dependências, coleta de arquivos estáticos e geração de um segredo privado. No Render, conecte este repositório como Blueprint; o domínio `onrender.com` fornecido pela plataforma é reconhecido automaticamente pelo Django. Após a implantação, confirme que a página, o CSS e o envio do formulário funcionam no endereço público.

A demonstração atual foi criada a partir da URL pública do repositório, sem conexão de implantação automática. Para publicar futuras alterações do GitHub, use **Manual Deploy** no painel do serviço Render. O arquivo `render.yaml` pode ser usado em uma configuração Blueprint futura.

Exemplo de inicialização em um servidor Linux com HTTPS configurado no proxy:

```bash
python manage.py collectstatic --noinput
gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000}
```

O WhiteNoise serve os arquivos estáticos. Não use `runserver` em produção. O valor padrão de `DJANGO_SECRET_KEY` serve apenas ao desenvolvimento local. Antes de divulgar uma implantação, execute `python manage.py check --deploy` com as variáveis reais e teste o formulário no domínio público.

## Próximos passos

- Validar as regras com exemplos de golpes brasileiros e medir falsos positivos e negativos.
- Melhorar a cobertura de URLs e a clareza das explicações sem visitar os destinos.
- Testar acessibilidade com leitores de tela e pessoas usuárias.
- Publicar uma política de privacidade apropriada para a hospedagem atual.

## Licença

MIT. Veja [LICENSE](LICENSE).
