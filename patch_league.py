import re

with open("index.html", "r") as f:
    text = f.read()

# 1. Update HTML controls
old_controls = """            <div class="controls" style="flex-wrap: wrap; justify-content: flex-end;">
                <select id="comp-filter" multiple size="3" onchange="renderMatches()" style="height: 60px;">"""
new_controls = """            <div class="controls" style="flex-wrap: wrap; justify-content: flex-end;">
                <select id="sport-filter" onchange="handleSportChange()">
                    <option value="ALL">All Sports</option>
                    <option value="MRU" selected>Men's Rugby Union</option>
                    <option value="WRU">Women's Rugby Union</option>
                    <option value="MRS">Men's Rugby Sevens</option>
                    <option value="WRS">Women's Rugby Sevens</option>
                </select>
                <select id="comp-filter" multiple size="3" onchange="handleCompChange()" style="height: 60px;">"""
text = text.replace(old_controls, new_controls)


# 2. Update populateFilters and handle functions
old_pop = """        function populateFilters() {
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
        }"""

new_pop = """        function handleSportChange() {
            populateCompFilter();
            populateTeamFilter();
            renderMatches();
        }

        function handleCompChange() {
            populateTeamFilter();
            renderMatches();
        }

        function populateCompFilter() {
            const sportFilter = document.getElementById('sport-filter').value;
            const compSelect = document.getElementById('comp-filter');
            
            // save current selection
            const currentSelections = Array.from(compSelect.selectedOptions).map(o => o.value);
            
            compSelect.innerHTML = '<option value="ALL">All Competitions</option>'; // Reset
            
            const compSet = new Set();
            allMatches.forEach(m => {
                const s = m.sport ? m.sport.toUpperCase() : 'UNKNOWN';
                if (sportFilter === 'ALL' || s === sportFilter) {
                    compSet.add(m.events?.[0]?.label || m.competition || 'International Fixture');
                }
            });

            Array.from(compSet).sort().forEach(c => {
                const opt = new Option(c, c);
                if (currentSelections.includes(c)) opt.selected = true;
                compSelect.add(opt);
            });
            // If all selected options vanished, maybe select ALL
            if (compSelect.selectedOptions.length === 0) compSelect.options[0].selected = true;
        }

        function populateTeamFilter() {
            const sportFilter = document.getElementById('sport-filter').value;
            const compSelect = document.getElementById('comp-filter');
            const selectedComps = Array.from(compSelect.selectedOptions).map(o => o.value);
            const filterAllComps = selectedComps.includes('ALL') || selectedComps.length === 0;

            const teamSelect = document.getElementById('team-filter');
            const currentSelections = Array.from(teamSelect.selectedOptions).map(o => o.value);

            teamSelect.innerHTML = '<option value="ALL">Highlight Team (None)</option>';

            const teamSet = new Set();
            allMatches.forEach(m => {
                const s = m.sport ? m.sport.toUpperCase() : 'UNKNOWN';
                if (sportFilter === 'ALL' || s === sportFilter) {
                    const c = m.events?.[0]?.label || m.competition || 'International Fixture';
                    if (filterAllComps || selectedComps.includes(c)) {
                        m.teams.forEach(t => teamSet.add(t.name));
                    }
                }
            });

            Array.from(teamSet).sort().forEach(t => {
                const opt = new Option(t, t);
                if (currentSelections.includes(t)) opt.selected = true;
                teamSelect.add(opt);
            });
            if (teamSelect.selectedOptions.length === 0) teamSelect.options[0].selected = true;
        }"""
text = text.replace(old_pop, new_pop)


# 3. Call split methods instead of monolithic one in fetchFixtures
old_call = """                // Sort ascending chronologically
                allMatches = data.matches.sort((a, b) => a.time.millis - b.time.millis);
                populateFilters();
                renderMatches();"""
new_call = """                // Sort ascending chronologically
                allMatches = data.matches.sort((a, b) => a.time.millis - b.time.millis);
                populateCompFilter();
                populateTeamFilter();
                renderMatches();"""
text = text.replace(old_call, new_call)


# 4. Integrate sport filter into renderMatches
# Find where it assigns matchesToRender and insert sport logic.
old_render_filter = """            let currentComp = '';
            let currentDate = '';
            let foundNextUpcoming = false;
            let liveMatchesToLoad = [];

            let matchesToRender = allMatches;
            if (!filterAllComps) {"""

new_render_filter = """            let currentComp = '';
            let currentDate = '';
            let foundNextUpcoming = false;
            let liveMatchesToLoad = [];

            const sportFilter = document.getElementById('sport-filter').value;

            let matchesToRender = allMatches;
            if (sportFilter !== 'ALL') {
                matchesToRender = matchesToRender.filter(m => {
                    const s = m.sport ? m.sport.toUpperCase() : 'UNKNOWN';
                    return s === sportFilter;
                });
            }

            if (!filterAllComps) {"""

text = text.replace(old_render_filter, new_render_filter)

with open("index.html", "w") as f:
    f.write(text)
