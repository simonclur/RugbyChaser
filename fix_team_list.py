import re

with open("index.html", "r") as f:
    html = f.read()

# Let's inspect .match-teams and .team-block. We need to center the players explicitly.
# Right now, `.home-team` (left side) is right-aligned for text, and `.away-team` is left-aligned.
# The user wants to "fix the centre justification of the team list cards" - so the player lists themselves are probably left/right aligned spilling out.

old_player_row = """                                    html += `<div class="player-row">
                                        <div class="player-num">${p.number || ''}</div>
                                        <div>${p.player.name.display}</div>
                                    </div>`;"""

# If we look at how player lists are constructed:
# `<div class="lineup-team">` -> it has a `player-row`. 
# Wait, let's just make sure `.lineup-team` is centered or has fixed widths so it doesn't spill over.
# It seems `.lineup-team` is basically the column for each team.

# "in IphoneSE device emulation mode, the team lists are appearing outcode the match card, overflowing to the right."
# "for longer team names, we don't appear to be be correctly centering the display and the team names are spilling over to the right - we should probably centre-justify on the match-card."

# The issue is likely `.lineup` flex container doesn't wrap or constrain widths.

css_updates = """
        .lineup {
            display: flex;
            justify-content: center;
            gap: 20px;
            font-size: 0.85em;
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px dashed var(--card-border);
            text-align: center;
            width: 100%;
            box-sizing: border-box;
            overflow-x: hidden;
        }
        
        .lineup-team {
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 4px;
            min-width: 0; 
            max-width: 50%;
        }

        .lineup-team h4 {
            margin: 0 0 10px 0;
            font-size: 1em;
            color: var(--text-color);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            text-align: center;
        }

        .player-row {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            overflow: hidden;
        }
        
        .player-row > div:last-child {
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .match-teams {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 15px 0;
            width: 100%;
            box-sizing: border-box;
        }

        .team-block {
            display: flex;
            align-items: center;
            gap: 15px;
            flex: 1;
            min-width: 0; /* allows text truncation */
        }
        
        .home-team { justify-content: flex-end; }
        .away-team { justify-content: flex-start; }

        .team-name {
            font-size: 1.1em;
            font-weight: bold;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
"""

html = re.sub(r'\s*\.lineup \{.*?\}', '', html, flags=re.DOTALL)
html = re.sub(r'\s*\.lineup-team \{.*?\}', '', html, flags=re.DOTALL)
html = re.sub(r'\s*\.player-row \{.*?\}', '', html, flags=re.DOTALL)
html = re.sub(r'\s*\.team-block \{.*?\}', '', html, flags=re.DOTALL)
html = re.sub(r'\s*\.match-teams \{.*?\}', '', html, flags=re.DOTALL)
html = re.sub(r'\s*\.team-name \{.*?\}', '', html, flags=re.DOTALL)

# Re-inject the cleaned up CSS constraints
html = html.replace('</style>', css_updates + '\n    </style>')

with open("index.html", "w") as f:
    f.write(html)
