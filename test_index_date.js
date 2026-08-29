const fs = require('fs');

const dateStr = '<div style="font-size: 0.9em;">Local kick-off: Sat, 22 Aug 2026 00:00 </div>';
fs.readFile('index.html', 'utf8', (err, data) => {
    
    // We want to verify exactly where Local kick-off is being written
    const search = "Local kick-off:";
    let idx = data.indexOf(search);
    if (idx > -1) {
        console.log(data.substring(idx - 50, idx + 150));
    }
});
