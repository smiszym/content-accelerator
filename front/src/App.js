import React, { Component } from 'react';

import { MainPage } from './MainPage';
import { CacheService } from './CacheService';
import { FetchService } from './FetchService';

export class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      loading: 'none',
      url: undefined,
      content: undefined,
    };
    if (this.props.initialUrl)
      this.loadPageFromUrl(this.props.initialUrl);
  }
  loadPageFromUrl(url, bypassPushState) {
    bypassPushState = bypassPushState || false;

    // First check if the page is already cached
    CacheService.isInCache(url)
      .then(isAvailable => {
        if (!isAvailable) {
          this.setState({ loading: 'fetch' });
        }
        CacheService.getFromCacheOrFetch(url, FetchService.fetchContent)
        .then(content => {
          this.setState({ loading: 'none', url: url, content: content });
          if (!bypassPushState)
            history.pushState(undefined, "", "?url=" + encodeURIComponent(url));
        })
        .catch(responseStatus => {
          // TODO Handle the failure (404/500, etc will land here)
        })
        .finally(() => {
          // TODO Schedule requesting next page to fill the cache
        });
      });
  }
  render() {
    return <MainPage
             loadingState={this.state.loading}
             url={this.state.url}
             content={this.state.content}
             loadPageFromUrl={url => this.loadPageFromUrl(url)} />;
  }
}
