import React, {Component} from "react";

export class NewUrlPrompt extends Component {
  constructor(props) {
    super(props);
    this.state = { url: '' };
  }
  render() {
    return <div>
      Podaj adres strony internetowej do dynamicznego załadowania:
      <input id="new-url" type="url" value={this.state.url} onChange={evt => this.setState({ url: evt.target.value })} />
      <br />
      <button id="go" onClick={evt => this.props.loadPageFromUrl(this.state.url)}>Załaduj</button>
    </div>;
  }
}
