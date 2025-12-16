from flask import Flask, jsonify
import requests

# ---------------- BASIC APP ----------------
app = Flask(__name__)

OWNER = "@GoatThunder"

# ---------------- HEALTH CHECK ----------------
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
        "api": "Vehicle + Challan Merge API",
        "status": "running",
        "Owner": OWNER,
        "endpoints": {
            "/health": "Health check",
            "/vehicle-merge/<vehicle_no>": "Merged raw response from RC, Vehicle & Challan APIs"
        }
    })

# ---------------- VEHICLE + CHALLAN MERGE API ----------------
@app.route("/vehicle-merge/<vehicle_no>")
def vehicle_merge(vehicle_no):
    primary_response = None
    secondary_response = None
    challan_response = None

    # -------- PRIMARY API (anuj-rcc) --------
    try:
        primary_url = f"https://anuj-rcc.vercel.app/rc?query={vehicle_no}"
        p = requests.get(primary_url, timeout=8)

        try:
            primary_response = p.json()
        except:
            primary_response = {
                "raw_response": p.text,
                "note": "Primary API did not return JSON"
            }

    except Exception as e:
        primary_response = {
            "error": "Primary API failed",
            "details": str(e)
        }

    # -------- SECONDARY API (flipcartstore) --------
    try:
        secondary_url = (
            "https://flipcartstore.serv00.net/vehicle/api.php"
            f"?reg={vehicle_no}&key=Tofficial"
        )
        s = requests.get(secondary_url, timeout=8)

        try:
            secondary_response = s.json()
        except:
            secondary_response = {
                "raw_response": s.text,
                "note": "Secondary API did not return JSON"
            }

    except Exception as e:
        secondary_response = {
            "error": "Secondary API failed",
            "details": str(e)
        }

    # -------- CHALLAN API (Cloudflare Worker – USER PROVIDED) --------
    try:
        challan_url = (
            "https://api.b77bf911.workers.dev/vehicle"
            f"?registration={vehicle_no}"
        )
        c = requests.get(challan_url, timeout=8)

        try:
            challan_response = c.json()
        except:
            challan_response = {
                "raw_response": c.text,
                "note": "Challan API did not return JSON"
            }

    except Exception as e:
        challan_response = {
            "error": "Challan API failed",
            "details": str(e)
        }

    # -------- FINAL PURE COPY-PASTE RESPONSE --------
    return jsonify({
        "success": True,
        "query": vehicle_no,

        "primary_api_response": primary_response,
        "secondary_api_response": secondary_response,
        "challan_api_response": challan_response,

        "Owner": OWNER
    })
