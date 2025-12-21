from flask import Flask, jsonify
import requests

app = Flask(__name__)

OWNER = "@GoatThunder"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

# ---------------- HEALTH ----------------
@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "Owner": OWNER
    })

# ---------------- HOME ----------------
@app.route("/")
def home():
    return jsonify({
        "api": "Vehicle Lookup API",
        "status": "running",
        "Owner": OWNER,
        "endpoints": {
            "/vehicle/<reg_no>": "Get vehicle details by registration number",
            "/health": "Health check"
        }
    })

# ---------------- VEHICLE LOOKUP ----------------
@app.route("/vehicle/<reg_no>")
def vehicle_lookup(reg_no):
    vehicle_api_response = None

    try:
        url = "https://botfiles.serv00.net/vehicle/api.php"
        params = {
            "key": "ThunderOfficial",
            "reg": reg_no
        }

        r = requests.get(url, headers=HEADERS, params=params, timeout=14)

        try:
            vehicle_api_response = r.json()
        except:
            vehicle_api_response = {
                "error": "Vehicle API did not return JSON",
                "raw_response": r.text
            }

    except Exception as e:
        vehicle_api_response = {
            "error": "Vehicle API failed",
            "details": str(e)
        }

    return jsonify({
        "success": True,
        "query": reg_no,
        "vehicle_api_response": vehicle_api_response,
        "Owner": OWNER
    })
