import React, {Component} from "react";

export class AvailableSpaceView extends Component {
  constructor(props) {
    super(props);
    this.state = { usage: 0, quota: 0 };
  }
  componentDidMount() {
    if ('storage' in navigator && 'estimate' in navigator.storage) {
      navigator.storage.estimate().then(({usage, quota}) => {
        this.setState({
          usage: usage / 1024 / 1024,
          quota: quota / 1024 / 1024,
        });
      });
    }
  }
  render() {
    return <div>
      Szacowane zużycie wynosi {this.state.usage.toFixed(0)} MB
      z {this.state.quota.toFixed(0)} MB dostępnego miejsca.
    </div>;
  }
}
