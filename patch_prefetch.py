import re

with open("index.html", "r") as f:
    text = f.read()

target = """            // Trigger async fetches for live matches after DOM is updated
            liveMatchesToLoad.forEach(lm => loadLiveMatchDetails(lm.id, lm.compName, lm.venueName));


        }"""

replacement = """            // Trigger async fetches for live matches after DOM is updated
            liveMatchesToLoad.forEach(lm => loadLiveMatchDetails(lm.id, lm.compName, lm.venueName));

            // Auto-scroll to the next/active fixture
            setTimeout(() => {
                const target = document.getElementById('auto-scroll-target');
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            }, 100);

            // Trigger prefetch for next 3 upcoming matches
            let prefetchedCount = 0;
            for (let match of allMatches) {
                if (match.status === 'U' && getMatchStatus(match) !== 'L') {
                    prefetchMatchDetails(match.matchId);
                    prefetchedCount++;
                    if (prefetchedCount >= 3) break;
                }
            }
        }"""

text = text.replace(target, replacement)

with open("index.html", "w") as f:
    f.write(text)
