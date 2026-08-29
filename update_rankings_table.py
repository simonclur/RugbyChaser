import json
import re

with open("index.html", "r") as f:
    html = f.read()

# Change data.entries.slice(0, 20) -> data.entries (to include all teams, since we are adding scrolling)
# Add a fixed-height scrolling wrapper around the `<tbody>` using a scrollable block.
# Actually, making just the `<tbody>` scrollable across all browsers without breaking width alignments is annoying.
# The easier way is to wrap the entire `<table>` in a `div` with `max-height` and `overflow-y: auto`.

old_start = """                    let tableHTML = `
                    <div style="overflow-x: auto;">
                        <table class="pools-table" style="width: 100%; border-collapse: collapse; margin-top: 10px;">
                            <thead>"""

new_start = """                    let tableHTML = `
                    <div style="overflow-x: auto; overflow-y: auto; max-height: 480px; scrollbar-width: thin;">
                        <table class="pools-table" style="width: 100%; border-collapse: collapse; margin-top: 10px;">
                            <thead style="position: sticky; top: 0; z-index: 10;">
                                <tr style="background-color: var(--secondary-bg); text-align: left; font-size: 0.8em; color: var(--muted-text);">"""

html = html.replace(old_start, new_start)

# Change slice:
html = html.replace("data.entries.slice(0, 20).forEach((entry, idx) => {", "data.entries.forEach((entry, idx) => {")

# Change footer snippet:
old_footer = """                        </table>
                        <div style="font-size: 0.7em; color: var(--muted-text); text-align: right; padding: 5px;">Showing Top 20 currently.</div>
                    </div>
"""
new_footer = """                        </table>
                    </div>
                    <div style="font-size: 0.7em; color: var(--muted-text); text-align: center; padding: 5px;">Scroll for more rankings.</div>
"""

html = html.replace(old_footer, new_footer)

with open("index.html", "w") as f:
    f.write(html)
