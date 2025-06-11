import requests

def is_cookie_valid(cookie: str) -> bool:
    headers = {
        "Cookie": cookie,
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get("https://www.instagram.com/", headers=headers)
    return "Login" not in response.text
