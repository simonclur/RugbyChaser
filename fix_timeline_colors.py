import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

timeline_events_old = """
                                html += `<div class="timeline-event">
                                    <div class="timeline-time">${timeLabel}</div>
                                    <div class="timeline-content">
                                        <strong>${ev.typeLabel || ev.type}</strong>
                                        ${pName ? `<div>${pName}</div>` : ''}
                                        ${tName ? `<div class="timeline-team">${tName}</div>` : ''}
                                    </div>
                                </div>`;
"""

timeline_events_new = """
                                let iconStyle = '';
                                if ((ev.typeLabel || ev.type) === 'SubstitutionOn' || (ev.typeLabel || ev.type) === 'Substitute On') {
                                    iconStyle = 'color: #22c55e;'; // Green for going on
                                } else if ((ev.typeLabel || ev.type) === 'SubstitutionOff' || (ev.typeLabel || ev.type) === 'Substitute Off') {
                                    iconStyle = 'color: #ef4444;'; // Red for going off
                                }
                                
                                html += `<div class="timeline-event">
                                    <div class="timeline-time">${timeLabel}</div>
                                    <div class="timeline-content">
                                        <strong style="${iconStyle}">${ev.typeLabel || ev.type}</strong>
                                        ${pName ? `<div>${pName}</div>` : ''}
                                        ${tName ? `<div class="timeline-team">${tName}</div>` : ''}
                                    </div>
                                </div>`;
"""


html = html.replace(timeline_events_old.strip(), timeline_events_new.strip())

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
