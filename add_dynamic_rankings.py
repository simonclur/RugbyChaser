import json

with open("index.html", "r") as f:
    html = f.read()

# We'll inject a fetch call right before renderRWCPools / renderRWCKnockout
# so that the client dynamically fetches rankings on load and overrides the static points!

inject_code = """
        // Fetch Live World Rugby Rankings to predict the bracket dynamically
        async function fetchInitialRankingsAndUpdatePools() {
            try {
                const response = await fetch('https://api.wr-rims-prod.pulselive.com/rugby/v3/rankings/mru', {
                    headers: { 'Accept': 'application/json' }
                });
                
                if (!response.ok) throw new Error("Rankings fetch failed");
                const data = await response.json();
                
                const rankingsMap = {};
                if (data && data.entries) {
                    data.entries.forEach(entry => {
                        if (typeof entry !== 'string' && entry.team && entry.team.name) {
                            rankingsMap[entry.team.name] = entry.pts;
                        }
                    });
                }
                
                const teamNameMap = {
                    "Hong Kong China": "Hong Kong China", 
                    "USA": "USA"
                };

                // Update rwcPoolsData with fetched pts
                if (window.rwcPoolsData) {
                    for (const [pool, teams] of Object.entries(rwcPoolsData)) {
                        teams.forEach(t => {
                            const mapName = teamNameMap[t.team] || t.team;
                            let pts = rankingsMap[mapName];
                            
                            // fallback fuzzy match if needed
                            if (pts === undefined) {
                                for (const [rName, rPts] of Object.entries(rankingsMap)) {
                                    if (rName.includes(mapName) || mapName.includes(rName)) {
                                        pts = rPts;
                                        break;
                                    }
                                }
                            }
                            
                            if (pts !== undefined) {
                                t.points = pts;
                            }
                        });
                        // Resort based on live ranking pts
                        teams.sort((a,b) => parseFloat(b.points || 0) - parseFloat(a.points || 0));
                    }
                }
            } catch (e) {
                console.error("Error updating pools with live rankings:", e);
                // Will just fall back to the static points loaded initially
            }
            
            // Re-render
            renderRWCPools();
            renderRWCKnockout();
        }
"""

if "fetchInitialRankingsAndUpdatePools" not in html:
    # insert function
    html = html.replace("        function renderRWCPools() {", inject_code + "\n        function renderRWCPools() {")
    
    # replace static calls at the bottom of the script
    html = html.replace("renderRWCPools();\n                    renderRWCKnockout();", "fetchInitialRankingsAndUpdatePools();")

with open("index.html", "w") as f:
    f.write(html)
