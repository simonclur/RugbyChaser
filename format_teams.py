import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the match-teams block
css_match_teams_old = """
        .match-teams {
            display: flex;
            align-items: center;
            justify-content: flex-start; /* explicitly pushing things to the left as requested */
            margin-top: 8px;
            width: 100%;
        }
"""
css_match_teams_new = """
        .match-teams {
            display: flex;
            align-items: center;
            justify-content: center; /* Center the match container */
            margin-top: 8px;
            width: 100%;
        }
"""
html = html.replace(css_match_teams_old.strip(), css_match_teams_new.strip())

css_team_block_home_old = """
        .team-block.home-team {
            justify-content: flex-start; 
            text-align: left;
            /* Add explicit fixed width to the home team side so the "vs" is aligned identically vertically */
            width: 130px; 
        }
"""
css_team_block_home_new = """
        .team-block.home-team {
            justify-content: flex-end; /* Push home team content to the right */
            text-align: right;
            width: 150px; /* fixed width for centering the vs block */
        }
"""
html = html.replace(css_team_block_home_old.strip(), css_team_block_home_new.strip())

css_team_block_away_old = """
        .team-block.away-team {
            justify-content: flex-start;
            text-align: left;
        }
"""
css_team_block_away_new = """
        .team-block.away-team {
            justify-content: flex-start;
            text-align: left;
            width: 150px; /* symmetric with home-team */
        }
"""
html = html.replace(css_team_block_away_old.strip(), css_team_block_away_new.strip())

home_html_old = """
                                        <div class="team-block home-team">
                                            <div class="team-score ${scoreHaze}" onclick="this.classList.toggle('score-haze')" title="Click to reveal/hide score" style="margin-right: 12px; font-size: 1.25em;">${isCompletedOrCancelled ? match.scores[0] : (status === 'L' ? match.scores[0] : '0')}</div>
                                            <img class="team-flag-img" src="${getTeamLogoUrl(match.teams[0].name)}" alt="${match.teams[0].name} flag" loading="lazy" onerror="this.src='https://ui-avatars.com/api/?name=${encodeURIComponent(match.teams[0].name)}&background=random&color=fff&bold=true'">
                                            <div class="team-name" style="text-align: left;">${match.teams[0].name}</div>
                                            
                                        </div>
"""
home_html_new = """
                                        <div class="team-block home-team">
                                            <div class="team-name" style="text-align: right;">${match.teams[0].name}</div>
                                            <img class="team-flag-img" src="${getTeamLogoUrl(match.teams[0].name)}" alt="${match.teams[0].name} flag" loading="lazy" style="margin-left: 8px; margin-right: 8px;" onerror="this.src='https://ui-avatars.com/api/?name=${encodeURIComponent(match.teams[0].name)}&background=random&color=fff&bold=true'">
                                            <div class="team-score ${scoreHaze}" onclick="this.classList.toggle('score-haze')" title="Click to reveal/hide score" style="font-size: 1.25em;">${isCompletedOrCancelled ? match.scores[0] : (status === 'L' ? match.scores[0] : '0')}</div>
                                        </div>
"""

html = html.replace(home_html_old.strip(), home_html_new.strip())

away_html_old = """
                                        <div class="team-block away-team">
                                            <div class="team-score ${scoreHaze}" onclick="this.classList.toggle('score-haze')" title="Click to reveal/hide score" style="margin-right: 12px; font-size: 1.25em;">${isCompletedOrCancelled ? match.scores[1] : (status === 'L' ? match.scores[1] : '0')}</div>
                                            <img class="team-flag-img" src="${getTeamLogoUrl(match.teams[1].name)}" alt="${match.teams[1].name} flag" loading="lazy" onerror="this.src='https://ui-avatars.com/api/?name=${encodeURIComponent(match.teams[1].name)}&background=random&color=fff&bold=true'">
                                            <div class="team-name" style="text-align: left;">${match.teams[1].name}</div>
                                        </div>
"""

away_html_new = """
                                        <div class="team-block away-team">
                                            <div class="team-score ${scoreHaze}" onclick="this.classList.toggle('score-haze')" title="Click to reveal/hide score" style="font-size: 1.25em;">${isCompletedOrCancelled ? match.scores[1] : (status === 'L' ? match.scores[1] : '0')}</div>
                                            <img class="team-flag-img" src="${getTeamLogoUrl(match.teams[1].name)}" alt="${match.teams[1].name} flag" loading="lazy" style="margin-left: 8px; margin-right: 8px;" onerror="this.src='https://ui-avatars.com/api/?name=${encodeURIComponent(match.teams[1].name)}&background=random&color=fff&bold=true'">
                                            <div class="team-name" style="text-align: left;">${match.teams[1].name}</div>
                                        </div>
"""

html = html.replace(away_html_old.strip(), away_html_new.strip())

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
