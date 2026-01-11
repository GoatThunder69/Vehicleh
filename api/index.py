import re
import requests
from urllib.parse import parse_qs

X10_API = "https://api.x10.network/numapi.php"
X10_KEY = "thunder"

def handler(request):
    query = parse_qs(request.query)

    def silent():
        return ("", 204, {})

    action = query.get("action", [None])[0]
    test1  = query.get("test1", [None])[0]

    # basic checks
    if action != "api" or not test1:
        return silent()

    data = test1.lower()

    # block spam / mentions / links
    for b in ["@", "http", "https", "www", "salaar"]:
        if b in data:
            return silent()

    # strict format (JK05F1806)
    if not re.match(r"^[A-Z]{2}[0-9]{2}[A-Z][0-9]{4}$", test1, re.I):
        return silent()

    # 🔥 CALL ORIGINAL X10 API (FAST)
    try:
        resp = requests.get(
            X10_API,
            params={
                "action": "api",
                "key": X10_KEY,
                "test1": test1
            },
            timeout=3
        )
    except:
        return silent()

    if resp.status_code != 200 or not resp.text:
        return silent()

    # 🔥 RETURN EXACT RESPONSE (NO CHANGE)
    return (
        resp.text,
        200,
        {"Content-Type": "application/json"}
        )
