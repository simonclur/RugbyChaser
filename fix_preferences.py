import re

with open("index.html", "r") as f:
    html = f.read()

# 1. Update toggleTheme to save to localStorage
new_theme = """        function toggleTheme() {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('rugbychaser-theme', newTheme);
        }"""
html = re.sub(r'        function toggleTheme\(\) \{.*?\}\n', new_theme + '\n', html, flags=re.DOTALL)

# 2. Update handleSportChange to save to localStorage
# Let's find handleSportChange
old_handle_sport = """        function handleSportChange() {
            // Need to reload data to apply team mapping based on selected sport
            loadJsonData();
        }"""
new_handle_sport = """        function handleSportChange() {
            const val = document.getElementById('sport-filter').value;
            localStorage.setItem('rugbychaser-sport', val);
            // Need to reload data to apply team mapping based on selected sport
            loadJsonData();
        }"""
html = html.replace(old_handle_sport, new_handle_sport)

# 3. Update timezone-select onchange behaviour to save to localStorage
# Is there a function for tz select? Inside HTML: `onchange="renderMatches(true)"`
# Let's override it to save first, then renderMatches.
html = html.replace('onchange="renderMatches(true)"', 'onchange="localStorage.setItem(\'rugbychaser-tz\', this.value); renderMatches(true)"')

# 4. Apply preferences on load
init_js = """        // Initialize settings from localStorage
        const savedTheme = localStorage.getItem('rugbychaser-theme');
        if (savedTheme) {
            document.documentElement.setAttribute('data-theme', savedTheme);
        }

        const savedSport = localStorage.getItem('rugbychaser-sport');
        if (savedSport) {
            document.getElementById('sport-filter').value = savedSport;
        }

        const savedTz = localStorage.getItem('rugbychaser-tz');
        if (savedTz) {
            document.getElementById('timezone-select').value = savedTz;
        }
"""
# Where to inject this? Right before `try { loadJsonData();` in DOMContentLoaded ?
# Let's look for how `loadJsonData` is called.

with open("index.html", "w") as f:
    f.write(html)

print("Injected localStorage savers!")
