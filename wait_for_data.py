import json

with open("index.html", "r") as f:
    html = f.read()

# I used the wrong replace block AGAIN?! No! `document.addEventListener('DOMContentLoaded', () => {` wasn't even in the file! I see, we don't have DOMContentLoaded in this vanilla app! 
# Let's find out how the app initializes!
