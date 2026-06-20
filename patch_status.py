import re

with open("index.html", "r") as f:
    text = f.read()

# Update CSS for CC
text = text.replace(
    ".status-badge.C { background-color: var(--completed-color); color: white; }",
    ".status-badge.C { background-color: var(--completed-color); color: white; }\n        .status-badge.CC { background-color: var(--completed-color); color: white; opacity: 0.7; }"
)

# Update getMatchStatus
old_getMatchStatus = """        function getMatchStatus(match) {
            // PulseLive: U=Upcoming, C=Completed
            // We'll treat anything that is not U or C as Live. Or if it's U but past start time, might be live.
            let status = match.status;
            if (status !== 'C' && status !== 'U') {
                return 'L'; 
            }
            // Fallback for API delays: if time is past but not strictly marked C or L.
            const now = Date.now();
            if (status === 'U' && now > match.time.millis && now < (match.time.millis + 10800000)) {
                // Within 3 hours of start time and not completed -> probably Live
                return 'L';
            }
            return status;
        }"""

new_getMatchStatus = """        function getMatchStatus(match) {
            let status = match.status;
            // CC is Cancelled by PulseLive. Do not treat it as Live.
            if (status === 'CC') return 'CC'; 
            
            if (status !== 'C' && status !== 'U') {
                return 'L'; 
            }
            // Fallback for API delays: if time is past but not strictly marked C or L.
            const now = Date.now();
            if (status === 'U' && now > match.time.millis && now < (match.time.millis + 10800000)) {
                // Within 3 hours of start time and not completed -> probably Live
                return 'L';
            }
            return status;
        }"""

text = text.replace(old_getMatchStatus, new_getMatchStatus)

old_status_class = """                const statusClass = status === 'C' ? 'completed' : (status === 'L' ? 'live' : (isNextScheduled ? 'next-scheduled' : 'upcoming'));
                const statusLabel = status === 'C' ? 'FT' : (status === 'L' ? 'LIVE' : (isNextScheduled ? 'NEXT: ' + timeString : timeString));"""

new_status_class = """                const isCompletedOrCancelled = status === 'C' || status === 'CC';
                const statusClass = isCompletedOrCancelled ? 'completed' : (status === 'L' ? 'live' : (isNextScheduled ? 'next-scheduled' : 'upcoming'));
                const statusLabel = status === 'C' ? 'FT' : (status === 'CC' ? 'CANC' : (status === 'L' ? 'LIVE' : (isNextScheduled ? 'NEXT: ' + timeString : timeString)));"""

text = text.replace(old_status_class, new_status_class)

with open("index.html", "w") as f:
    f.write(text)

