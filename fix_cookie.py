import codecs

# Paste your escaped cookie string here (from IG_COOKIE)
escaped = ".instagram.com\tTRUE\t/\tTRUE\t1784312561\tcsrftoken\tK8w30dVuthWzTVuwL1pL0QWbFkC74HOX\n.instagram.com\tTRUE\t/\tTRUE\t1784312561\tmid\taEsa8QALAAFvE3aYs1q7hAXQNWyB\n.instagram.com\tTRUE\t/\tTRUE\t1781288561\tig_did\t6E73DF01-392E-4FEB-9F47-44D98EC2D72B\n.instagram.com\tTRUE\t/\tTRUE\t1781288561\tig_nrcb\t1"

decoded = codecs.decode(escaped, 'unicode_escape')

with open("cookie_fixed.txt", "w", encoding="utf-8") as f:
    f.write(decoded)

print("✅ cookie_fixed.txt created successfully.")




