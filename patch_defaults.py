with open('index.html', 'r') as f:
    text = f.read()

# Add global var
old_var = "        let loadedMatchDetails = {};"
new_var = "        let loadedMatchDetails = {};\n        let isInitialUI = true;"
text = text.replace(old_var, new_var)

# Turn off global var in fetchFixtures
old_fetch = """                populateCompFilter();
                populateTeamFilter();
                renderMatches();"""
new_fetch = """                populateCompFilter();
                populateTeamFilter();
                isInitialUI = false;
                renderMatches();"""
text = text.replace(old_fetch, new_fetch)

# Update populateCompFilter
old_comp = """            Array.from(compSet).sort().forEach(c => {
                const opt = new Option(c, c);
                if (currentSelections.includes(c)) opt.selected = true;
                compSelect.add(opt);
            });
            // If all selected options vanished, maybe select ALL
            if (compSelect.selectedOptions.length === 0) compSelect.options[0].selected = true;"""

new_comp = """            const defaultComps = ["Men's Internationals", "Nations Championship", "Six Nations", "Bledisloe Cup", "World Cup", "World Rugby Nations Cup", "Rugby’s Greatest Rivalry"];
            
            Array.from(compSet).sort().forEach(c => {
                const opt = new Option(c, c);
                if (isInitialUI) {
                    if (defaultComps.some(dc => c.includes(dc))) opt.selected = true;
                } else {
                    if (currentSelections.includes(c)) opt.selected = true;
                }
                compSelect.add(opt);
            });
            
            if (isInitialUI) {
                // Deselect ALL initially if we matched any defaults
                if (compSelect.selectedOptions.length > 0) compSelect.options[0].selected = false;
            } else {
                if (compSelect.selectedOptions.length === 0) compSelect.options[0].selected = true;
            }"""
text = text.replace(old_comp, new_comp)

# Update populateTeamFilter
old_team = """            Array.from(teamSet).sort().forEach(t => {
                const opt = new Option(t, t);
                if (currentSelections.includes(t)) opt.selected = true;
                teamSelect.add(opt);
            });"""

new_team = """            Array.from(teamSet).sort().forEach(t => {
                const opt = new Option(t, t);
                if (isInitialUI) {
                    if (t === "South Africa") opt.selected = true;
                } else {
                    if (currentSelections.includes(t)) opt.selected = true;
                }
                teamSelect.add(opt);
            });"""
text = text.replace(old_team, new_team)


with open('index.html', 'w') as f:
    f.write(text)
