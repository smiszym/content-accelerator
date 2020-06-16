import axios from 'axios';
import React, { Component } from 'react';

import { MainPage } from './components';

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
  loadPageFromUrl(url) {
    axios.get('/v1/minimized-page', { params: { url: url } })
    .then(response => {
      this.setState({ url: url, content: response.data });
    })
    .catch(error => {
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
