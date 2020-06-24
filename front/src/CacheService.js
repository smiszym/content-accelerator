import { get, set } from 'idb-keyval';

export const CacheService = {
  isInCache: function (url) {
    return new Promise((resolve, reject) => {
      get(url)
        .then(value => {
          resolve(value !== undefined);
        });
    });
  },
  getFromCache: function (url) {
    return new Promise((resolve, reject) => {
      get(url)
        .then(value => {
          resolve(value);
        });
    });
  },
  putToCache: function (url, content) {
    set(url, content)
      .catch(err => {
        // TODO Handle failure to write to the cache
      });
  }
};
