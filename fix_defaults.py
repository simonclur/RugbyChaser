import re

with open("index.html", "r") as f:
    html = f.read()

# Wait, `team-filter` HTML element has an error where its `onchange` accidentally saves to `rugbychaser-tz` instead of executing a function or `rugbychaser-teams`!
old_team_onchange = """<select id="team-filter" multiple onchange="localStorage.setItem('rugbychaser-tz', this.value); renderMatches(true)">"""
new_team_onchange = """<select id="team-filter" multiple onchange="handleTeamChange()">"""
html = html.replace(old_team_onchange, new_team_onchange)

js_teamChange = """
        function handleTeamChange() {
            const teamSelect = document.getElementById('team-filter');
            const selections = Array.from(teamSelect.selectedOptions).map(o => o.value);
            localStorage.setItem('rugbychaser-teams', JSON.stringify(selections));
            renderMatches(true);
        }
"""
html = html.replace("        function populateCompFilter() {", js_teamChange + "\n        function populateCompFilter() {")


# Also handleCompChange needs to save preferences:
old_handleComp = """        function handleCompChange() {
            populateTeamFilter();
            renderMatches(true);
        }"""
new_handleComp = """        function handleCompChange() {
            const compSelect = document.getElementById('comp-filter');
            const selections = Array.from(compSelect.selectedOptions).map(o => o.value);
            localStorage.setItem('rugbychaser-comps', JSON.stringify(selections));
            populateTeamFilter();
            renderMatches(true);
        }"""
html = html.replace(old_handleComp, new_handleComp)

# And now, we need to enforce the INITIAL defaults if nothing is in localStorage yet!
# The user wants default: 
# Sport: MRU 
# Theme: dark
# Tz: 10
# Comps: Bledisloe Cup 2026, Bledisloe Cup 2027, Men's Internationals 2026, Men's Internationals 2027, Nations Championship 2026, Rugby's Greatest Rivalry 2026, Six Nations 2027, Mens Rugby World Cup 2027
# Teams: South Africa

init_settings = """
            let savedTheme = localStorage.getItem('rugbychaser-theme');
            if (!savedTheme) { savedTheme = 'dark'; localStorage.setItem('rugbychaser-theme', 'dark'); }
            if (savedTheme) document.documentElement.setAttribute('data-theme', savedTheme);

            let savedSport = localStorage.getItem('rugbychaser-sport');
            if (!savedSport) { savedSport = 'MRU'; localStorage.setItem('rugbychaser-sport', 'MRU'); }
            if (savedSport) {
                const sportElem = document.getElementById('sport-filter');
                if (sportElem) sportElem.value = savedSport;
            }

            let savedTz = localStorage.getItem('rugbychaser-tz');
            if (!savedTz) { savedTz = '10'; localStorage.setItem('rugbychaser-tz', '10'); }
            if (savedTz) {
                const tzElem = document.getElementById('timezone-select');
                if (tzElem) tzElem.value = savedTz;
            }

            let savedComps = localStorage.getItem('rugbychaser-comps');
            if (!savedComps) {
                savedComps = JSON.stringify([
                    "Bledisloe Cup 2026", "Bledisloe Cup 2027", "Men's Internationals 2026", 
                    "Men's Internationals 2027", "Nations Championship 2026", 
                    "Rugby's Greatest Rivalry 2026", "Six Nations 2027", "Men's Rugby World Cup 2027"
                ]); 
                localStorage.setItem('rugbychaser-comps', savedComps); 
            }
            
            let savedTeams = localStorage.getItem('rugbychaser-teams');
            if (!savedTeams) { 
                savedTeams = JSON.stringify(['South Africa']); 
                localStorage.setItem('rugbychaser-teams', savedTeams); 
            }
"""

# Now, we must ALSO update loadJsonData to actually apply those selections when populating
# The `populateCompFilter()` function saves `const currentSelections = Array.from(compSelect.selectedOptions).map(o => o.value);`
# Let's override populateCompFilter to ALSO check localStorage.
old_populate_comp = """            // save current selection
            const currentSelections = Array.from(compSelect.selectedOptions).map(o => o.value);"""
new_populate_comp = """            // save current selection
            let currentSelections = Array.from(compSelect.selectedOptions).map(o => o.value);
            if (currentSelections.length === 0 || currentSelections[0] === 'ALL') {
                const saved = localStorage.getItem('rugbychaser-comps');
                if (saved) {
                    try { currentSelections = JSON.parse(saved); } catch (e) {}
                }
            }"""
html = html.replace(old_populate_comp, new_populate_comp)

old_populate_teams = """            const currentSelections = Array.from(teamSelect.selectedOptions).map(o => o.value);"""
new_populate_teams = """            let currentSelections = Array.from(teamSelect.selectedOptions).map(o => o.value);
            if (currentSelections.length === 0 || currentSelections[0] === 'ALL') {
                const saved = localStorage.getItem('rugbychaser-teams');
                if (saved) {
                    try { currentSelections = JSON.parse(saved); } catch (e) {}
                }
            }"""
html = html.replace(old_populate_teams, new_populate_teams)


# Finally replace the simplistic init timeout logic I wrote with the actual fallback defaults!
# `const savedTheme = localStorage.getItem('rugbychaser-theme');`
old_timeout_init = """            const savedTheme = localStorage.getItem('rugbychaser-theme');
            if (savedTheme) {
                document.documentElement.setAttribute('data-theme', savedTheme);
            }

            const savedSport = localStorage.getItem('rugbychaser-sport');
            if (savedSport) {
                const sportElem = document.getElementById('sport-filter');
                if (sportElem) sportElem.value = savedSport;
            }

            const savedTz = localStorage.getItem('rugbychaser-tz');
            if (savedTz) {
                const tzElem = document.getElementById('timezone-select');
                if (tzElem) tzElem.value = savedTz;
            }"""

html = html.replace(old_timeout_init, init_settings.strip())

with open("index.html", "w") as f:
    f.write(html)
print("Updated defaults and logic!")
