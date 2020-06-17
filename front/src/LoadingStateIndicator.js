import React, { Component } from 'react';

export class LoadingStateIndicator extends Component {
  render() {
    if (this.props.loadingState && this.props.loadingState !== 'none') {
      const mapping = {
        'none': 'Wybrana strona jest wyświetlana',
        'fetch': 'Wybrana strona jest właśnie pobierana z serwera',
        'ready': 'Wybrana strona jest gotowa do wyświetlenia',
      };
      return <div id="loading-state-indicator"><strong>{mapping[this.props.loadingState]}</strong></div>;
    } else {
      return null;
    }
  }
}
