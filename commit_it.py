import urllib.request
import json
import re

with open("index.html", "r") as f:
    html = f.read()

# I see it! Wait! 
#                         teams.forEach(t => {
#                             const mapName = teamNameMap[t.team] || t.team;
#                             let pts = rankingsMap[mapName];
                            
#                             // fallback fuzzy match if needed
#                             if (pts === undefined) {
#                                 for (const [rName, rPts] of Object.entries(rankingsMap)) {
#                                     if (rName.includes(mapName) || mapName.includes(rName)) {
#                                         pts = rPts;
#                                         break;
#                                     }
#                                 }
#                             }
                            
#                             if (pts !== undefined) {
#                                 t.rankingPts = parseFloat(pts); 
#                             } else {
#                                 console.log('Could not find ranking for', mapName);
#                             }
#                         });
# THEN: 
#                     });
#                 }
# It seems my logic replacement of `rwcPoolsData` from `window.rwcPoolsData` worked properly!
