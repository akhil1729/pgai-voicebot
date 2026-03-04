import os
from twilio.rest import Client

def make_call(to_number: str, twiml_url: str, status_callback: str):
    client = Client(os.environ["TWILIO_ACCOUNT_SID"], os.environ["TWILIO_AUTH_TOKEN"])

    public_base = os.environ["PUBLIC_BASE_URL"].rstrip("/")
    if not public_base:
        raise RuntimeError("PUBLIC_BASE_URL is empty. Start cloudflared and set it in .env")

    call = client.calls.create(
        to=to_number,
        from_=os.environ["TWILIO_FROM_NUMBER"],
        url=twiml_url,

        # status events
        status_callback=status_callback,
        status_callback_method="POST",
        status_callback_event=["initiated", "ringing", "answered", "completed"],

        # ✅ recording + callback
        record=True,
        recording_status_callback=f"{public_base}/recording_status",
        recording_status_callback_method="POST",
        recording_status_callback_event=["completed"],
    )
    return call.sid