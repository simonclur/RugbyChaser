const https = require('https');

// A function to fetch multiple pages if needed, but let's just grab the first page and assume it's there
const url = `https://api.wr-rims-prod.pulselive.com/rugby/v3/match?startDate=2026-08-20&endDate=2026-09-10&sort=asc&pageSize=100&client=pulse`;

fetch(url)
    .then(res => res.json())
    .then(json => {
        const matches = json.content || [];
        matches.forEach(m => {
            const teams = m.teams.map(t => t.name).join(' vs ');
            if (teams.includes('South Africa') && teams.includes('New Zealand')) {
                console.log(`Match ID: ${m.matchId}`);
                console.log(`Match: ${teams}`);
                console.log(`Venue: ${m.venue ? m.venue.name : 'Unknown'}`);
                console.log(`Time Object: ${JSON.stringify(m.time)}`);
                console.log(`Calculated UTC Date: ${new Date(m.time.millis).toISOString()}`);
                console.log('---');
            }
        });
    })
    .catch(e => console.error(e));
