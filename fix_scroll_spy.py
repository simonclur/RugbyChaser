import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add ID targets to all sections that map directly to their nav tab link
html = html.replace("""<a href="javascript:void(0)" onclick="openSettingsAndScroll()" class="nav-tab">⚙️ Settings</a>""", """<a href="javascript:void(0)" onclick="openSettingsAndScroll()" class="nav-tab" data-target="settings-collapse">⚙️ Settings</a>""")
html = html.replace("""<a href="javascript:void(0)" onclick="document.getElementById('auto-scroll-target')?.scrollIntoView({behavior: 'smooth', block: 'start'})" class="nav-tab">Live/Next</a>""", """<a href="javascript:void(0)" onclick="document.getElementById('auto-scroll-target')?.scrollIntoView({behavior: 'smooth', block: 'start'})" class="nav-tab" data-target="matches-container">Live/Next</a>""")
html = html.replace("""<a href="#rankings-section" class="nav-tab">Rankings</a>""", """<a href="#rankings-section" class="nav-tab" data-target="rankings-section">Rankings</a>""")
html = html.replace("""<a href="#countdown-section" class="nav-tab">Countdown</a>""", """<a href="#countdown-section" class="nav-tab" data-target="countdown-section">Countdown</a>""")
html = html.replace("""<a href="#groups-section" class="nav-tab">Pools</a>""", """<a href="#groups-section" class="nav-tab" data-target="groups-section">Pools</a>""")
html = html.replace("""<a href="#knockout-section" class="nav-tab">Knockout</a>""", """<a href="#knockout-section" class="nav-tab" data-target="knockout-section">Knockout</a>""")
html = html.replace("""<a href="#points-section" class="nav-tab">Top Scorers</a>""", """<a href="#points-section" class="nav-tab" data-target="points-section">Top Scorers</a>""")
html = html.replace("""<a href="#all-time-points-section" class="nav-tab">All Time</a>""", """<a href="#all-time-points-section" class="nav-tab" data-target="all-time-points-section">All Time</a>""")


# Add the ScrollSpy Event Logic
js_hook = """
        // Initialize settings from localStorage before loading matches
"""

js_inject = """
        // ScrollSpy logic to dynamically center nav bar buttons as user scrolls
        document.addEventListener('scroll', () => {
            const navTabs = document.querySelectorAll('.bottom-nav .nav-tab');
            const navContainer = document.querySelector('.bottom-nav');
            
            let activeTab = null;
            let currentMinDistance = window.innerHeight; // threshold

            // Iterate over all tabs to check which section is most central to viewport
            navTabs.forEach(tab => {
                const targetId = tab.getAttribute('data-target');
                if (targetId) {
                    const section = document.getElementById(targetId);
                    if (section) {
                        const rect = section.getBoundingClientRect();
                        
                        // Calculate center of section relative to center of viewport
                        const viewportCenter = window.innerHeight / 2;
                        const sectionCenter = rect.top + (rect.height / 2);
                        
                        const distanceToCenter = Math.abs(viewportCenter - sectionCenter);
                        
                        // We check if the section is taking up a significant portion of the screen (top is above center and bottom is below)
                        // OR if it's the closest to the center
                        if ((rect.top <= viewportCenter && rect.bottom >= viewportCenter) || distanceToCenter < currentMinDistance) {
                            currentMinDistance = distanceToCenter;
                            activeTab = tab;
                        }
                    }
                }
            });

            if (activeTab) {
                // Remove active styling from all (optional, depending on if you want visual feedback)
                navTabs.forEach(t => t.style.borderBottom = 'none');
                
                // Add active styling
                activeTab.style.borderBottom = '2px solid white';
                
                // Calculate centering for the navigation bar itself
                const containerWidth = navContainer.clientWidth;
                const scrollWidth = navContainer.scrollWidth;
                const tabPosition = activeTab.offsetLeft;
                const tabWidth = activeTab.offsetWidth;
                
                let scrollPosition = tabPosition - (containerWidth / 2) + (tabWidth / 2);
                
                if (scrollPosition < 0) {
                    scrollPosition = 0;
                } else if (scrollPosition > scrollWidth - containerWidth) {
                    scrollPosition = scrollWidth - containerWidth;
                }

                // Use smooth scrolling, but debounced inherently by the browser's scroll handling 
                navContainer.scrollTo({
                    left: scrollPosition,
                    behavior: 'smooth'
                });
            }
        });

        // Initialize settings from localStorage before loading matches
"""

if js_hook in html:
    html = html.replace(js_hook, js_inject)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Injected cleanly.")
else:
    print("Oops, anchor not found.")
