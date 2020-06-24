import {CacheService} from "./CacheService";
import {FetchService} from "./FetchService";
import {FetchQueueService} from "./FetchQueueService";

export const ContentRepository = {
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
