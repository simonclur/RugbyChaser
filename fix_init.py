import json

with open("index.html", "r") as f:
    html = f.read()

# Let's just find the very end of the <script> block and insert our initialization logic!
init_logic = """
        // Initialize settings from localStorage before loading matches
        setTimeout(() => {
            const savedTheme = localStorage.getItem('rugbychaser-theme');
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
            }
            
            if (savedTz || savedSport) {
                if (typeof handleSportChange === "function") handleSportChange();
                if (typeof renderMatches === "function") renderMatches(true);
            }

        }, 100);
"""

# inject right before `</script>`
html = html.replace("</script>", init_logic + "\n    </script>")

with open("index.html", "w") as f:
    f.write(html)
