import json

with open("index.html", "r") as f:
    html = f.read()

# I see it in the screenshot! `.player-num` and the Name are squished.
# Actually, the user says "the text is not aligning nicely within the IphoneSE display"
# One issue is that the text inside the team is NOT centered globally relative to its column... because the columns themselves (`.lineup-team`) is taking up max 50% width!
# By using flex-start on .player-row it shoves everything exactly against the left boundary of that 50% flex box.
# For the right side wrapper, it shoves it all the way left towards the center!
# If we change `justify-content: flex-start` to `justify-content: center`, it will align nicely down the exact middle of each column. 

old_player_row = """        .player-row {
            display: flex;
            align-items: center;
            justify-content: flex-start;
            gap: 6px;
            overflow: hidden;
        }"""
new_player_row = """        .player-row {
            display: flex;
            align-items: center;
            justify-content: center; /* Center player content inside each 50% column block */
            gap: 6px;
            overflow: hidden;
            width: 100%;
        }"""

html = html.replace(old_player_row, new_player_row)

old_lineup_team = """        .lineup-team {
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 4px;
            min-width: 0; 
            max-width: 50%;
        }"""
new_lineup_team = """        .lineup-team {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center; /* keep inner text blocks grouped symmetrically */
            gap: 4px;
            min-width: 0; 
            max-width: 50%;
        }"""

html = html.replace(old_lineup_team, new_lineup_team)

old_lineup_h4 = """        .lineup-team h4 {
            margin: 0 0 10px 0;
            font-size: 1em;
            color: var(--text-color);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            text-align: center;
        }"""
new_lineup_h4 = """        .lineup-team h4 {
            margin: 0 0 10px 0;
            font-size: 1em;
            color: var(--text-color);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            text-align: center;
            width: 100%; /* Force header to assert full bounds for centering */
        }"""

html = html.replace(old_lineup_h4, new_lineup_h4)


# Let's ALSO add a wrapper rule so that if we want it left-aligned inside the column, we align the text nodes left, BUT group the column block centered. 
# actually let's just make the text left aligned:
# `.player-row-inner` wrapper maybe?
# I'll just change `.player-row` to `justify-content: center;` but fixed width the number: `.player-num { width: 14px; text-align: right; }`

css_extra = """
        .player-row-content {
            display: flex; 
            width: 100%; 
            max-width: 140px; /* Force an equal bounds layout to keep text left-justified but structurally centered */
            justify-content: flex-start;
        }
        .player-num { margin-right: 2px; opacity: 0.7; }
"""
html = html.replace("</style>", css_extra + "\n    </style>")

# Update how we inject `player-row`
# from:
# html += `<div class="player-row"> 
#               <div class="player-num">${p.number || ''}</div>
#               <div>${p.player.name.display}</div>
#          </div>`;
html = html.replace("""<div class="player-row">
                                            <div class="player-num">${p.number || ''}</div>
                                            <div>${p.player.name.display}</div>
                                        </div>""", """<div class="player-row">
                                            <div class="player-row-content">
                                                <div class="player-num">${p.number ? (p.number + '.') : ''}</div>
                                                <div style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${p.player.name.display}</div>
                                            </div>
                                        </div>""")

with open("index.html", "w") as f:
    f.write(html)
