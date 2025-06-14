# escape_cookie.py
with open("cookie_fixed.txt", "r", encoding="utf-8") as f:
    raw = f.read()

escaped = raw.encode("unicode_escape").decode()
print(escaped)
