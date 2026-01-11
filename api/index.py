import re
from urllib.parse import parse_qs

def handler(request):
    query = parse_qs(request.query)

    def silent():
        return ("", 204, {})

    action = query.get("action", [None])[0]
    test1 = query.get("test1", [None])[0]

    if action != "api" or not test1:
        return silent()

    data = test1.lower()

    # block spam
    for b in ["@", "http", "https", "www", "salaar"]:
        if b in data:
            return silent()

    # strict pattern
    if not re.match(r"^[A-Z]{2}[0-9]{2}[A-Z][0-9]{4}$", test1, re.I):
        return silent()

    return (
        f'{{"status":true,"result":"{test1}"}}',
        200,
        {"Content-Type": "application/json"}
    )
