import axios from 'axios';

export const FetchService = {
  fetchContent: function (url) {
    return new Promise((resolve, reject) => {
      axios.get('/v1/minimized-page', {params: {url: url}})
        .then(response => {
          resolve(response.data);
        })
        .catch(error => {
          reject(error.response.status);
        });
    });
  }
};
