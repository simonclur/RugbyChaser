import re

with open("index.html", "r") as f:
    text = f.read()

new_css = """        .info-icon {
            cursor: pointer;
            margin-left: 10px;
            background: none; border: none; font-size: 1.2em;
            padding: 0; color: inherit;
        }

        /* Settings Panel */
        .settings-panel {
            display: none;
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            flex-direction: column;
            gap: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        }

        .settings-panel.active {
            display: flex;
        }

        .settings-row {
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
        }

        .settings-group {
            display: flex;
            flex-direction: column;
            flex: 1;
            min-width: 200px;
        }

        .settings-group label {
            font-weight: bold;
            margin-bottom: 8px;
            font-size: 0.9em;
            color: var(--muted-text);
        }

        select[multiple] {
            height: 140px;
            padding: 8px;
            cursor: pointer;
        }
        
        .settings-btn {
            background-color: var(--card-bg);
            color: var(--text-color);
            border: 1px solid var(--card-border);
            display: flex;
            align-items: center;
            gap: 8px;
        }
    </style>"""

text = text.replace("""        .info-icon {
            cursor: pointer;
            margin-left: 10px;
            background: none; border: none; font-size: 1.2em;
            padding: 0; color: inherit;
        }
    </style>""", new_css)



old_html_controls = """        <div class="header">
            <h2>Rugby Internationals</h2>
            <div class="controls" style="flex-wrap: wrap; justify-content: flex-end;">
                <select id="sport-filter" onchange="handleSportChange()">
                    <option value="ALL">All Sports</option>
                    <option value="MRU" selected>Men's Rugby Union</option>
                    <option value="WRU">Women's Rugby Union</option>
                    <option value="MRS">Men's Rugby Sevens</option>
                    <option value="WRS">Women's Rugby Sevens</option>
                </select>
                <div style="position: relative; height: 60px; width: 220px; z-index: 20;">
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

new_html_controls = """        <div class="header">
            <h2>Rugby Internationals</h2>
            <button onclick="toggleSettings()" id="settings-toggle" class="settings-btn">⚙️ Show Settings</button>
        </div>

        <div id="filter-summary" style="width: 100%; text-align: center; margin-bottom: 15px; font-size: 0.9em; font-weight: 500; color: var(--muted-text);"></div>

        <div id="settings-panel" class="settings-panel">
            <div class="settings-row">
                <div class="settings-group">
                    <label>Sport</label>
                    <select id="sport-filter" onchange="handleSportChange()">
                        <option value="ALL">All Sports</option>
                        <option value="MRU" selected>Men's Rugby Union</option>
                        <option value="WRU">Women's Rugby Union</option>
                        <option value="MRS">Men's Rugby Sevens</option>
                        <option value="WRS">Women's Rugby Sevens</option>
                    </select>
                </div>
                <div class="settings-group">
                    <label>Competitions</label>
                    <select id="comp-filter" multiple onchange="handleCompChange()">
                        <option value="ALL" selected>All Competitions</option>
                    </select>
                </div>
                <div class="settings-group">
                    <label>Highlight Teams</label>
                    <select id="team-filter" multiple onchange="renderMatches()">
                        <option value="ALL" selected>Highlight Team (None)</option>
                    </select>
                </div>
            </div>
            <div class="settings-row" style="justify-content: flex-end; align-items: center;">
                <div class="settings-group" style="flex: 0; min-width: auto; margin-right: 15px;">
                    <label>Local Timezone</label>
                    <select id="timezone-select" onchange="renderMatches()"></select>
                </div>
                <div class="settings-group" style="flex: 0; min-width: auto;">
                    <label>Theme</label>
                    <button onclick="toggleTheme()" id="theme-toggle">🌗 Toggle Mode</button>
                </div>
            </div>
        </div>"""
text = text.replace(old_html_controls, new_html_controls)

js_insert = """        function toggleSettings() {
            const panel = document.getElementById('settings-panel');
            const btn = document.getElementById('settings-toggle');
            if (panel.classList.contains('active')) {
                panel.classList.remove('active');
                btn.textContent = '⚙️ Show Settings';
            } else {
                panel.classList.add('active');
                btn.textContent = '⚙️ Hide Settings';
            }
        }

        let liveRefreshIntervals = {};"""

text = text.replace("        let liveRefreshIntervals = {};", js_insert)

with open("index.html", "w") as f:
    f.write(text)

