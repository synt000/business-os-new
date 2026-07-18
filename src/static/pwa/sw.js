const CACHE_NAME = "business-os-v1";

const ASSETS = [
    "/",
    "/static/pwa/manifest.json",
    "/static/pwa/icon-192.png",
    "/static/pwa/icon-512.png"
];

self.addEventListener("install", event => {

    event.waitUntil(

        caches.open(CACHE_NAME)
        .then(cache => {

            return Promise.all(
                ASSETS.map(url =>
                    cache.add(url).catch(err =>
                        console.log("Cache skip:", url)
                    )
                )
            );

        })

    );

});


self.addEventListener("fetch", event => {

    event.respondWith(

        caches.match(event.request)
        .then(response => {

            return response || fetch(event.request);

        })

    );

});
