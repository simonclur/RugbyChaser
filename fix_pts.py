import json

with open("index.html", "r") as f:
    html = f.read()

# Ah! In the fetch loop, I STILL have:
# if (pts !== undefined) { t.points = pts; }
# And:
# teams.sort((a,b) => parseFloat(b.points || 0) - parseFloat(a.points || 0));

html = html.replace('t.points = pts;', 't.rankingPts = pts;')
html = html.replace('teams.sort((a,b) => parseFloat(b.points || 0) - parseFloat(a.points || 0));', 'teams.sort((a,b) => (parseFloat(b.points || 0) - parseFloat(a.points || 0)) || (parseFloat(b.rankingPts || 0) - parseFloat(a.rankingPts || 0)));')

with open("index.html", "w") as f:
    f.write(html)
