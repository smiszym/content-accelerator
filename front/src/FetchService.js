import axios from 'axios';
import {FetchQueueService} from "./FetchQueueService";
import {CacheService} from "./CacheService";

export const FetchService = {
  initialize: function () {
    FetchService.fetchInBackground();
  },
  waitForFetch: function (url) {
    return new Promise((resolve, reject) => {
      FetchService.observers.push({url: url, resolve: resolve});
    });
  },
  fetchInBackground: function () {
    setTimeout(function() {
      FetchService.currentlyFetchedUrl = FetchQueueService.dequeue();
      if (FetchService.currentlyFetchedUrl) {
        console.log("Fetching " + FetchService.currentlyFetchedUrl);

        axios.get('/v1/minimized-page', {params: {url: FetchService.currentlyFetchedUrl}})
          .then(response => {
            const content = response.data;
            CacheService.putToCache(FetchService.currentlyFetchedUrl, content);
            console.log("Put to cache: " + FetchService.currentlyFetchedUrl);
            FetchService.observers = FetchService.observers.filter(observer => {
              if (observer.url === FetchService.currentlyFetchedUrl) {
                observer.resolve(content);
                return false;
              } else {
                return true;
              }
            });
            FetchService.currentlyFetchedUrl = null;
            FetchService.fetchInBackground();
          })
          .catch(error => {
            console.log("Error " + error.response.status + " while fetching " + FetchService.currentlyFetchedUrl);
            FetchService.currentlyFetchedUrl = null;
            FetchService.fetchInBackground();
          });
      } else {
        FetchService.fetchInBackground();
      }
    }, 500);
  },
  fetchContent: function (url) {
    return new Promise((resolve, reject) => {
      FetchQueueService.insertWithPriority(url);
      FetchService.waitForFetch(url)
        .then(content => {
          resolve(content);
        })
        .catch(error => {
          reject(error);
        });
    });
  },
  currentlyFetchedUrl: undefined,
  observers: []
};
