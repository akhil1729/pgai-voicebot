import os
from fastapi import FastAPI, Request, Response
from fastapi.responses import PlainTextResponse
from twilio.twiml.voice_response import VoiceResponse, Pause
from dotenv import load_dotenv
from .scenarios import all_scenarios
from .utils import download_file
from .transcribe import transcribe_audio, bug_analyze, save_artifacts

load_dotenv()

app = FastAPI()
SCENARIOS = all_scenarios()

PUBLIC_BASE_URL = os.environ.get("PUBLIC_BASE_URL", "").rstrip("/")
if not PUBLIC_BASE_URL:
    # You can still run locally, but Twilio must reach your endpoints via tunnel.
    print("WARNING: PUBLIC_BASE_URL is not set. Twilio webhooks won't work without a public URL.")

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/twiml")
@app.get("/twiml")
async def twiml(request: Request):
    scenario_id = request.query_params.get("scenario", "sched_simple")
    s = SCENARIOS.get(scenario_id)

    vr = VoiceResponse()
    if not s:
        vr.say("Sorry, scenario not found. Goodbye.")
        vr.hangup()
        return Response(content=str(vr), media_type="text/xml")

    # Speak scripted "patient" turns with pauses for the agent to respond.
    # This is simple but effective for stress testing.
    vr.say(f"Scenario: {s.title}.")
    vr.pause(length=1)

    for turn in s.turns:
        vr.say(turn.say)
        vr.append(Pause(length=max(1, int(turn.pause_sec))))

    vr.say("Goodbye.")
    vr.hangup()

    return Response(content=str(vr), media_type="text/xml")

@app.post("/call_status")
async def call_status(request: Request):
    # Twilio posts CallSid, CallStatus, RecordingUrl may not appear here.
    form = await request.form()
    call_sid = form.get("CallSid")
    status = form.get("CallStatus")
    return PlainTextResponse(f"{call_sid} {status}")

@app.post("/recording_status")
async def recording_status(request: Request):
    """
    Twilio will hit this when the recording is ready.
    We'll download it, transcribe it, and generate bug report.
    """
    form = await request.form()
    call_sid = form.get("CallSid")
    recording_url = form.get("RecordingUrl")  # without file extension usually

    if not call_sid or not recording_url:
        return PlainTextResponse("missing fields", status_code=400)

    # Twilio recording URLs often need .mp3 appended
    mp3_url = recording_url + ".mp3"
    out_mp3 = f"artifacts/recordings/{call_sid}.mp3"

    try:
        download_file(mp3_url, out_mp3)
        transcript_text = transcribe_audio(out_mp3)
        bugs = bug_analyze(transcript_text)
        save_artifacts(call_sid, transcript_text, bugs)
    except Exception as e:
        return PlainTextResponse(f"error: {e}", status_code=500)

    return PlainTextResponse("ok")