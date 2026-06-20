import re

with open("index.html", "r") as f:
    text = f.read()

toggle_script = """
        // Easy toggle for multiple selects without holding Cmd/Ctrl
        document.addEventListener('mousedown', function(e) {
            if (e.target.tagName === 'OPTION' && e.target.closest('select[multiple]')) {
                e.preventDefault();
                
                const select = e.target.closest('select[multiple]');
                const isAllClick = e.target.value === 'ALL';
                
                if (isAllClick) {
                    Array.from(select.options).forEach(opt => opt.selected = false);
                    e.target.selected = true;
                } else {
                    const allOption = Array.from(select.options).find(opt => opt.value === 'ALL');
                    if (allOption && e.target.selected === false) {
                        allOption.selected = false;
                    }
                    e.target.selected = !e.target.selected;
                    
                    if (select.selectedOptions.length === 0 && allOption) {
                        allOption.selected = true;
                    }
                }
                
                // Keep focus on select so people can scroll it with keyboard if needed
                select.focus();
                select.dispatchEvent(new Event('change'));
            }
        });
"""

# Insert right after fetchFixtures() definition or DOMContentLoaded
target = """    <script>
"""
replacement = target + toggle_script

if target in text:
    text = text.replace(target, replacement, 1)
else:
    print("Could not find script tag to inject toggle behavior!")

with open("index.html", "w") as f:
    f.write(text)

