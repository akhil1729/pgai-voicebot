# 📞 PGAI Voicebot – Setup & Run Guide

This project creates an outbound AI-powered patient bot that:

1. Makes automated calls via Twilio
2. Records the call
3. Downloads the recording
4. Transcribes audio using OpenAI Whisper
5. Generates a structured bug/quality report

---

# 🧰 Tech Stack

- Python 3.11+
- FastAPI
- Twilio Voice API
- OpenAI API
- Cloudflare Tunnel (public webhook exposure)

---

# 📁 Project Structure
pgai-voicebot/
│
├── app/
│ ├── server.py
│ ├── twilio_client.py
│ ├── transcribe.py
│ ├── scenarios.py
│ ├── utils.py
│
├── artifacts/
│ ├── recordings/
│ ├── transcripts/
│ ├── bug_reports/
│
├── run_calls.py
├── requirements.txt
├── .env
└── README.md



---

# ⚙️ Environment Setup (Windows)

## 1️⃣ Clone or open project

powershell
cd D:\pgai-voicebot


python -m venv .venv
& .venv\Scripts\Activate.ps1

pip install -r requirements.txt

pip install twilio fastapi uvicorn python-multipart requests python-dotenv openai


# Twilio
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_FROM_NUMBER=+1xxxxxxxxxx

# Cloudflare public URL
PUBLIC_BASE_URL=https://your-tunnel.trycloudflare.com

# Target number to call
TARGET_NUMBER=+1xxxxxxxxxx

# OpenAI
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx
OPENAI_MODEL=gpt-4o-mini


# Step 1 – Start FastAPI server
Open Terminal 1:
& .venv\Scripts\Activate.ps1
uvicorn app.server:app --host 0.0.0.0 --port 8000

#Step 2 – Start Cloudflare Tunnel

Open Terminal 2:

.\cloudflared.exe tunnel --url http://localhost:8000

#Copy the generated URL:
https://random-name.trycloudflare.com

#update .env
PUBLIC_BASE_URL=https://random-name.trycloudflare.com


## make a call
# Open Terminal 3
& .venv\Scripts\Activate.ps1
python run_calls.py

