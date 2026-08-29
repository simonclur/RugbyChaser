import json

with open("index.html", "r") as f:
    html = f.read()

# OH, I see! `rwcPoolsData` is declared at the bottom of the script inside the DOMContentLoaded handler, but `fetchInitialRankingsAndUpdatePools()` is inside that too, OR it's outside. Let's make sure it updates the global variable!
# Wait! "if (window.rwcPoolsData) {" -> rwcPoolsData was populated dynamically using `rwcPoolsData = await poolsRes.json();` ! So `window.rwcPoolsData` doesn't exist, it's just `rwcPoolsData` inside the module context!

html = html.replace("if (window.rwcPoolsData) {", "if (rwcPoolsData) {")

with open("index.html", "w") as f:
    f.write(html)

print("Fixed scope issue!")
