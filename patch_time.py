import re

with open("index.html", "r") as f:
    text = f.read()

text = text.replace(
    "const offsetH = parseFloat(tzSelect.value);",
    "const offsetH = parseFloat(tzSelect.value);\n            const tzLabel = tzSelect.options[tzSelect.selectedIndex].text;"
)


old_match_loop = """            allMatches.forEach(match => {
                const { dateString, timeString } = formatDateTime(match.time.millis, offsetH);
                const status = getMatchStatus(match);"""

new_match_loop = """            allMatches.forEach(match => {
                const { dateString, timeString } = formatDateTime(match.time.millis, offsetH);
                const venueOffset = match.time.gmtOffset || 0;
                const venueDateTime = formatDateTime(match.time.millis, venueOffset);
                const status = getMatchStatus(match);"""

text = text.replace(old_match_loop, new_match_loop)

old_meta = """                                    <div class="match-meta">
                                        ${match.venue?.name || 'TBA'}, ${match.venue?.city || ''}
                                    </div>"""

new_meta = """                                    <div class="match-meta">
                                        ${match.venue?.name || 'TBA'}, ${match.venue?.city || ''}<br>
                                        <span style="font-size: 0.95em;">${timeString} (${tzLabel}) | <span style="opacity: 0.8">Local: ${venueDateTime.dateString} ${venueDateTime.timeString}</span></span>
                                    </div>"""

text = text.replace(old_meta, new_meta)

with open("index.html", "w") as f:
    f.write(text)

