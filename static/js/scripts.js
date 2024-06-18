function increment(username, clicks, func) {
    var xhr = new XMLHttpRequest();
    clicks++;
    const data = {username, clicks}
    xhr.open("POST", "/" + func);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify(data));
    sleep(10).then(() => { location.reload(); }); //let func complete before refreshing
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}