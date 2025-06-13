import codecs

# Paste your escaped cookie string here (from IG_COOKIE)
escaped = """.instagram.com\tTRUE\t/\tTRUE\tps_n\t1783751581\t1\n.instagram.com\tTRUE\t/\tTRUE\tdatr\t1783751586\tnItCaJyyhxuoliUKZZul0f3F\n.instagram.com\tTRUE\t/\tTRUE\tig_nrcb\t1780728994\t1\n.instagram.com\tTRUE\t/\tTRUE\tds_user_id\t1757524897\t75050363583\n.instagram.com\tTRUE\t/\tTRUE\tcsrftoken\t1784308897\t6ii0ELkEr1nCEoByGJDmlBnFMsFtmMCl\n.instagram.com\tTRUE\t/\tTRUE\tig_did\t1780727586\tF99C0934-2CA3-4EF4-9110-E0F9248329B1\n.instagram.com\tTRUE\t/\tTRUE\tps_l\t1783751581\t1\n.instagram.com\tTRUE\t/\tTRUE\twd\t1750353690\t1280x574\n.instagram.com\tTRUE\t/\tTRUE\tmid\t1783752966\taEKRBgALAAGLVjG1lW-qNpw8YJj4\n.instagram.com\tTRUE\t/\tTRUE\tsessionid\t1781249454\t75050363583%3AEmY3ejtSzdRB1f%3A22%3AAYd4NS4ONAJ-VO641F_yqod4wCu9vdcUcGClGxRSWQ\n.instagram.com\tTRUE\t/\tTRUE\tdpr\t1750353690\t1.5\n.instagram.com\tTRUE\t/\tTRUE\trur\t1749835299\t\"EAG\\05475050363583\\0541781284897:01fe27095248d3ab97d6c88ae40899a43fdb3a8c4b89942e49f7531c2b3e0ea6fec24abd\"
"""

decoded = codecs.decode(escaped, 'unicode_escape')

with open("cookie_fixed.txt", "w", encoding="utf-8") as f:
    f.write(decoded)

print("✅ cookie_fixed.txt created successfully.")
