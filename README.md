# CrewAI + n8n (30-min MVP) — Webhook Triagem

MVP bem enxuto: **n8n** recebe um **Webhook** e chama um **script Python (CrewAI)** que devolve um **JSON**.

> ⚠️ Você precisa ter **Python 3.10+** instalado e uma **OPENAI_API_KEY** (ou adaptar para outro provider).

---

## 1) Subir o n8n (Docker)

```bash
docker compose up -d
```

Abra:
- http://localhost:5678

Arquivo usado: `docker-compose.yml`

---

## 2) Preparar o Python (CrewAI)

### 2.1 Criar venv e instalar deps
```bash
cd crew_mvp
python -m venv .venv

# Windows:
.venv\Scripts\activate

# Linux/Mac:
# source .venv/bin/activate

pip install -r requirements.txt
```

### 2.2 Configurar env
Crie um `.env` dentro de `crew_mvp/` com:
```bash
OPENAI_API_KEY=COLE_SUA_KEY_AQUI
```

Você pode usar como base: `crew_mvp/.env.example`

---

## 3) Teste rápido do script (sem n8n)

```bash
cd crew_mvp

python crew_runner.py "{\"subject\":\"Erro no login\",\"body\":\"Não consigo entrar. Erro 500\",\"from\":\"cliente@x.com\"}"
```

Ele deve imprimir um JSON.

---

## 4) Importar o workflow no n8n

Arquivo:
- `n8n/workflow_webhook_triage.json`

No n8n:
1. **Workflows** → **Import from File**
2. Abra o JSON acima
3. No node **Execute Command**, ajuste o comando (abaixo)

### Ajuste do Execute Command (IMPORTANTE)
Você precisa apontar para o caminho do projeto e python da venv.

**Windows (exemplo):**
```bat
cmd /c "cd C:\CAMINHO\DO\REPO\crew_mvp && .venv\Scripts\python crew_runner.py \"{{$json | jsonStringify}}\""
```

**Linux/Mac (exemplo):**
```bash
bash -lc "cd /CAMINHO/DO/REPO/crew_mvp && . .venv/bin/activate && python crew_runner.py '{{$json | jsonStringify}}'"
```

Depois ative o workflow.

---

## 5) Testar o Webhook

```bash
curl -X POST "http://localhost:5678/webhook/triage" \
  -H "Content-Type: application/json" \
  -d "{\"subject\":\"Boleto\",\"body\":\"Preciso da 2 via do boleto\",\"from\":\"cliente@x.com\"}"
```

---

## Saída esperada (exemplo)
```json
{
  "category": "financeiro",
  "priority": "media",
  "summary": "Cliente solicitou 2ª via do boleto.",
  "entities": {},
  "reply_draft": "Olá! Claro — vou te ajudar com a 2ª via do boleto. Pode me confirmar..."
}
```

---

## Estrutura do repo

```
.
├─ docker-compose.yml
├─ crew_mvp/
│  ├─ crew_runner.py
│  ├─ requirements.txt
│  └─ .env.example
└─ n8n/
   └─ workflow_webhook_triage.json
```

Boa noite 😄
