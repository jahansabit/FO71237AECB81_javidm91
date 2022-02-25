console.log("hi there vpn");

// Listen for messages
chrome.runtime.onMessage.addListener(function (msg, sender, sendResponse) {
    // If the received message has the expected format...
    console.log("msg", msg);
    var data = {};
    data["url"] = window.location.href;
    data["title"] = document.title;
    data["html"] = document.documentElement.outerHTML;
    sendResponse(data);
});