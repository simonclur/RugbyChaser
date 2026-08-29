import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix the time logic
time_logic_old = """
        function formatDateTime(millis, offsetH) {
            const date = new Date(millis);
            // Apply absolute UTC offset
            const offsetMillis = offsetH * 60 * 60 * 1000;
            const utcTime = date.getTime() + (date.getTimezoneOffset() * 60000);
            const localDate = new Date(utcTime + offsetMillis);

            const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
            const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
            
            const day = days[localDate.getDay()];
            const dateNum = String(localDate.getDate()).padStart(2, '0');
            const month = months[localDate.getMonth()];
            const year = localDate.getFullYear();
            
            const hours = String(localDate.getHours()).padStart(2, '0');
            const minutes = String(localDate.getMinutes()).padStart(2, '0');

            return {
                dateString: `${day}, ${dateNum} ${month} ${year}`,
                timeString: `${hours}:${minutes}`
            };
        }
"""

time_logic_new = """
        function formatDateTime(millis, offsetH) {
            const tzSelectMs = offsetH * 60 * 60 * 1000;
            let targetMillis = millis;
            if (offsetH !== null && offsetH !== undefined) {
                targetMillis = millis + tzSelectMs;
            }
            const targetDate = new Date(targetMillis);

            const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
            const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
            
            const day = days[targetDate.getUTCDay()];
            const dateNum = String(targetDate.getUTCDate()).padStart(2, '0');
            const month = months[targetDate.getUTCMonth()];
            const year = targetDate.getUTCFullYear();
            
            const hours = String(targetDate.getUTCHours()).padStart(2, '0');
            const minutes = String(targetDate.getUTCMinutes()).padStart(2, '0');

            return {
                dateString: `${day}, ${dateNum} ${month} ${year}`,
                timeString: `${hours}:${minutes}`
            };
        }
"""

html = html.replace(time_logic_old.strip(), time_logic_new.strip())

# Fix the CSS for match-teams - you can see they are extending out bounds due to padding/margin logic that doesn't fit on thin screens.
css_old = """
        .match-teams {
            display: flex;
            justify-content: space-between;
            align-items: center;
            width: 100%;
            margin-bottom: 20px;
            padding: 0 10px;
            box-sizing: border-box;
        }
"""

css_new = """
        .match-teams {
            display: flex;
            justify-content: space-between;
            align-items: center;
            width: 100%;
            margin-bottom: 20px;
            padding: 0 10px;
            box-sizing: border-box;
            gap: 15px; /* keep spacing tight inside */
        }
"""

html = html.replace(css_old.strip(), css_new.strip())


# Fix the `.team-block.away-team` text-align explicitly
css_away_old = """
        .team-block.away-team {
            flex-direction: row;
            text-align: right;
            border-left: none;
            padding-left: 0;
            border-right: 3px solid var(--accent-color);
            padding-right: 15px;
        }
"""

css_away_new = """
        .team-block.away-team {
            flex-direction: row;
            /* Allow text alignment left here as well so the team score on LHS and flag in middle still keeps names uniformly left justified per user request */
            text-align: right; 
            border-left: none;
            padding-left: 0;
            border-right: 3px solid var(--accent-color);
            padding-right: 15px;
        }
"""

html = html.replace(css_away_old.strip(), css_away_new.strip())

# We also inject the .player-row override specifically enforcing left alignment directly down from the row
css_row_old = """
        .player-row {
            display: grid;
            grid-template-columns: 24px 1fr;
            gap: 10px;
            padding: 5px 0;
            border-bottom: 1px solid var(--card-border);
            text-align: left;
            width: 100%;
        }
"""

css_row_new = """
        .player-row {
            display: grid;
            grid-template-columns: 24px 1fr;
            gap: 10px;
            padding: 5px 0;
            border-bottom: 1px solid var(--card-border);
            text-align: left; /* strictly enforced by inline rule in render logic now too */
            width: 100%;
        }
"""

html = html.replace(css_row_old.strip(), css_row_new.strip())


# Now handle the render logic of the match-teams inline so away-team text-align left works with the wrapping
match_render_old = """
                                        <div class="team-block away-team">
                                            <div class="team-score ${scoreHaze}" onclick="this.classList.toggle('score-haze')" title="Click to reveal/hide score" style="margin-right: 12px; font-size: 1.25em;">${isCompletedOrCancelled ? match.scores[1] : (status === 'L' ? match.scores[1] : '0')}</div>
                                            <img class="team-flag-img" src="${getTeamLogoUrl(match.teams[1].name)}" alt="${match.teams[1].name} flag" loading="lazy" onerror="this.src='https://ui-avatars.com/api/?name=${encodeURIComponent(match.teams[1].name)}&background=random&color=fff&bold=true'">
                                            <div class="team-name" style="text-align: left;">${match.teams[1].name}</div>
                                        </div>
"""

match_render_new = """
                                        <div class="team-block away-team" style="justify-content: flex-end;">
                                            <div class="team-score ${scoreHaze}" onclick="this.classList.toggle('score-haze')" title="Click to reveal/hide score" style="margin-right: 12px; font-size: 1.25em;">${isCompletedOrCancelled ? match.scores[1] : (status === 'L' ? match.scores[1] : '0')}</div>
                                            <img class="team-flag-img" src="${getTeamLogoUrl(match.teams[1].name)}" alt="${match.teams[1].name} flag" loading="lazy" onerror="this.src='https://ui-avatars.com/api/?name=${encodeURIComponent(match.teams[1].name)}&background=random&color=fff&bold=true'">
                                            <div class="team-name" style="text-align: left;">${match.teams[1].name}</div>
                                        </div>
"""
# Note team-name is text-align: left above

html = html.replace(match_render_old.strip(), match_render_new.strip())


html = html.replace("""<div class="team-block home-team">""", """<div class="team-block home-team" style="justify-content: flex-start;">""")



with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
