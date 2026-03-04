import os
import json
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Ensure .env is loaded even when this module is imported first
load_dotenv()

def _client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is missing. Check your .env file.")
    return OpenAI(api_key=api_key)

def transcribe_audio(audio_path: str) -> str:
    # Whisper transcription (single mixed track). Good enough for challenge.
    with open(audio_path, "rb") as f:
        transcript = _client().audio.transcriptions.create(
            model="whisper-1",
            file=f
        )
    return transcript.text

def bug_analyze(transcript_text: str) -> dict:
    model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
    prompt = f"""
You are evaluating a healthcare phone agent. Given the call transcript below (mixed audio transcription),
identify bugs or quality issues:
- incorrect answers
- hallucinations / made-up details
- failure to understand intent
- awkward / unprofessional phrasing
- missing steps (e.g., not confirming appointment details)
- looping / dead-ends

Return JSON with:
{{
  "summary": "...",
  "issues": [
    {{"type": "...", "severity": "low|medium|high", "evidence": "...", "suggested_fix": "..."}}
  ]
}}

Transcript:
{transcript_text}
"""
    resp = _client().chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    content = resp.choices[0].message.content.strip()

    # Try to parse JSON. If parsing fails, wrap raw text.
    try:
        return json.loads(content)
    except Exception:
        return {"summary": "Non-JSON output", "issues": [], "raw": content}

def save_artifacts(call_sid: str, transcript_text: str, bug_json: dict):
    base = Path("artifacts")
    (base / "transcripts").mkdir(parents=True, exist_ok=True)
    (base / "bug_reports").mkdir(parents=True, exist_ok=True)

    (base / "transcripts" / f"{call_sid}.txt").write_text(transcript_text, encoding="utf-8")
    (base / "bug_reports" / f"{call_sid}.json").write_text(
        json.dumps(bug_json, indent=2), encoding="utf-8"
    )