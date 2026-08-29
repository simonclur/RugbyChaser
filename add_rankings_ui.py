import json

with open("index.html", "r") as f:
    html = f.read()

# We need to add the rankings rendering logic inside the `fetchInitialRankingsAndUpdatePools` function

rankings_js = """
                // --- ADDED: Render Men's Rankings Table ---
                const rankingsSection = document.getElementById('rankings-section');
                if (rankingsSection && data && data.entries) {
                    let tableHTML = `
                    <div style="overflow-x: auto;">
                        <table class="pools-table" style="width: 100%; border-collapse: collapse; margin-top: 10px;">
                            <thead>
                                <tr style="background-color: var(--secondary-bg); text-align: left; font-size: 0.8em; color: var(--muted-text);">
                                    <th style="padding: 8px 12px; width: 40px; text-align:center;">Pos</th>
                                    <th style="padding: 8px 12px;">Team</th>
                                    <th style="padding: 8px 12px; text-align: right;">Pts</th>
                                </tr>
                            </thead>
                            <tbody>
                    `;
                    
                    data.entries.slice(0, 20).forEach((entry, idx) => {
                        if (typeof entry === 'string') return;
                        const name = entry.team.name;
                        const pts = Number(entry.pts).toFixed(2);
                        const pos = entry.pos;
                        const prevPos = entry.previousPos;
                        const flagSrc = getTeamLogoUrl(name);
                        
                        let movSymbol = '';
                        if (prevPos > pos) movSymbol = '<span style="color: #2e7d32; font-size:0.7em;">▲</span>';
                        else if (prevPos < pos) movSymbol = '<span style="color: #c62828; font-size:0.7em;">▼</span>';
                        else movSymbol = '<span style="color: grey; font-size:0.7em;">-</span>';

                        tableHTML += `
                            <tr style="border-bottom: 1px solid var(--card-border); background-color: var(--card-bg);">
                                <td style="padding: 8px 12px; font-weight: bold; text-align:center; font-size: 0.9em; border-right: 1px solid var(--card-border);">${pos} <div style="margin-top:2px;">${movSymbol}</div></td>
                                <td style="padding: 8px 12px; font-weight: 500; display:flex; align-items:center; gap: 8px;">
                                    <img src="${flagSrc}" alt="${name} flag" style="width: 20px; height: 20px; border-radius: 50%; object-fit: cover;" onerror="this.src='https://ui-avatars.com/api/?name=${encodeURIComponent(name || 'TBD')}&background=random&color=fff&bold=true'">
                                    ${name}
                                </td>
                                <td style="padding: 8px 12px; text-align: right; font-weight: 600; color: var(--accent-color);">${pts}</td>
                            </tr>
                        `;
                    });

                    tableHTML += `
                            </tbody>
                        </table>
                        <div style="font-size: 0.7em; color: var(--muted-text); text-align: right; padding: 5px;">Showing Top 20 currently.</div>
                    </div>
                    `;
                    
                    // Replace the loading text wrapper
                    const loader = rankingsSection.querySelector('.match-card');
                    if (loader) {
                        loader.style.padding = '0';
                        loader.style.textAlign = 'left';
                        loader.innerHTML = tableHTML;
                    }
                }
                // --- END Rankings Render ---
"""

target = "                        teams.sort((a,b) => parseFloat(b.points || 0) - parseFloat(a.points || 0));\n                    }\n                }"
if target in html:
    html = html.replace(target, target + "\n" + rankings_js)

with open("index.html", "w") as f:
    f.write(html)
