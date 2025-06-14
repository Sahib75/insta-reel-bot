import codecs

# 👇 Paste your IG_COOKIE value here (escaped)
escaped = ".instagram.com\tTRUE\t\/\tTRUE\t1783751581\tps_n\t1\r\n.instagram.com\tTRUE\t\/\tTRUE\t1783751586\tdatr\tnItCaJyyhxuoliUKZZul0f3F\r\n.instagram.com\tTRUE\t\/\tTRUE\t1780728994\tig_nrcb\t1\r\n.instagram.com\tTRUE\t\/\tTRUE\t1757674735\tds_user_id\t75050363583\r\n.instagram.com\tTRUE\t\/\tTRUE\t1784458735\tcsrftoken\t6ii0ELkEr1nCEoByGJDmlBnFMsFtmMCl\r\n.instagram.com\tTRUE\t\/\tTRUE\t1780727586\tig_did\tF99C0934-2CA3-4EF4-9110-E0F9248329B1\r\n.instagram.com\tTRUE\t\/\tTRUE\t1783751581\tps_l\t1\r\n.instagram.com\tTRUE\t\/\tTRUE\t1750503529\twd\t1280x574\r\n.instagram.com\tTRUE\t\/\tTRUE\t1783752966\tmid\taEKRBgALAAGLVjG1lW-qNpw8YJj4\r\n.instagram.com\tTRUE\t\/\tTRUE\t1781433314\tsessionid\t75050363583%3AEmY3ejtSzdRB1f%3A22%3AAYfrDHFxP7Jh-sKuUccMj06kWZ9o4vSgDjii3FEunQ\r\n\r\n"

decoded = codecs.decode(escaped, 'unicode_escape')

with open("cookie_fixed.txt", "w", encoding="utf-8") as f:
    f.write(decoded)

print("✅ cookie_fixed.txt created.")
