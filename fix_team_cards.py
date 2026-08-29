import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# I want to fix match teams so they do NOT use justify-content: flex-start on .match-teams and flex: 1 on .team-block which currently squeezes/pushes things around.
css_old = """
        .match-teams {
            display: flex;
            align-items: center;
            justify-content: flex-start;
            margin-top: 8px;
            width: 100%;
        }

        .team-block {
            display: flex;
            align-items: center;
            flex: 1;
        }

        .team-block.home-team {
            justify-content: flex-end;
            text-align: right;
        }

        .team-block.away-team {
            justify-content: flex-start;
            text-align: left;
        }
"""

css_new = """
        .match-teams {
            display: flex;
            align-items: center;
            justify-content: flex-start; /* explicitly pushing things to the left as requested */
            margin-top: 8px;
            width: 100%;
        }

        .team-block {
            display: flex;
            align-items: center;
            /* Remove flex: 1; this restricts the blocks to their intrinsic sizes 
               meaning the away-team doesn't get squished to the edge causing words to wrap or overflow */
        }

        .team-block.home-team {
            justify-content: flex-start; 
            text-align: left;
            /* Add explicit fixed width to the home team side so the "vs" is aligned identically vertically */
            width: 130px; 
        }

        .team-block.away-team {
            justify-content: flex-start;
            text-align: left;
        }
"""

html = html.replace(css_old.strip(), css_new.strip())

# Adjust the UI render itself
home_old = """
                                        <div class="team-block home-team">
                                            <div class="team-name" style="text-align: right;">${match.teams[0].name}</div>
                                            <img class="team-flag-img" src="${getTeamLogoUrl(match.teams[0].name)}" alt="${match.teams[0].name} flag" loading="lazy" onerror="this.src='https://ui-avatars.com/api/?name=${encodeURIComponent(match.teams[0].name)}&background=random&color=fff&bold=true'">
                                            <div class="team-score ${scoreHaze}" onclick="this.classList.toggle('score-haze')" title="Click to reveal/hide score" style="margin-left: 12px; font-size: 1.25em;">${isCompletedOrCancelled ? match.scores[0] : (status === 'L' ? match.scores[0] : '0')}</div>
                                        </div>
"""

# Let's fix the order. Score on left, Flag, Name on Right for both blocks so we get a pure left-justified look as per memory 
home_new = """
                                        <div class="team-block home-team">
                                            <div class="team-score ${scoreHaze}" onclick="this.classList.toggle('score-haze')" title="Click to reveal/hide score" style="margin-right: 12px; font-size: 1.25em;">${isCompletedOrCancelled ? match.scores[0] : (status === 'L' ? match.scores[0] : '0')}</div>
                                            <img class="team-flag-img" src="${getTeamLogoUrl(match.teams[0].name)}" alt="${match.teams[0].name} flag" loading="lazy" onerror="this.src='https://ui-avatars.com/api/?name=${encodeURIComponent(match.teams[0].name)}&background=random&color=fff&bold=true'">
                                            <div class="team-name" style="text-align: left;">${match.teams[0].name}</div>
                                            
                                        </div>
"""

html = html.replace(home_old.strip(), home_new.strip())

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
