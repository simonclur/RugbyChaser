const https = require('https');

const startDate = new Date('2026-08-20').getTime();
const endDate = new Date('2026-09-10').getTime();
const url = `https://api.wr-rims-prod.pulselive.com/rugby/v3/match?startDate=${startDate}&endDate=${endDate}&sort=asc&pageSize=100&client=pulse`;

https.get(url, (res) => {
    let data = '';
    res.on('data', chunk => data += chunk);
    res.on('end', () => {
        try {
            const json = JSON.parse(data);
            const matches = json.content || [];
            matches.forEach(m => {
                const teams = m.teams.map(t => t.name).join(' vs ');
                if (teams.includes('South Africa') && teams.includes('New Zealand')) {
                    console.log(`Match: ${teams}`);
                    console.log(`Venue: ${m.venue ? m.venue.name : 'Unknown'}`);
                    console.log(`Time Object: ${JSON.stringify(m.time)}`);
                    console.log(`Calculated UTC Date: ${new Date(m.time.millis).toISOString()}`);
                    console.log('---');
                }
            });
        } catch (e) {
            console.error('Error parsing JSON', e);
        }
    });
}).on('error', (e) => {
    console.error(e);
});
