import json
import re

with open("index.html", "r") as f:
    html = f.read()

# I want to change:
# t.points = pts;
# TO:
# t.rankingPts = pts;
html = html.replace('t.points = pts;', 't.rankingPts = pts;')

# I want to change:
# teams.sort((a,b) => parseFloat(b.points || 0) - parseFloat(a.points || 0));
# TO basically NOT sort in place, or sort by rankingPts if points are 0
# Actually let's just sort by actual points, then by rankingPts as a tie-breaker.
new_sort = "teams.sort((a,b) => (parseFloat(b.points || 0) - parseFloat(a.points || 0)) || (parseFloat(b.rankingPts || 0) - parseFloat(a.rankingPts || 0)));"
old_sort = "teams.sort((a,b) => parseFloat(b.points || 0) - parseFloat(a.points || 0));"

html = html.replace(old_sort, new_sort)

# Now in renderRWCKnockout, I need it to use rankingPts + points to get standings
old_get_team_sort = "const p = allTeams.filter(t => t.pool === pool).sort((a,b) => b.pts - a.pts || b.gd - a.gd);"
# in renderRWCKnockout we mapped pts to parseInt(t.points)
# Let's see how allTeams is mapped:
# pts: parseInt(t.points) || 0,
# gd: parseInt(t.points_diff) || 0,
# rankingPts: parseFloat(t.rankingPts) || 0
old_allteams_map = """                        pts: parseInt(t.points) || 0,
                        gd: parseInt(t.points_diff) || 0"""
new_allteams_map = """                        pts: parseInt(t.points) || 0,
                        gd: parseInt(t.points_diff) || 0,
                        rankingPts: parseFloat(t.rankingPts) || 0"""
html = html.replace(old_allteams_map, new_allteams_map)

new_get_team_sort = "const p = allTeams.filter(t => t.pool === pool).sort((a,b) => b.pts - a.pts || b.gd - a.gd || b.rankingPts - a.rankingPts);"
html = html.replace(old_get_team_sort, new_get_team_sort)


with open("index.html", "w") as f:
    f.write(html)
