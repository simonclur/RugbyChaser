import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()


# Add a specific active class to the CSS
css_old = """
        .nav-tab:hover, .nav-tab:active {
            background-color: var(--accent-color);
            color: white;
            border-color: var(--accent-color);
        }
"""

css_new = """
        .nav-tab:hover, .nav-tab:active, .nav-tab.active-section {
            background-color: var(--accent-color);
            color: white;
            border-color: var(--accent-color);
        }
"""
html = html.replace(css_old.strip(), css_new.strip())

# Update the javascript to toggle the class instead of applying inline border
js_old = """
            if (activeTab) {
                // Remove active styling from all (optional, depending on if you want visual feedback)
                navTabs.forEach(t => t.style.borderBottom = 'none');
                
                // Add active styling
                activeTab.style.borderBottom = '2px solid white';
                
                // Calculate centering for the navigation bar itself
"""

js_new = """
            if (activeTab) {
                // Remove active styling from all (optional, depending on if you want visual feedback)
                navTabs.forEach(t => {
                    t.style.borderBottom = 'none';
                    t.classList.remove('active-section');
                });
                
                // Add active styling
                activeTab.classList.add('active-section');
                
                // Calculate centering for the navigation bar itself
"""

html = html.replace(js_old.strip(), js_new.strip())


with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
