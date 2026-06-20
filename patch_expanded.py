import re

with open("index.html", "r") as f:
    text = f.read()

# 1. Add summary div and update selects
old_controls = """                <select id="comp-filter" multiple size="3" onchange="handleCompChange()" style="height: 60px;">
                    <option value="ALL" selected>All Competitions</option>
                </select>
                <select id="team-filter" multiple size="3" onchange="renderMatches()" style="height: 60px;">
                    <option value="ALL" selected>Highlight Team (None)</option>
                </select>
                <select id="timezone-select" onchange="renderMatches()"></select>
                <button onclick="toggleTheme()" id="theme-toggle">🌗 Mode</button>
            </div>
        </div>"""

# Ensure the parent .header has position relative or flex that can handle absolute selects
new_controls = """                <div style="position: relative; height: 60px; width: 220px; z-index: 20;">
                    <select id="comp-filter" multiple size="8" onchange="handleCompChange()" 
                            onmouseenter="this.style.height='250px'; this.style.boxShadow='0 4px 12px rgba(0,0,0,0.5)';"
                            onmouseleave="if (document.activeElement !== this) { this.style.height='60px'; this.style.boxShadow='none'; }"
                            onfocus="this.style.height='250px'; this.style.boxShadow='0 4px 12px rgba(0,0,0,0.5)';"
                            onblur="this.style.height='60px'; this.style.boxShadow='none';"
                            style="position: absolute; top:0; left:0; width: 100%; height: 60px; cursor: pointer; transition: height 0.2s ease; border-radius: 6px;">
                        <option value="ALL" selected>All Competitions</option>
                    </select>
                </div>
                <div style="position: relative; height: 60px; width: 220px; z-index: 10;">
                    <select id="team-filter" multiple size="8" onchange="renderMatches()" 
                            onmouseenter="this.style.height='250px'; this.style.boxShadow='0 4px 12px rgba(0,0,0,0.5)';"
                            onmouseleave="if (document.activeElement !== this) { this.style.height='60px'; this.style.boxShadow='none'; }"
                            onfocus="this.style.height='250px'; this.style.boxShadow='0 4px 12px rgba(0,0,0,0.5)';"
                            onblur="this.style.height='60px'; this.style.boxShadow='none';"
                            style="position: absolute; top:0; left:0; width: 100%; height: 60px; cursor: pointer; transition: height 0.2s ease; border-radius: 6px;">
                        <option value="ALL" selected>Highlight Team (None)</option>
                    </select>
                </div>
                <select id="timezone-select" onchange="renderMatches()"></select>
                <button onclick="toggleTheme()" id="theme-toggle">🌗 Mode</button>
            </div>
            <div id="filter-summary" style="width: 100%; text-align: right; padding-top: 10px; font-size: 0.85em; color: var(--muted-text);"></div>
        </div>"""
text = text.replace(old_controls, new_controls)

# 2. Update renderMatches to inject metrics into the new div
old_footer = """            // Trigger prefetch for next 3 upcoming matches
            let prefetchedCount = 0;
            for (let match of matchesToRender) {
                if (match.status === 'U' && getMatchStatus(match) !== 'L') {
                    prefetchMatchDetails(match.matchId);
                    prefetchedCount++;
                    if (prefetchedCount >= 3) break;
                }
            }
        }"""

new_footer = """            // Trigger prefetch for next 3 upcoming matches
            let prefetchedCount = 0;
            for (let match of matchesToRender) {
                if (match.status === 'U' && getMatchStatus(match) !== 'L') {
                    prefetchMatchDetails(match.matchId);
                    prefetchedCount++;
                    if (prefetchedCount >= 3) break;
                }
            }

            // Update dynamically displayed summary information
            const filterSummary = document.getElementById('filter-summary');
            if (filterSummary) {
                const visibleMatches = matchesToRender.length;
                const activeComps = new Set();
                matchesToRender.forEach(m => activeComps.add(m.events?.[0]?.label || m.competition || 'International Fixture'));
                
                let infoArr = [];
                if (filterAllComps) {
                    infoArr.push(`Showing <strong>${visibleMatches}</strong> matches across <strong>${activeComps.size}</strong> competitions`);
                } else {
                    infoArr.push(`Showing <strong>${visibleMatches}</strong> matches in <strong>${selectedComps.length}</strong> selected competition(s)`);
                }

                if (!filterAllTeams) {
                    infoArr.push(`Highlighting <strong>${selectedTeams.length}</strong> team(s)`);
                }
                
                filterSummary.innerHTML = infoArr.join(' | ');
            }
        }"""
text = text.replace(old_footer, new_footer)

with open("index.html", "w") as f:
    f.write(text)

