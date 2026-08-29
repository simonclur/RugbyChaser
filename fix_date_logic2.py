import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# I also need to update the top-level init block used inside init rendering!
init_logic_old = """
                const venueOffset = match.time.gmtOffset || 0;
                const venueDateTime = formatDateTime(match.time.millis, venueOffset);
                const isTbc = startDate.getUTCHours() === 0 && startDate.getUTCMinutes() === 0 && venueOffset === 0;
                const localTimeText = isTbc ? 'TBC' : `${venueDateTime.dateString} ${venueDateTime.timeString}`;
"""

init_logic_new = """
                const venueOffset = match.time.gmtOffset || 0;
                const venueDateTime = formatDateTime(match.time.millis, venueOffset);
                let isTbc = startDate.getUTCHours() === 0 && startDate.getUTCMinutes() === 0 && venueOffset === 0;
                if (startDate.getUTCHours() === 22 && startDate.getUTCMinutes() === 0 && venueOffset === 2) {
                    isTbc = true;
                }
                const localTimeText = isTbc ? 'TBC' : `${venueDateTime.dateString} ${venueDateTime.timeString}`;
"""

if init_logic_old.strip() in html:
    html = html.replace(init_logic_old.strip(), init_logic_new.strip())
else:
    print("Could not find the TBC logic block for init logic.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
