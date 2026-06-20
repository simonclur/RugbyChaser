import re

with open("index.html", "r") as f:
    text = f.read()

# I will replace the start of renderMatches up to matchesToRender.forEach
pattern = re.compile(r"        function renderMatches\(\) \{.*?(?=            matchesToRender\.forEach\()", re.DOTALL)

new_code = """        function renderMatches() {
            const container = document.getElementById('matches-container');
            const offsetH = parseFloat(tzSelect.value);
            const tzLabel = tzSelect.options[tzSelect.selectedIndex].text;
            
            const compSelect = document.getElementById('comp-filter');
            const teamSelect = document.getElementById('team-filter');
            const sportFilter = document.getElementById('sport-filter').value;
            
            // Collect all selected values into arrays
            const selectedComps = Array.from(compSelect.selectedOptions).map(o => o.value);
            const selectedTeams = Array.from(teamSelect.selectedOptions).map(o => o.value);
            
            const filterAllComps = selectedComps.includes('ALL') || selectedComps.length === 0;
            const filterAllTeams = selectedTeams.includes('ALL') || selectedTeams.length === 0;

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
            
            if (sportFilter !== 'ALL') {
                matchesToRender = matchesToRender.filter(m => {
                    const s = m.sport ? m.sport.toUpperCase() : 'UNKNOWN';
                    return s === sportFilter;
                });
            }

            if (!filterAllComps) {
                matchesToRender = matchesToRender.filter(m => {
                    const c = m.events?.[0]?.label || m.competition || 'International Fixture';
                    return selectedComps.includes(c);
                });
            }

"""

text = pattern.sub(new_code, text)

with open("index.html", "w") as f:
    f.write(text)

