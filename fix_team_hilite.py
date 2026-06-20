import re

with open("index.html", "r") as f:
    text = f.read()

# Make sure highlight class logic works correctly with the filterAllTeams var
old_highlight = """                const badgeClass = isNextScheduled ? 'N' : status;

                const involvesTeam = !filterAllTeams && (selectedTeams.includes(match.teams[0].name) || selectedTeams.includes(match.teams[1].name));"""
new_highlight = """                const badgeClass = isNextScheduled ? 'N' : status;

                const involvesTeam = !filterAllTeams && (selectedTeams.includes(match.teams[0].name) || selectedTeams.includes(match.teams[1].name));"""

# Also ensure we are passing filterAllTeams to the summary output
old_summary = """                let infoArr = [];
                if (filterAllComps) {"""

new_summary = """                let infoArr = [];
                const teamSelectElem = document.getElementById('team-filter');
                const selTeams = Array.from(teamSelectElem.selectedOptions).map(o => o.value);
                const filtAllTeams = selTeams.includes('ALL') || selTeams.length === 0;

                if (filterAllComps) {"""

text = text.replace(old_summary, new_summary)


old_summary_push = """                if (!filterAllTeams) {
                    infoArr.push(`Highlighting <strong>${selectedTeams.length}</strong> team(s)`);
                }"""

new_summary_push = """                if (!filtAllTeams) {
                    infoArr.push(`Highlighting <strong>${selTeams.length}</strong> team(s)`);
                }"""
text = text.replace(old_summary_push, new_summary_push)


with open("index.html", "w") as f:
    f.write(text)

