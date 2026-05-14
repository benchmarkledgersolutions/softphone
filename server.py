from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VoiceGrant
from twilio.twiml.voice_response import VoiceResponse, Dial
import os

app = Flask(__name__, static_folder="static")
CORS(app)

# ── Twilio credentials ──────────────────────────────────────────────────────
ACCOUNT_SID   = os.environ.get("TWILIO_ACCOUNT_SID",   "ACdf3325e833a14baa42bde3a72b8d0e33")
AUTH_TOKEN    = os.environ.get("TWILIO_AUTH_TOKEN",    "278a01637634d88ae8ee25643e0b30ae")
API_KEY       = os.environ.get("TWILIO_API_KEY",       "SK84f1fda5406e228ab91bb9c9f4222cec")
API_SECRET    = os.environ.get("TWILIO_API_SECRET",    "TdQCdgl2J7El01GS725lnKXojhvGD9vU")
TWIML_APP_SID = os.environ.get("TWILIO_APP_SID",       "AP7ee0c56ee46c1f7ff89a3c041c474c29")
FROM_NUMBER   = os.environ.get("TWILIO_NUMBER",        "+16167278602")
# ────────────────────────────────────────────────────────────────────────────


@app.route("/")
def index():
    """Serve the frontend."""
    return send_from_directory("static", "index.html")


@app.route("/token")
def token():
    """
    Return a short-lived Twilio Access Token so the browser SDK can make calls.
    Identity can be passed as ?identity=alice; defaults to 'staff'.
    """
    identity = request.args.get("identity", "staff")

    access_token = AccessToken(
        ACCOUNT_SID,
        API_KEY,
        API_SECRET,
        identity=identity,
        ttl=3600          # token valid for 1 hour
    )
    grant = VoiceGrant(
        outgoing_application_sid=TWIML_APP_SID,
        incoming_allow=False
    )
    access_token.add_grant(grant)

    return jsonify(token=access_token.to_jwt())


@app.route("/voice", methods=["POST"])
def voice():
    """
    Twilio hits this endpoint when the browser initiates a call.
    It returns TwiML that dials the destination number.
    """
    to = request.form.get("To", "")
    response = VoiceResponse()

    if to:
        dial = Dial(caller_id=FROM_NUMBER, timeout=30)
        dial.number(to)
        response.append(dial)
    else:
        response.say("No destination number provided.")

    return str(response), 200, {"Content-Type": "text/xml"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
