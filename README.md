# Staff Softphone — Deployment Guide

A sleek browser-based phone for your staff. Powered by Twilio.

## Files
```
twilio-phone/
├── server.py          ← Flask backend (generates tokens, handles calls)
├── requirements.txt   ← Python dependencies
├── Procfile           ← For Railway / Render deployment
└── static/
    └── index.html     ← The phone UI your staff uses
```

---

## Option A — Deploy to Railway (recommended, free tier)

1. Install the [Railway CLI](https://docs.railway.app/develop/cli) or use railway.app in your browser
2. Create a free account at https://railway.app
3. In your terminal:
   ```bash
   cd twilio-phone
   railway login
   railway init
   railway up
   ```
4. Copy the public URL Railway gives you (e.g. `https://your-app.up.railway.app`)

---

## Option B — Deploy to Render (also free)

1. Push this folder to a GitHub repo
2. Go to https://render.com → New → Web Service
3. Connect your GitHub repo
4. Set:
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `gunicorn server:app`
5. Copy the public URL Render gives you

---

## Option C — Run locally with ngrok (for testing)

```bash
cd twilio-phone
pip install -r requirements.txt
python server.py
```
In a second terminal:
```bash
ngrok http 5000
```
Copy the `https://xxxx.ngrok.io` URL.

---

## Final step — Point Twilio to your server

1. Go to [Twilio Console](https://console.twilio.com) → Voice → TwiML Apps
2. Open your TwiML App (AP7ee0c56ee46c1f7ff89a3c041c474c29)
3. Set **Voice Request URL** to: `https://YOUR-URL/voice`
4. Save

Then open `https://YOUR-URL` in your browser — your staff phone is live!

---

## Notes

- The token auto-refreshes if the device goes offline
- Call history is saved in the browser (localStorage)
- To add a second staff member, open the URL on their computer — they each get their own history
- Calls are billed per minute by Twilio from your account balance
