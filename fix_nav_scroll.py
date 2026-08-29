import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# I want to inject the JS logic that handles centering the nav tab when clicked
js_logic_old = """
        function openSettingsAndScroll() {
            document.getElementById('settings-collapse').classList.remove('collapsed');
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        }
"""

js_logic_new = """
        function openSettingsAndScroll() {
            document.getElementById('settings-collapse').classList.remove('collapsed');
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        }
        
        // Let's attach an event listener to the bottom nav bar tabs.
        // It will trigger when a nav button is clicked and center it dynamically.
        document.addEventListener('DOMContentLoaded', () => {
            const navTabs = document.querySelectorAll('.bottom-nav .nav-tab');
            const navContainer = document.querySelector('.bottom-nav');
            
            navTabs.forEach(tab => {
                tab.addEventListener('click', function(e) {
                    // Calculate the position to center the clicked tab
                    const containerWidth = navContainer.clientWidth;
                    const tabPosition = this.offsetLeft;
                    const tabWidth = this.offsetWidth;
                    
                    // The target scroll point places the center of the tab at the center of the container
                    const scrollPosition = tabPosition - (containerWidth / 2) + (tabWidth / 2);
                    
                    navContainer.scrollTo({
                        left: scrollPosition,
                        behavior: 'smooth'
                    });
                });
            });
        });
"""

html = html.replace(js_logic_old.strip(), js_logic_new.strip())

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
