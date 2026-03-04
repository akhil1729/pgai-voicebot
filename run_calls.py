import os
import time
from dotenv import load_dotenv
from app.twilio_client import make_call
from app.scenarios import all_scenarios

load_dotenv()

PUBLIC_BASE_URL = os.environ["PUBLIC_BASE_URL"].rstrip("/")
TARGET_NUMBER = os.environ["TARGET_NUMBER"]

def main():
    scenarios = list(all_scenarios().keys())

    # Use 10 calls minimum (or more if you want)
    chosen = scenarios[:10]

    for scenario_id in chosen:
        twiml_url = f"{PUBLIC_BASE_URL}/twiml?scenario={scenario_id}"

        # Recording callback is separate from status callback.
        # We'll attach recordingStatusCallback using Twilio Console OR by app logic.
        # Here we set status callback only; recording callback is configured in Console (recommended)
        status_callback = f"{PUBLIC_BASE_URL}/call_status"

        sid = make_call(
            to_number=TARGET_NUMBER,
            twiml_url=twiml_url,
            status_callback=status_callback
        )
        print(f"Started call {sid} scenario={scenario_id}")
        time.sleep(5)  # small delay so you don’t spam instantly

if __name__ == "__main__":
    main()