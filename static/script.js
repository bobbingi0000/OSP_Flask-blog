document.addEventListener('DOMContentLoaded', () => {
    // Animate system status bars
    const cpuBar = document.getElementById('cpu-bar');
    const memBar = document.getElementById('mem-bar');

    setInterval(() => {
        if (cpuBar) {
            const cpuUsage = Math.floor(Math.random() * 30) + 10; // 10-40%
            cpuBar.style.width = cpuUsage + '%';
        }
    }, 2000);

    setInterval(() => {
        if (memBar) {
            const memUsage = Math.floor(Math.random() * 10) + 80; // 80-90%
            memBar.style.width = memUsage + '%';
        }
    }, 5000);

    // Update terminal clock
    const clockElem = document.getElementById('sys-clock');
    if (clockElem) {
        setInterval(() => {
            const now = new Date();
            clockElem.textContent = now.toISOString().replace('T', ' ').substring(0, 19);
        }, 1000);
    }
});
