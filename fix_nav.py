with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's see what classes we ACTUALLY have for the bottom nav
import re
nav_styles = re.search(r'\.bottom-nav.*?(?=\n\s*\.)', html, re.DOTALL)
if nav_styles:
    print("Found .bottom-nav styles:")
    print(nav_styles.group(0))

nav_item_styles = re.search(r'\.nav-item.*?(?=\n\s*\.)', html, re.DOTALL)
if nav_item_styles:
    print("\nFound .nav-item styles:")
    print(nav_item_styles.group(0))
