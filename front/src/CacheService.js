import { get, set } from 'idb-keyval';

export const CacheService = {
  getFromCacheOrFetch: function (url, fetchingFunc) {
    return new Promise((resolve, reject) => {
      get(url)
        .then(value => {
          if (value) {
            // URL found in the cache
            resolve(value);
          } else {
            // URL not found in the cache, it needs to be fetched
            fetchingFunc(url)
              .then(content => {
                set(url, content)
                  .catch(err => {
                    // TODO Handle failure to write to the cache
                  });
                resolve(content);
              })
              .catch(responseStatus => {
                reject(responseStatus);
              });
          }
        });
    });
  }
};
