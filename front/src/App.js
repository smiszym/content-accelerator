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
      lastPageLoadTime: undefined,
    };
    if (this.props.initialUrl)
      this.loadPageFromUrl(this.props.initialUrl);
  }
  loadPageFromUrl(url, bypassPushState) {
    bypassPushState = bypassPushState || false;
    if (performance.mark !== undefined) {
      performance.mark("page-requested");
      this.setState({ lastPageLoadTime: undefined });
    }

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
          if (performance.mark !== undefined) {
            performance.mark("page-displayed");
            performance.measure("page-load-time", "page-requested", "page-displayed");
            const entries = performance.getEntriesByName("page-load-time","measure");
            if (entries.length === 1) {
              this.setState({ lastPageLoadTime: entries[0].duration });
              console.log("Content Accelerator: load time was " + this.state.lastPageLoadTime.toFixed(0)
                          + " ms (" + (isAvailable?"hot":"cold") + " cache) for url " + url);
            }
            performance.clearMeasures();
            performance.clearMarks();
          }
        })
        .catch(responseStatus => {
          this.setState({ loading: 'failure' });
          console.log("Failure (status code: " + responseStatus + ") to load URL " + url);
        })
        .finally(() => {
          // TODO Schedule requesting next page to fill the cache
        });
      });
  }
  render() {
    return <MainPage
             loadingState={this.state.loading}
             lastPageLoadTime={this.state.lastPageLoadTime}
             url={this.state.url}
             content={this.state.content}
             loadPageFromUrl={url => this.loadPageFromUrl(url)} />;
  }
}
