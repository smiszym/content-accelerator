export const PredictionService = {
  urlsToFetch: function(urls) {
    // This function predicts which URLs from the list will likely be accessed by the user.
    // Currently the naive implementation is that all URLs are likely to be visited.
    return urls;
  }
};
