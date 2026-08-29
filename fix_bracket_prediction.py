import json

with open("index.html", "r") as f:
    html = f.read()

# The script does correctly update t.rankingPts in fetchInitialRankingsAndUpdatePools()!
# Oh wait, my old fix_pts.py script broke something! 
# Let me look closely at the fetch InitialRankingsAndUpdatePools inside index.html

new_js = """                            if (pts !== undefined) {
                                t.rankingPts = pts;
                            }
"""

html = html.replace("""                            if (pts !== undefined) {
                                t.rankingPts = pts;
                            }""", """                            if (pts !== undefined) {
                                t.rankingPts = parseFloat(pts); 
                            }""")

with open("index.html", "w") as f:
    f.write(html)
