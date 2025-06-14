import json
import codecs

cookie_path = "cookie.txt"


# Parse Netscape format manually
def parse_netscape_cookie(file_path):
    cookie_parts = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith("#") or not line.strip():
                continue
            parts = line.strip().split("\t")
            if len(parts) == 7:
                name = parts[5]
                value = parts[6]
                cookie_parts.append(f"{name}={value}")
    return "; ".join(cookie_parts)


# Step 1: Read cookie from cookie.txt
raw_cookie = parse_netscape_cookie(cookie_path)
print("\n🔎 Raw Cookie:")
print(raw_cookie)

# Step 2: Escape the cookie
escaped_cookie = codecs.encode(raw_cookie, "unicode_escape").decode()

# Step 3: Final output
print("\n✅ Paste this into Railway .env as IG_COOKIE:")
print(f"\nIG_COOKIE={escaped_cookie}")
