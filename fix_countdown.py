import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_countdown_js = """
                    if (diff > 0) {
                        const d = Math.floor(diff / (1000 * 60 * 60 * 24));
                        const h = Math.floor((diff / (1000 * 60 * 60)) % 24);
                        const m = Math.floor((diff / 1000 / 60) % 60);
                        const s = Math.floor((diff / 1000) % 60);
                        
                        let timeParts = [];
                        if (d > 0) timeParts.push(`${d} days`);
                        if (h > 0) timeParts.push(`${h} hours`);
                        // Only show seconds if we're under 24 hours to keep the UI clean
                        if (d === 0) {
                            timeParts.push(`${m} mins`);
                            timeParts.push(`${s} s`);
                        } else {
                            if (m > 0) timeParts.push(`${m} mins`);
                        }
                        
                        el.textContent = `${timeParts.join(' ')}`;
                    } else {
"""

new_countdown_js = """
                    if (diff > 0) {
                        const d = Math.floor(diff / (1000 * 60 * 60 * 24));
                        const h = Math.floor((diff / (1000 * 60 * 60)) % 24);
                        const m = Math.floor((diff / 1000 / 60) % 60);
                        
                        let timeParts = [];
                        if (d > 0) timeParts.push(`${d} days`);
                        if (h > 0) timeParts.push(`${h} hours`);
                        if (m > 0 || (d === 0 && h === 0)) timeParts.push(`${m} mins`);
                        
                        el.textContent = `${timeParts.join(' ')}`;
                    } else {
"""

html = html.replace(old_countdown_js.strip(), new_countdown_js.strip())


with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
