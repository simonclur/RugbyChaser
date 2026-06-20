import re

with open("index.html", "r") as f:
    text = f.read()

# Update getMatchStatus to handle games older than 3 hours
old_getMatchStatus = """        function getMatchStatus(match) {
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

new_getMatchStatus = """        function getMatchStatus(match) {
            let status = match.status;
            // CC is Cancelled by PulseLive. Do not treat it as Cancelled/Live improperly.
            if (status === 'CC') return 'CC'; 
            
            if (status !== 'C' && status !== 'U') {
                return 'L'; 
            }
            // Fallback for API delays: if time is past but not strictly marked C or L.
            const now = Date.now();
            if (status === 'U') {
                if (now > match.time.millis && now < (match.time.millis + 10800000)) {
                    // Within 3 hours of start time and not completed -> probably Live
                    return 'L';
                } else if (now >= (match.time.millis + 10800000)) {
                    // Over 3 hours past start time, so the match is definitely over
                    // Treat it as Completed locally so it doesn't block 'Next'
                    return 'C'; 
                }
            }
            return status;
        }"""

text = text.replace(old_getMatchStatus, new_getMatchStatus)

with open("index.html", "w") as f:
    f.write(text)

