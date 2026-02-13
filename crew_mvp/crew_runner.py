import json
import sys
from dotenv import load_dotenv
from crewai import Agent, Task, Crew

load_dotenv()

def _clean_fenced_json(text: str) -> str:
    t = text.strip()
    if t.startswith("```"):
        # remove fence markers and optional language tag
        t = t.strip("`").strip()
        if t.lower().startswith("json"):
            t = t[4:].strip()
    return t

def main():
    # Entrada: JSON string no argv[1]
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Missing JSON input"}))
        sys.exit(1)

    raw = sys.argv[1]
    try:
        data = json.loads(raw)
    except Exception:
        print(json.dumps({"error": "Invalid JSON input"}))
        sys.exit(1)

    subject = (data.get("subject") or "").strip()
    body = (data.get("body") or "").strip()
    sender = (data.get("from") or "").strip()

    triage_agent = Agent(
        role="Triage Analyst",
        goal="Classificar mensagem, definir prioridade e gerar resumo objetivo em JSON.",
        backstory="Você transforma mensagens soltas em dados estruturados para automação.",
        verbose=False,
        allow_delegation=False,
    )

    task = Task(
        description=f"""
Analise a mensagem abaixo e retorne APENAS um JSON VÁLIDO, sem texto extra.

Regras:
- category ∈ ["suporte","financeiro","comercial","bug","outros"]
- priority ∈ ["baixa","media","alta"]
- summary: 1 a 2 frases
- entities: pode conter cliente/produto/prazo (se tiver)
- reply_draft: resposta curta e educada (1 parágrafo)

Mensagem:
from: {sender}
subject: {subject}
body: {body}

Formato de saída (JSON):
{{
  "category": "...",
  "priority": "...",
  "summary": "...",
  "entities": {{}},
  "reply_draft": "..."
}}
""",
        expected_output="Um JSON válido no formato solicitado."
    )

    crew = Crew(agents=[triage_agent], tasks=[task], verbose=False)
    result = crew.kickoff()

    text = _clean_fenced_json(str(result))

    # Garantir saída JSON
    try:
        parsed = json.loads(text)
        print(json.dumps(parsed, ensure_ascii=False))
    except Exception:
        print(json.dumps({"raw_output": text}, ensure_ascii=False))

if __name__ == "__main__":
    main()
