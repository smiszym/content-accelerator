import React, { Component } from 'react';

export class LoadingStateIndicator extends Component {
  render() {
    if (this.props.loadingState && this.props.loadingState !== 'none') {
      const mapping = {
        'none': 'The page you requested is being displayed',
        'fetch': 'The page you requested is being fetched from the server',
        'ready': 'The page you requested is ready to be displayed',
      };
      return <div id="loading-state-indicator"><strong>{mapping[this.props.loadingState]}</strong></div>;
    } else {
      return null;
    }
  }
}
