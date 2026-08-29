function formatDateTime(millis, offsetH) {
    const date = new Date(millis);
    const tzSelectMs = offsetH * 60 * 60 * 1000;
    
    // Instead of fighting getTimezoneOffset(), just compute the target UTC time
    // and rely on getUTC* methods to format it without local tz interference.
    
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

console.log(formatDateTime(1724943600000, 10)); // Current UTC: 15:00 Aug 29th -> Should be 01:00 Aug 30th (Bris)
console.log(formatDateTime(1725116400000, 2)); // SA vs NZ at Ellis Park (15:00 UTC Aug 31) -> Should be 17:00 Aug 31st (SA time)
