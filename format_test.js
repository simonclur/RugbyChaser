function formatDateTime(millis, offsetH) {
    const tzSelectMs = offsetH * 60 * 60 * 1000;
    let targetMillis = millis;
    if (offsetH !== null && offsetH !== undefined) {
        targetMillis = millis + tzSelectMs;
    }
    const targetDate = new Date(targetMillis);

    const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    
    const day = days[targetDate.getUTCDay()];
    const dateNum = String(targetDate.getUTCDate()).padStart(2, '0');
    const month = months[targetDate.getUTCMonth()];
    const year = targetDate.getUTCFullYear();
    
    const hours = String(targetDate.getUTCHours()).padStart(2, '0');
    const minutes = String(targetDate.getUTCMinutes()).padStart(2, '0');

    return {
        dateString: `${day}, ${dateNum} ${month} ${year}`,
        timeString: `${hours}:${minutes}`
    };
}

const venueOffset = 2; // For SA vs NZ

console.log("Calculated output mapping:");
console.log(formatDateTime(1788016200000, 2));


// Detect TBC matches (midnight UTC returning 0.0 offset from API)
let venueDateTime = formatDateTime(1788016200000, venueOffset);
const d = new Date(1788016200000);
const isTbc = d.getUTCHours() === 0 && d.getUTCMinutes() === 0 && venueOffset === 0;

console.log(`isTBC: ${isTbc}`); // TBC?
console.log(`venueDateTime: ${JSON.stringify(venueDateTime)}`);


