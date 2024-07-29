let x = "aHR0cHM6Ly9nb2ZpbGUuaW8vZC9ZR083Y2t8MDM5ZjVjMTMxMA=="

var decodedUrl = atob(x).split('|')[0];

console.log(decodedUrl)



function redirectToLink(encodedUrl) {
    var decodedUrl = atob(encodedUrl);
    window.location.href = decodedUrl;
}
function openEpisode(encodedPermalink) {
    var decodedPermalink = atob(encodedPermalink);
    window.location.href = decodedPermalink;
}
document.addEventListener("DOMContentLoaded", function() {
    var apiKey = "97c2f6cd-5143-4e42-93d8-b239b7c781be";
    function loadIframe(link) {
        var encodedUrl = link.getAttribute("data-url");
        var decodedUrl = atob(encodedUrl);
        var pattern = /^https:\/\/yonaplay\.org\/embed\.php\?id=\d+$/;
        var urlWithApiKey = decodedUrl;
        if (pattern.test(decodedUrl)) {
            urlWithApiKey += "&apiKey=" + apiKey;
        }
        var iframeContainer = document.getElementById("iframe-container");
        while (iframeContainer.firstChild) {
            iframeContainer.removeChild(iframeContainer.firstChild);
        }
        var iframe = document.createElement("iframe");
        iframe.src = urlWithApiKey;
        iframe.loading = "lazy";
        iframe.frameBorder = 0;
        iframe.allow = "fullscreen";
        iframeContainer.appendChild(iframe);
    }
    var serverLinks = document.querySelectorAll(".server-link");
    var serverUrls = window[dynamicServerVarName];
    serverLinks.forEach(function(link) {
        var key = link.getAttribute("data-key");
        if (serverUrls[key]) {
            link.setAttribute("data-url", serverUrls[key]);
            link.addEventListener("click", function(event) {
                event.preventDefault();
                loadIframe(this);
            });
        }
    });
});
