function timeSince(date) {
    let pubDiv = document.getElementById("pubDate")

    const seconds = Math.floor((new Date() - date) / 1000);

    let interval = seconds / 31536000;

    let result;
    if (interval > 1) {
        result = Math.floor(interval) + " سال قبل";
        pubDiv.innerHTML = result;
    }
    interval = seconds / 2592000;
    if (interval > 1) {
        result = Math.floor(interval) + " ماه قبل";
        pubDiv.innerHTML = result;
    }
    interval = seconds / 86400;
    if (interval > 1) {
        result = Math.floor(interval) + " روز قیل";
        pubDiv.innerHTML = result;
    }
    interval = seconds / 3600;
    if (interval > 1) {
        result = Math.floor(interval) + " ساعت قبل";
        pubDiv.innerHTML = result;
    }
    interval = seconds / 60;
    if (interval > 1) {
        result = Math.floor(interval) + " دقیقه قبل";
        pubDiv.innerHTML = result;
    }
    else {
        result = Math.floor(seconds) + " ثانیه قبل";
        pubDiv.innerHTML = result;
    }
}
