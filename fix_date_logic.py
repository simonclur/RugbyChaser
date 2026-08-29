import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# I need to see exactly what values are parsed out of `match` directly!
old_logic = """
                // Detect TBC matches (midnight UTC returning 0.0 offset from API)
                const d = new Date(match.time.millis);
                const isTbc = d.getUTCHours() === 0 && d.getUTCMinutes() === 0 && venueOffset === 0;
"""

new_logic = """
                // Detect TBC matches (midnight UTC returning 0.0 offset from API)
                const d = new Date(match.time.millis);
                const isTbc = d.getUTCHours() === 0 && d.getUTCMinutes() === 0 && venueOffset === 0;
                
                // Safety net fallback for 2026 South Africa vs New Zealand matches! 
                // The API actually passes through midnight local kickoffs (venue offset 2) for these games for some reason?
                if (match.time.label && match.time.label.includes("2026-08") || match.time.label?.includes("2026-09")) {
                    if (d.getUTCHours() === 22 && d.getUTCMinutes() === 0 && venueOffset === 2) {
                        // The time resolves to 00:00 local time! This is a placeholder time for these specific fixtures which have not confirmed kickoff times!
                        timeString = "TBC";
                        venueDateTime.timeString = "TBC";
                        utcDateTime.timeString = "TBC";
                    }
                }
"""

if old_logic.strip() in html:
    html = html.replace(old_logic.strip(), new_logic.strip())
else:
    print("Could not find the TBC logic block exactly.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
