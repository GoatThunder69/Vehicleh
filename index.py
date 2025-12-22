from flask import Flask, jsonify
import requests
import time

app = Flask(__name__)

OWNER = "@GoatThunder"
DELAY_SECONDS = 8   # 8 sec (yahan 10 chahiye to 10 kar do)

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

def remove_never_delete(obj):
    """
    Recursively remove any value or key containing '@never_delete'
    """
    if isinstance(obj, dict):
        clean = {}
        for k, v in obj.items():
            if isinstance(v, str) and "@never_delete" in v:
                continue
            if isinstance(k, str) and "@never_delete" in k:
                continue
            clean[k] = remove_never_delete(v)
        return clean

    elif isinstance(obj, list):
        return [remove_never_delete(i) for i in obj]

    elif isinstance(obj, str):
        return obj.replace("@never_delete", "").strip()

    return obj


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
        "api": "Vehicle + RC Merge API",
        "status": "running",
        "Owner": OWNER,
        "endpoints": {
            "/vehicle-merge/<reg_no>": "Merge botfiles vehicle API + anuj-rcc API",
            "/health": "Health check"
        }
    })


# ---------------- VEHICLE + RC MERGE ----------------
@app.route("/vehicle-merge/<reg_no>")
def vehicle_merge(reg_no):

    vehicle_api_response = None
    rc_api_response = None

    # -------- VEHICLE API (botfiles) --------
    try:
        v_url = "https://botfiles.serv00.net/vehicle/api.php"
        v_params = {
            "key": "ThunderOfficial",
            "reg": reg_no
        }

        v = requests.get(v_url, headers=HEADERS, params=v_params, timeout=14)
        try:
            vehicle_api_response = remove_never_delete(v.json())
        except:
            vehicle_api_response = {
                "error": "Vehicle API invalid JSON",
                "raw": v.text
            }

    except Exception as e:
        vehicle_api_response = {
            "error": "Vehicle API failed",
            "details": str(e)
        }

    # -------- RC API (anuj-rcc) --------
    try:
        r_url = f"https://anuj-rcc.vercel.app/rc?query={reg_no}"
        r = requests.get(r_url, headers=HEADERS, timeout=14)
        try:
            rc_api_response = remove_never_delete(r.json())
        except:
            rc_api_response = {
                "error": "RC API invalid JSON",
                "raw": r.text
            }

    except Exception as e:
        rc_api_response = {
            "error": "RC API failed",
            "details": str(e)
        }

    # -------- DELAY (so both APIs open properly) --------
    time.sleep(DELAY_SECONDS)

    # -------- FINAL RESPONSE --------
    return jsonify({
        "success": True,
        "query": reg_no,
        "vehicle_api_response": vehicle_api_response,
        "rc_api_response": rc_api_response,
        "Owner": OWNER
    })
