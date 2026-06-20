with open('index.html', 'r') as f:
    text = f.read()

# CSS adjustments
css_to_add = """
        .live-details {
            display: grid;
            grid-template-columns: 2fr 1.5fr;
            gap: 20px;
        }
        @media (max-width: 768px) {
            .live-details { grid-template-columns: 1fr; }
        }
        .match-timeline-container {
            font-size: 0.85em;
            background: var(--bg-color);
            padding: 15px;
            border-radius: 8px;
            max-height: 400px;
            overflow-y: auto;
            text-align: left;
        }
        .timeline-event {
            display: flex;
            align-items: flex-start;
            margin-bottom: 12px;
            padding-bottom: 12px;
            border-bottom: 1px solid var(--border-color);
        }
        .timeline-event:last-child {
            border-bottom: none;
            margin-bottom: 0;
            padding-bottom: 0;
        }
        .timeline-time {
            width: 45px;
            font-weight: bold;
            color: var(--live-color);
        }
        .timeline-content {
            flex: 1;
        }
        .timeline-team {
            font-size: 0.8em;
            color: var(--muted-text);
            text-transform: uppercase;
        }
"""
text = text.replace(".live-lineups {", css_to_add + "        .live-lineups {")

# JS replacements
old_js_start = """                if (summaryData && summaryData.teams && summaryData.teams.length > 0) {
                    let html = `<div class="live-lineups">`;"""
new_js_start = """                let timelineEvents = [];
                try {
                    const tlRes = await fetch(`https://api.wr-rims-prod.pulselive.com/rugby/v3/match/${matchId}/timeline?t=${cacheBust}`);
                    if (tlRes.ok) {
                        const tlData = await tlRes.json();
                        if (tlData && tlData.timeline) {
                            timelineEvents = tlData.timeline.sort((a,b) => (a.time?.secs || 0) - (b.time?.secs || 0));
                        }
                    }
                } catch(e) {}

                if (summaryData && summaryData.teams && summaryData.teams.length > 0) {
                    const playerMap = {};
                    const teamNames = [];
                    [0, 1].forEach(tIdx => {
                        const tm = summaryData.teams[tIdx];
                        if (tm) {
                            teamNames[tIdx] = tm.name || 'Team ' + (tIdx+1);
                            if (tm.teamList?.list) {
                                tm.teamList.list.forEach(p => {
                                    playerMap[p.player?.id] = p.player?.name?.display || 'Unknown Player';
                                });
                            }
                        }
                    });

                    let html = `<div class="live-details"><div class="live-lineups">`;"""
text = text.replace(old_js_start, new_js_start)

old_js_end = """                        html += `</div>`;
                    });
                    html += `</div>`;
                    container.innerHTML = html;
                    loadedMatchDetails[matchId] = true;"""
new_js_end = """                        html += `</div>`;
                    });
                    html += `</div>`;
                    
                    // Build timeline DOM
                    html += `<div class="match-timeline-container"><h4>Match Events</h4>`;
                    if (timelineEvents.length > 0) {
                        timelineEvents.forEach(ev => {
                            const timeLabel = ev.time?.label || "00:00";
                            const pName = ev.playerId ? (playerMap[ev.playerId] || 'Unknown Player') : '';
                            const tName = (ev.teamIndex === 0 || ev.teamIndex === 1) ? teamNames[ev.teamIndex] : '';
                            
                            html += `<div class="timeline-event">
                                <div class="timeline-time">${timeLabel}</div>
                                <div class="timeline-content">
                                    <strong>${ev.typeLabel || ev.type}</strong>
                                    ${pName ? `<div>${pName}</div>` : ''}
                                    ${tName ? `<div class="timeline-team">${tName}</div>` : ''}
                                </div>
                            </div>`;
                        });
                    } else {
                        html += `<div style="color: var(--muted-text);">No events recorded yet.</div>`;
                    }
                    html += `</div></div>`; // close match-timeline-container and live-details
                    
                    container.innerHTML = html;
                    loadedMatchDetails[matchId] = true;"""
text = text.replace(old_js_end, new_js_end)

with open('index.html', 'w') as f:
    f.write(text)
