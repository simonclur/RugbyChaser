import json

with open("index.html", "r") as f:
    html = f.read()

# I used the wrong old logic replacement string!
# Let's fix handleSportChange correctly!

old_sport = """        function handleSportChange() {
            populateCompFilter();
            populateTeamFilter();
            renderMatches(true);
        }"""
new_sport = """        function handleSportChange() {
            localStorage.setItem('rugbychaser-sport', document.getElementById('sport-filter').value);
            populateCompFilter();
            populateTeamFilter();
            renderMatches(true);
        }"""

html = html.replace(old_sport, new_sport)

# Let's find DOMContentLoaded to inject initialization
# Look for "document.addEventListener('DOMContentLoaded'"

old_dom = "document.addEventListener('DOMContentLoaded', () => {"
new_dom = """document.addEventListener('DOMContentLoaded', () => {

        // Initialize settings from localStorage
        const savedTheme = localStorage.getItem('rugbychaser-theme');
        if (savedTheme) {
            document.documentElement.setAttribute('data-theme', savedTheme);
        }

        const savedSport = localStorage.getItem('rugbychaser-sport');
        if (savedSport) {
            document.getElementById('sport-filter').value = savedSport;
        }

        // Wait to assign timezone value until AFTER the dropdown is populated
"""

html = html.replace(old_dom, new_dom)

# Timezone population is:
"""        // Initialize timezone dropdown
        const tzSelect = document.getElementById('timezone-select');
        for (let i = -12; i <= 14; i++) {
...
        }
        tzSelect.value = Math.round(-new Date().getTimezoneOffset() / 60);
"""

old_tz_init = "tzSelect.value = Math.round(-new Date().getTimezoneOffset() / 60);"
new_tz_init = """        const savedTz = localStorage.getItem('rugbychaser-tz');
        if (savedTz) {
            tzSelect.value = savedTz;
        } else {
            tzSelect.value = Math.round(-new Date().getTimezoneOffset() / 60);
        }"""

html = html.replace(old_tz_init, new_tz_init)

with open("index.html", "w") as f:
    f.write(html)
