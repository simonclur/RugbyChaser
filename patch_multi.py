import re

with open("index.html", "r") as f:
    text = f.read()

# 1. Update HTML elements to be multiselect
old_selects = """                <select id="comp-filter" onchange="renderMatches()"><option value="ALL">All Competitions</option></select>
                <select id="team-filter" onchange="renderMatches()"><option value="ALL">Highlight Team (None)</option></select>"""
new_selects = """                <select id="comp-filter" multiple size="3" onchange="renderMatches()" style="height: 60px;">
                    <option value="ALL" selected>All Competitions</option>
                </select>
                <select id="team-filter" multiple size="3" onchange="renderMatches()" style="height: 60px;">
                    <option value="ALL" selected>Highlight Team (None)</option>
                </select>"""
text = text.replace(old_selects, new_selects)


# 2. Find the renderMatches filtering block and update it for multi-select arrays
old_filter_logic = """        function renderMatches() {
            const container = document.getElementById('matches-container');
            const offsetH = parseFloat(tzSelect.value);
            
            container.innerHTML = '';"""
            
new_filter_logic = """        function renderMatches() {
            const container = document.getElementById('matches-container');
            const offsetH = parseFloat(tzSelect.value);
            
            const compSelect = document.getElementById('comp-filter');
            const teamSelect = document.getElementById('team-filter');
            
            // Collect all selected values into arrays
            const selectedComps = Array.from(compSelect.selectedOptions).map(o => o.value);
            const selectedTeams = Array.from(teamSelect.selectedOptions).map(o => o.value);
            
            // If user selects specific items while 'ALL' was active, remove 'ALL' (unless they specifically clicked ALL to reset)
            // It's simpler to just say: if 'ALL' is part of the array, ignore the others and default to all.
            const filterAllComps = selectedComps.includes('ALL') || selectedComps.length === 0;
            const filterAllTeams = selectedTeams.includes('ALL') || selectedTeams.length === 0;

            container.innerHTML = '';"""
text = text.replace(old_filter_logic, new_filter_logic)


# Right after liveMatchesToLoad = []; in renderMatches()
old_match_assignment = """            let currentComp = '';
            let currentDate = '';
            let foundNextUpcoming = false;
            let liveMatchesToLoad = [];

            allMatches.forEach(match => {"""
            
new_match_assignment = """            let currentComp = '';
            let currentDate = '';
            let foundNextUpcoming = false;
            let liveMatchesToLoad = [];

            let matchesToRender = allMatches;
            if (!filterAllComps) {
                matchesToRender = matchesToRender.filter(m => {
                    const c = m.events?.[0]?.label || m.competition || 'International Fixture';
                    return selectedComps.includes(c);
                });
            }

            matchesToRender.forEach(match => {"""
text = text.replace(old_match_assignment, new_match_assignment)


# In the card rendering logic
old_highlight = """                const badgeClass = isNextScheduled ? 'N' : status;

                if (isLive) {"""
new_highlight = """                const badgeClass = isNextScheduled ? 'N' : status;

                const involvesTeam = !filterAllTeams && (selectedTeams.includes(match.teams[0].name) || selectedTeams.includes(match.teams[1].name));
                const highlightClass = involvesTeam ? 'highlighted-team' : '';

                if (isLive) {"""
text = text.replace(old_highlight, new_highlight)


# Final UI class injection
old_html_card = """                    html += `
                        <div class="match-card ${statusClass}">
                            <div class="match-primary-content">"""
new_html_card = """                    html += `
                        <div class="match-card ${statusClass} ${highlightClass}">
                            <div class="match-primary-content">"""
text = text.replace(old_html_card, new_html_card)

with open("index.html", "w") as f:
    f.write(text)
