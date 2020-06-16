import React, { Component } from 'react';

import { MainPage } from './components';
import { CacheService } from './CacheService';
import { FetchService } from './FetchService';

export class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      url: undefined,
      content: undefined,
    };
    if (this.props.initialUrl)
      this.loadPageFromUrl(this.props.initialUrl);
  }
  loadPageFromUrl(url, bypassPushState) {
    bypassPushState = bypassPushState || false;
    CacheService.getFromCacheOrFetch(url, FetchService.fetchContent)
    .then(content => {
      this.setState({ url: url, content: content });
      if (!bypassPushState)
        history.pushState(undefined, "", "?url=" + encodeURIComponent(url));
    })
    .catch(responseStatus => {
      // TODO Handle the failure (404/500, etc will land here)
    })
    .finally(() => {
      // TODO Schedule requesting next page to fill the cache
    });
  }
  render() {
    return <MainPage
             url={this.state.url}
             content={this.state.content}
             loadPageFromUrl={url => this.loadPageFromUrl(url)} />;
  }
}
