import React, {Component} from "react";
import {ParseService} from "./ParseService";

export class ContentView extends Component {
  render() {
    const elements = ParseService.parse(this.props.content, this.props.loadPageFromUrl);
    return <div className="content-view">
      {elements}
    </div>;
  }
}
