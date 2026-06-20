import re

with open("index.html", "r") as f:
    html = f.read()

pattern = re.compile(
    r"(async function loadLiveMatchDetails\(matchId, compName, venueName\) \{.*?\})(?=\s*function renderMatches\(\))",
    re.DOTALL
)

replacement = """async function loadLiveMatchDetails(matchId, compName, venueName) {
            const targetContainer = document.getElementById(`live-details-${matchId}`);
            if (!targetContainer) return;

            // Clear any existing poller
            if (liveRefreshIntervals[matchId]) {
                clearInterval(liveRefreshIntervals[matchId]);
            }

            const activeMatch = allMatches.find(m => m.matchId === matchId);
            const { dateString, timeString } = formatDateTime(activeMatch.time.millis, parseFloat(document.getElementById('timezone-select').value));
            const koDisplay = `${dateString} ${timeString}`;

            // Show loading initially
            targetContainer.innerHTML = `
                <div class="spotlight" style="margin-bottom: 10px;">
                    <div class="spotlight-title">LIVE MATCH <button class="info-icon" onclick="openInfoPanel()">ℹ️</button></div>
                    <p>Loading live match data for ${compName}...</p>
                </div>
            `;

            async function fetchDataAndUpdate() {
                try {
                    document.getElementById('info-api-status').textContent = 'Fetching...';
                    document.getElementById('info-api-status').style.color = 'inherit';
                    
                    const cacheBust = Date.now();
                    const [matchRes, statsRes, summaryRes] = await Promise.all([
                        fetch(`https://api.wr-rims-prod.pulselive.com/rugby/v3/match/${matchId}?t=${cacheBust}`),
                        fetch(`https://api.wr-rims-prod.pulselive.com/rugby/v3/match/${matchId}/stats?t=${cacheBust}`).catch(() => null),
                        fetch(`https://api.wr-rims-prod.pulselive.com/rugby/v3/match/${matchId}/summary?t=${cacheBust}`).catch(() => null)
                    ]);

                    document.getElementById('info-last-refresh').textContent = new Date().toLocaleTimeString();
                    if (matchRes.ok) {
                        document.getElementById('info-api-status').textContent = 'OK';
                        document.getElementById('info-api-status').style.color = 'var(--next-color)';
                    } else {
                        throw new Error('API Error');
                    }

                    const mData = await matchRes.json();
                    let statsData = null, summaryData = null;
                    
                    if (statsRes && statsRes.ok) statsData = await statsRes.json();
                    if (summaryRes && summaryRes.ok) summaryData = await summaryRes.json();

                    const clock = mData.clock ? mData.clock.label : "00:00";
                    const t1 = mData.teams[0];
                    const t2 = mData.teams[1];
                    
                    let html = `
                        <div class="spotlight" style="margin-bottom: 10px;">
                            <div class="spotlight-title">LIVE MATCH <button class="info-icon" onclick="openInfoPanel()" title="System Info">ℹ️</button></div>
                            <div class="match-meta" style="text-align: center;">
                                ${compName} | ${venueName}
                            </div>
                            <div class="match-meta" style="text-align: center; margin-top: 5px; font-weight: bold; color: var(--live-color);">
                                Kick-off: ${koDisplay}
                            </div>
                            <div class="live-clock">${clock}</div>
                            <div class="live-scoreline">
                                <div style="flex:1; text-align:right">${t1.name}</div>
                                <div style="font-size: 1.2em; background: var(--bg-color); padding: 5px 15px; border-radius: 6px;">
                                    ${mData.scores[0]} - ${mData.scores[1]}
                                </div>
                                <div style="flex:1; text-align:left">${t2.name}</div>
                            </div>
                    `;

                    // Stats Section
                    if (statsData && statsData.teamStats && statsData.teamStats.length > 0) {
                        const st1 = statsData.teamStats[0].stats || {};
                        const st2 = statsData.teamStats.length > 1 ? statsData.teamStats[1].stats || {} : {};
                        
                        const statKeys = [
                            {key: 'Tries', label: 'Tries'},
                            {key: 'PenaltiesConceded', label: 'Penalties'},
                            {key: 'Carries', label: 'Carries'},
                            {key: 'Tackles', label: 'Tackles'},
                            {key: 'CleanBreaks', label: 'Clean Breaks'}
                        ];

                        html += `<div class="live-stats">`;
                        statKeys.forEach(s => {
                            const v1 = st1[s.key] ?? '-';
                            const v2 = st2[s.key] ?? '-';
                            html += `
                                <div class="live-stat-row">
                                    <div class="stat-val-home">${v1}</div>
                                    <div class="stat-label">${s.label}</div>
                                    <div class="stat-val-away">${v2}</div>
                                </div>
                            `;
                        });
                        html += `</div>`;
                    }

                    // Lineups Section
                    if (summaryData && summaryData.teams && summaryData.teams.length > 0) {
                        html += `<div class="live-lineups">`;
                        [0, 1].forEach(tIdx => {
                            const tm = summaryData.teams[tIdx];
                            const tObj = tIdx === 0 ? t1 : t2;
                            html += `<div class="lineup-team"><h4>${tObj.name}</h4>`;
                            
                            if (tm && tm.teamList && tm.teamList.list) {
                                // Filter only starting 15 (position !== Rep)
                                const starters = tm.teamList.list.filter(p => !p.player.isReplacement).sort((a,b) => parseInt(a.number||0) - parseInt(b.number||0));
                                if (starters.length > 0) {
                                    starters.forEach(p => {
                                        html += `<div class="player-row">
                                            <div class="player-num">${p.number || ''}</div>
                                            <div>${p.player.name.display}</div>
                                        </div>`;
                                    });
                                } else {
                                    html += `<div style="text-align:center; color: var(--muted-text);">Lineup not available</div>`;
                                }
                            } else {
                                html += `<div style="text-align:center; color: var(--muted-text);">Lineup not available</div>`;
                            }
                            html += `</div>`;
                        });
                        html += `</div>`;
                    }

                    html += `</div>`;
                    targetContainer.innerHTML = html;
                } catch(e) {
                    document.getElementById('info-api-status').textContent = 'Failed';
                    document.getElementById('info-api-status').style.color = 'var(--live-color)';
                    targetContainer.innerHTML = `<div class="spotlight"><div class="spotlight-title">LIVE MATCH <button class="info-icon" onclick="openInfoPanel()" title="System Info">ℹ️</button></div><p>Failed to load live tracking data.</p></div>`;
                }
            }
            
            // Execute initially
            await fetchDataAndUpdate();
            // Then poll every 60s
            liveRefreshIntervals[matchId] = setInterval(fetchDataAndUpdate, 60000);
        }"""

new_html = pattern.sub(replacement, html)

with open("index.html", "w") as f:
    f.write(new_html)

