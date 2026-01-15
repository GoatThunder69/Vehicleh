import json
import time
import random
import requests

def handler(request):
    try:
        query = request.query.get("query")

        if not query:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({
                    "status": False,
                    "message": "query parameter missing",
                    "credit": "@GoatThunder"
                })
            }

        # ⚠️ SAFE DELAY (vercel free)
        time.sleep(random.uniform(7, 8))

        url = f"https://api.b77bf911.workers.dev/v2?query={query}"
        response = requests.get(url, timeout=10)
        data = response.json()

        data["credit"] = "@GoatThunder"
        data["powered_by"] = "GoatThunder API"

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(data)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "status": False,
                "error": str(e),
                "credit": "@GoatThunder"
            })
        }
