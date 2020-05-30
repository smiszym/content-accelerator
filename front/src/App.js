import React, { Component } from 'react';

import { MainPage } from './components';

export class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      url: undefined,
      content: undefined,
    };
  }
  loadPageFromUrl(url) {
    const xhttp = new XMLHttpRequest();
    const setState = (state) => { this.setState(state); };
    xhttp.onreadystatechange = function() {
      if (this.readyState === 4 && this.status === 200) {
        const content = JSON.parse(this.responseText);
        setState({ url: url, content: content });
      }
    };
    xhttp.open("GET", "/minimized-page?url=" + encodeURIComponent(url), true);
    xhttp.send();
  }
  render() {
    return <MainPage
             url={this.state.url}
             content={this.state.content}
             loadPageFromUrl={url => this.loadPageFromUrl(url)} />;
  }
}
