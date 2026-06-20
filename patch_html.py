import re

with open("index.html", "r") as f:
    text = f.read()

old_html = """                } else {
                    html += `
                        <div class="match-card ${statusClass}">
                            <div class="match-main">
                                <div class="match-meta">
                                    ${match.venue?.name || 'TBA'}, ${match.venue?.city || ''}
                                </div>
                                <div class="match-teams">
                                    <div class="team-row">
                                        <div class="team-name">${match.teams[0].name}</div>
                                        <div class="team-score">${isUpcoming && !isLive ? '-' : match.scores[0]}</div>
                                    </div>
                                    <div class="team-row">
                                        <div class="team-name">${match.teams[1].name}</div>
                                        <div class="team-score">${isUpcoming && !isLive ? '-' : match.scores[1]}</div>
                                    </div>
                                </div>
                            </div>
                            <div class="match-status status-badge ${badgeClass}">
                                ${statusLabel}
                            </div>
                        </div>
                    `;
                }"""

new_html = """                } else {
                    html += `
                        <div class="match-card ${statusClass}">
                            <div class="match-primary-content">
                                <div class="match-main">
                                    <div class="match-meta">
                                        ${match.venue?.name || 'TBA'}, ${match.venue?.city || ''}
                                    </div>
                                    <div class="match-teams">
                                        <div class="team-row">
                                            <div class="team-name">${match.teams[0].name}</div>
                                            <div class="team-score">${isUpcoming && !isLive ? '-' : match.scores[0]}</div>
                                        </div>
                                        <div class="team-row">
                                            <div class="team-name">${match.teams[1].name}</div>
                                            <div class="team-score">${isUpcoming && !isLive ? '-' : match.scores[1]}</div>
                                        </div>
                                    </div>
                                </div>
                                <div class="match-status status-badge ${badgeClass}">
                                    ${statusLabel}
                                </div>
                            </div>
                            <div style="flex-basis: 100%;">
                                <div class="see-more-badge" id="badge-${match.matchId}" onclick="toggleMatchDetails('${match.matchId}')">See more</div>
                            </div>
                            <div class="extended-container" id="extended-${match.matchId}">
                                <div style="text-align:center; color: var(--muted-text);">Loading details...</div>
                            </div>
                        </div>
                    `;
                }"""

text = text.replace(old_html, new_html)

js_injection_point = "        // Initialize theme"
js_new = """        const loadedMatchDetails = {};
        const preloadedMatchDetails = {};

        async function prefetchMatchDetails(matchId) {
            if (preloadedMatchDetails[matchId] || loadedMatchDetails[matchId]) return;
            try {
                const res = await fetch(`https://api.wr-rims-prod.pulselive.com/rugby/v3/match/${matchId}/summary`);
                if (res.ok) {
                    preloadedMatchDetails[matchId] = await res.json();
                }
            } catch(e) {}
        }

        async function toggleMatchDetails(matchId) {
            const badge = document.getElementById(`badge-${matchId}`);
            const container = document.getElementById(`extended-${matchId}`);
            
            if (container.style.display === 'block') {
                container.style.display = 'none';
                badge.textContent = 'See more';
                return;
            }

            container.style.display = 'block';
            badge.textContent = 'See less';

            if (loadedMatchDetails[matchId]) return;

            try {
                let summaryData = preloadedMatchDetails[matchId];
                if (!summaryData) {
                    const cacheBust = Date.now();
                    const summaryRes = await fetch(`https://api.wr-rims-prod.pulselive.com/rugby/v3/match/${matchId}/summary?t=${cacheBust}`);
                    if (summaryRes.ok) {
                        summaryData = await summaryRes.json();
                    }
                }

                if (summaryData && summaryData.teams && summaryData.teams.length > 0) {
                    let html = `<div class="live-lineups">`;
                    [0, 1].forEach(tIdx => {
                        const tm = summaryData.teams[tIdx];
                        html += `<div class="lineup-team"><h4>${tm ? tm.name || 'Team ' + (tIdx+1) : 'Team ' + (tIdx+1)}</h4>`;
                        
                        if (tm && tm.teamList && tm.teamList.list && tm.teamList.list.length > 0) {
                            // Splitting into starting and reserves
                            const starters = tm.teamList.list.filter(p => !p.player.isReplacement).sort((a,b) => parseInt(a.number||0) - parseInt(b.number||0));
                            const reserves = tm.teamList.list.filter(p => p.player.isReplacement).sort((a,b) => parseInt(a.number||0) - parseInt(b.number||0));
                            
                            html += `<strong>Starting</strong>`;
                            if (starters.length > 0) {
                                starters.forEach(p => {
                                    html += `<div class="player-row">
                                        <div class="player-num">${p.number || ''}</div>
                                        <div>${p.player.name.display}</div>
                                    </div>`;
                                });
                            } else {
                                html += `<div style="color: var(--muted-text);">Not announced</div>`;
                            }

                            html += `<strong style="display:block; margin-top:10px;">Reserves</strong>`;
                            if (reserves.length > 0) {
                                reserves.forEach(p => {
                                    html += `<div class="player-row">
                                        <div class="player-num">${p.number || ''}</div>
                                        <div>${p.player.name.display}</div>
                                    </div>`;
                                });
                            } else {
                                html += `<div style="color: var(--muted-text);">Not announced</div>`;
                            }

                        } else {
                            html += `<div style="text-align:center; color: var(--muted-text);">Lineup not available</div>`;
                        }
                        html += `</div>`;
                    });
                    html += `</div>`;
                    container.innerHTML = html;
                    loadedMatchDetails[matchId] = true;
                } else {
                    container.innerHTML = `<div style="text-align:center; color: var(--muted-text);">Match details not available</div>`;
                    loadedMatchDetails[matchId] = true;
                }

            } catch (e) {
                container.innerHTML = `<div style="text-align:center; color: var(--live-color);">Failed to load details</div>`;
            }
        }

        // Initialize theme"""

text = text.replace(js_injection_point, js_new)


# Now hook the prefetch logic into renderMatches
old_render_matches_end = """            // Trigger async fetches for live matches after DOM is updated
            liveMatchesToLoad.forEach(lm => loadLiveMatchDetails(lm.id, lm.compName, lm.venueName));

            // Auto-scroll to the next/active fixture"""

new_render_matches_end = """            // Trigger async fetches for live matches after DOM is updated
            liveMatchesToLoad.forEach(lm => loadLiveMatchDetails(lm.id, lm.compName, lm.venueName));

            // Auto-scroll to the next/active fixture
            setTimeout(() => {
                const target = document.getElementById('auto-scroll-target');
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            }, 100);

            // Trigger prefetch for next 3 upcoming matches
            let prefetchedCount = 0;
            for (let match of allMatches) {
                if (match.status === 'U' && getMatchStatus(match) !== 'L') {
                    prefetchMatchDetails(match.matchId);
                    prefetchedCount++;
                    if (prefetchedCount >= 3) break;
                }
            }"""

# Remove the old setTimeout as we inject it together
text = text.replace("""            // Auto-scroll to the next/active fixture
            setTimeout(() => {
                const target = document.getElementById('auto-scroll-target');
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            }, 100);""", "")


text = text.replace("""            // Trigger async fetches for live matches after DOM is updated
            liveMatchesToLoad.forEach(lm => loadLiveMatchDetails(lm.id, lm.compName, lm.venueName));

            // Auto-scroll to the next/active fixture""", new_render_matches_end)

with open("index.html", "w") as f:
    f.write(text)

