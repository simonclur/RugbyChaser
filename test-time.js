function formatLocalTime(utcMillisStr, offset) {
    if (!utcMillisStr) return '';
    try {
        const utcMillis = typeof utcMillisStr === 'string' ? parseFloat(utcMillisStr) : utcMillisStr;
        if (isNaN(utcMillis)) return '';
        
        let targetMillis = utcMillis;

        if (offset !== null && offset !== undefined) {
            // Apply numeric offset manually.
            const userOffsetMs = parseFloat(offset) * 60 * 60 * 1000;
            // The browser will *still* adjust this to local timezone when rendering string
            // We need to use UTC getters to represent the exact localized time
            
            targetMillis = utcMillis + userOffsetMs;
            const targetDate = new Date(targetMillis);
            
            const hours = String(targetDate.getUTCHours()).padStart(2, '0');
            const minutes = String(targetDate.getUTCMinutes()).padStart(2, '0');
            return `${hours}:${minutes}`;
        }
        
    } catch (e) {
        return '';
    }
}
console.log(formatLocalTime(1724943600000, 10)); // UTC 15:00 29th Aug -> 01:00 Bris 30th Aug
console.log(formatLocalTime(1725116400000, 2)); // SA vs NZ at Ellis Park (15:00 UTC Aug 31)
