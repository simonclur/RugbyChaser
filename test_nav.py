with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re

# Since I just noticed I didn't actually deploy the nav listener block locally earlier due to the git revert `HEAD --hard 0f6e9e3` wipeout, it never existed! Let's inject it cleanly.

js_hook = """
        // Initialize settings from localStorage before loading matches
"""

js_inject = """
        // Let's attach an event listener to the bottom nav bar tabs.
        // It will trigger when a nav button is clicked and center it dynamically until it hits the edges.
        document.addEventListener('DOMContentLoaded', () => {
            const navTabs = document.querySelectorAll('.bottom-nav .nav-tab');
            const navContainer = document.querySelector('.bottom-nav');
            
            navTabs.forEach(tab => {
                tab.addEventListener('click', function(e) {
                    // Get viewport context
                    const containerWidth = navContainer.clientWidth;
                    const scrollWidth = navContainer.scrollWidth;
                    
                    // Calculate positional anchors of the button relative to the flex container
                    const tabPosition = this.offsetLeft;
                    const tabWidth = this.offsetWidth;
                    
                    // Center algorithm mapping exactly to flex constraints
                    let scrollPosition = tabPosition - (containerWidth / 2) + (tabWidth / 2);
                    
                    // Cap bounds logically against flex paddings internally
                    if (scrollPosition < 0) {
                        scrollPosition = 0;
                    } else if (scrollPosition > scrollWidth - containerWidth) {
                        scrollPosition = scrollWidth - containerWidth;
                    }

                    navContainer.scrollTo({
                        left: scrollPosition,
                        behavior: 'smooth'
                    });
                });
            });
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
