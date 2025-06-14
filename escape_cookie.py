import json

# Step 1 Load JSON cookie file
with open("session_data.bin", "r", encoding="utf-8") as f:
    cookies = json.load(f)

# Step 2 Pick only required cookies
required_names = {"ds_user_id", "sessionid", "csrftoken"}
selected = [f"{c['name']}={c['value']}" for c in cookies if c["name"] in required_names]

# Step 3 Join them as single header string
header_cookie = "; ".join(selected)
print("\nRaw Cookie:\n", header_cookie)

# ✅ ✅ Step 4 Escape it for Railway
escaped = header_cookie.encode("unicode_escape").decode()
print("\nEscaped Cookie for IG_COOKIE:\n", escaped)
