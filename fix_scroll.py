import re

with open("index.html", "r") as f:
    text = f.read()

# Make renderMatches optionally accept a skipScroll parameter
old_render = """        function renderMatches() {"""
new_render = """        function renderMatches(skipScroll = false) {"""
text = text.replace(old_render, new_render)

# Call with true when triggered from controls
old_handle_comp = """        function handleCompChange() {
            populateTeamFilter();
            renderMatches();
        }"""
new_handle_comp = """        function handleCompChange() {
            populateTeamFilter();
            renderMatches(true);
        }"""
text = text.replace(old_handle_comp, new_handle_comp)

old_handle_sport = """        function handleSportChange() {
            populateCompFilter();
            populateTeamFilter();
            renderMatches();
        }"""
new_handle_sport = """        function handleSportChange() {
            populateCompFilter();
            populateTeamFilter();
            renderMatches(true);
        }"""
text = text.replace(old_handle_sport, new_handle_sport)

# Update HTML calls
text = text.replace('onchange="renderMatches()"', 'onchange="renderMatches(true)"')

# Don't scroll if skipScroll is true
old_scroll = """            // Auto-scroll to the next/active fixture
            setTimeout(() => {
                const target = document.getElementById('auto-scroll-target');
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            }, 100);"""
new_scroll = """            // Auto-scroll to the next/active fixture
            if (!skipScroll) {
                setTimeout(() => {
                    const target = document.getElementById('auto-scroll-target');
                    if (target) {
                        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    }
                }, 100);
            }"""
text = text.replace(old_scroll, new_scroll)


with open("index.html", "w") as f:
    f.write(text)

