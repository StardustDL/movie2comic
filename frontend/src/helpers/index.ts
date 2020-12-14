export function readableSecondTimeString(value: number) {
    const minute = Math.floor(value / 60);
    const second = Math.floor(value % 60);
    if (minute == 0) {
        return `${second}''`;
    }
    else if (second == 0) {
        return `${minute}'`;
    }
    else {
        return `${minute}'${second}''`;
    }
}