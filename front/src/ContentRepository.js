import {CacheService} from "./CacheService";
import {FetchService} from "./FetchService";
import {FetchQueueService} from "./FetchQueueService";

export const ContentRepository = {
  // Retrieves the content either from the cache or from the server and returns it in a promise
  getContent: function (url) {
    return new Promise((resolve, reject) => {
      // First, try to get the content from the cache
      CacheService.getFromCache(url)
        .then(value => {
          if (value) {
            resolve(value);
          } else {
            // The content is not in cache
            if (FetchService.currentlyFetchedUrl === url) {
              // The content is being fetched
              FetchService.waitForFetch(url).then(resolve).catch(reject);
            } else {
              if (FetchQueueService.contains(url)) {
                // The content is queued for fetching
                // TODO Move to the front of the queue
                FetchService.waitForFetch(url).then(resolve).catch(reject);
              } else {
                // The content is not queued for fetching, so enqueue it
                FetchQueueService.insertWithPriority(url);
                FetchService.waitForFetch(url).then(resolve).catch(reject);
              }
            }
          }
        });
    });
  },
  checkContentState: function (url) {
    return new Promise((resolve, reject) => {
      // First, check if the content is in the cache
      CacheService.isInCache(url)
        .then(present => {
          if (present) {
            resolve('cached');
          } else {
            // Then, check if we're currently fetching this URL
            if (FetchService.currentlyFetchedUrl === url) {
              resolve('fetching');
            } else {
              if (FetchQueueService.contains(url)) {
                resolve('pending');
              } else {
                resolve('none');
              }
            }
          }
        });
    });
  }
};
