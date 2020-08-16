import { get, set, keys } from 'idb-keyval';

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
          if (value)
            value.url = url;
          resolve(value);
        });
    });
  },
  putToCache: function (url, content) {
    set(url, content)
      .catch(err => {
        // TODO Handle failure to write to the cache
      });
  },
  listOfEntries: function () {
    return new Promise((resolve, reject) => {
      keys()
        .then(keys => {
          Promise.allSettled(keys.map(key => CacheService.getFromCache(key)))
            .then(outcomes => {
              resolve(outcomes.map(outcome => ({title: outcome.value.title, url: outcome.value.url})));
            });
        });
    });
  }
};
