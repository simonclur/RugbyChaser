import json
import re

with open("rwc_pools.json", "r") as f:
    pools_data = f.read()
    
with open("index.html", "r") as f:
    html = f.read()

# Replace the const rwcPoolsData = { ... }; block
html = re.sub(
    r'const rwcPoolsData = {.*?};', 
    f'const rwcPoolsData = {pools_data};', 
    html,
    flags=re.DOTALL
)

with open("index.html", "w") as f:
    f.write(html)
print("Re-injected rwc_pools.json into index.html")
