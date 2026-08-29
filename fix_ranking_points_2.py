import json

with open("index.html", "r") as f:
    html = f.read()

# Ah wait, I need to clear out the previous hardcoded mutation block
# The javascript dynamically overwrites the 'TBD' or fetched `rwc_pools.json` points because of: 
# `t.points = pts;`

html = html.replace('t.rankingPts = pts;', 't.rankingPts = pts; // DO NOT Overwrite the groups ladder t.points anymore')

with open("index.html", "w") as f:
    f.write(html)
