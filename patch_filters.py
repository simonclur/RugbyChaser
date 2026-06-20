import re

with open("index.html", "r") as f:
    text = f.read()

# 1. Update CSS
old_css = """        .scroll-target {
            scroll-margin-top: 100px;
        }"""
new_css = """        .scroll-target {
            scroll-margin-top: 100px;
        }
        .match-card.highlighted-team {
            border: 2px solid var(--accent-color);
            box-shadow: 0 0 8px var(--accent-color);
            transform: scale(1.02);
            z-index: 5;
            position: relative;
        }"""
text = text.replace(old_css, new_css)

# 2. Update controls HTML
old_controls = """            <div class="controls">
                <select id="timezone-select" onchange="renderMatches()"></select>
                <button onclick="toggleTheme()" id="theme-toggle">🌗 Mode</button>
            </div>"""
new_controls = """            <div class="controls" style="flex-wrap: wrap; justify-content: flex-end;">
                <select id="comp-filter" onchange="renderMatches()"><option value="ALL">All Competitions</option></select>
                <select id="team-filter" onchange="renderMatches()"><option value="ALL">Highlight Team (None)</option></select>
                <select id="timezone-select" onchange="renderMatches()"></select>
                <button onclick="toggleTheme()" id="theme-toggle">🌗 Mode</button>
            </div>"""
text = text.replace(old_controls, new_controls)

# 3. Add populateFilters function
js_injection = """        async function fetchFixtures() {"""
js_new = """        function populateFilters() {
            const compSet = new Set();
            const teamSet = new Set();
            allMatches.forEach(m => {
                compSet.add(m.events?.[0]?.label || m.competition || 'International Fixture');
                m.teams.forEach(t => teamSet.add(t.name));
            });

            const compSelect = document.getElementById('comp-filter');
            Array.from(compSet).sort().forEach(c => {
                compSelect.add(new Option(c, c));
            });

            const teamSelect = document.getElementById('team-filter');
            Array.from(teamSet).sort().forEach(t => {
                teamSelect.add(new Option(t, t));
            });
        }

        async function fetchFixtures() {"""
text = text.replace(js_injection, js_new)

# 4. Call populateFilters after fetch
fetch_sort = """                // Sort ascending chronologically
                allMatches = data.matches.sort((a, b) => a.time.millis - b.time.millis);
                renderMatches();"""
fetch_sort_new = """                // Sort ascending chronologically
                allMatches = data.matches.sort((a, b) => a.time.millis - b.time.millis);
                populateFilters();
                renderMatches();"""
text = text.replace(fetch_sort, fetch_sort_new)

# 5. Update renderMatches to filter and highlight
old_render = """        function renderMatches() {
            const container = document.getElementById('matches-container');
            const offsetH = parseFloat(tzSelect.value);
            
            container.innerHTML = '';
            
            // Clear any active polling intervals before redrawing
            for (let id in liveRefreshIntervals) {
                clearInterval(liveRefreshIntervals[id]);
            }
            liveRefreshIntervals = {};

            let liveHtml = '';
            let nextMatchId = null;
            let foundNext = false;
            let html = '';

            // We need to group by Competition, while retaining Oldest to Last completed order.
            // As per requirements: "lists all fixtures and results, with groupings by competition label... Completed matches should be displayed Oldest to last completed above the current active or next scheduled fixture"
            // The matches are sorted by time.millis ascending.

            let currentComp = '';
            let currentDate = '';
            let foundNextUpcoming = false;
            let liveMatchesToLoad = [];

            allMatches.forEach(match => {"""
new_render = """        function renderMatches() {
            const container = document.getElementById('matches-container');
            const offsetH = parseFloat(tzSelect.value);
            const compFilter = document.getElementById('comp-filter').value;
            const teamFilter = document.getElementById('team-filter').value;
            
            container.innerHTML = '';
            
            // Clear any active polling intervals before redrawing
            for (let id in liveRefreshIntervals) {
                clearInterval(liveRefreshIntervals[id]);
            }
            liveRefreshIntervals = {};

            let liveHtml = '';
            let nextMatchId = null;
            let foundNext = false;
            let html = '';

            let currentComp = '';
            let currentDate = '';
            let foundNextUpcoming = false;
            let liveMatchesToLoad = [];

            let matchesToRender = allMatches;
            if (compFilter !== 'ALL') {
                matchesToRender = matchesToRender.filter(m => {
                    const c = m.events?.[0]?.label || m.competition || 'International Fixture';
                    return c === compFilter;
                });
            }

            matchesToRender.forEach(match => {"""
text = text.replace(old_render, new_render)

old_card = """                    html += `
                        <div class="match-card ${statusClass}">
                            <div class="match-primary-content">"""
new_card = """                    const involvesTeam = teamFilter !== 'ALL' && (match.teams[0].name === teamFilter || match.teams[1].name === teamFilter);
                    const highlightClass = involvesTeam ? 'highlighted-team' : '';
                    html += `
                        <div class="match-card ${statusClass} ${highlightClass}">
                            <div class="match-primary-content">"""
text = text.replace(old_card, new_card)

# Need to also update the for loop at the end of renderMatches where we do prefetch
old_prefetch_loop = """            for (let match of allMatches) {"""
new_prefetch_loop = """            for (let match of matchesToRender) {"""
text = text.replace(old_prefetch_loop, new_prefetch_loop)

with open("index.html", "w") as f:
    f.write(text)

