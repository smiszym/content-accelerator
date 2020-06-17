import React, { Component } from 'react';
import { AvailableSpaceView } from "./AvailableSpaceView";
import { ContentView } from "./ContentView";
import { LoadingStateIndicator } from "./LoadingStateIndicator";
import { NewUrlPrompt } from "./NewUrlPrompt";

class MainPageWithoutContent extends Component {
  render() {
    return <div>
      <LoadingStateIndicator loadingState={this.props.loadingState} />
      <h1 id="content-title">Content Accelerator</h1>
      <p>
        To jest aplikacja wspomagająca dostęp do treści internetowych w warunkach
        słabego łącza.
      </p>
      <NewUrlPrompt loadPageFromUrl={this.props.loadPageFromUrl} />
      <AvailableSpaceView />
    </div>;
  }
}

class MainPageWithContent extends Component {
  render() {
    const content = this.props.content;

    return <div>
      <LoadingStateIndicator loadingState={this.props.loadingState} />
      <h1 id="content-title">{content.title}</h1>
      <ContentView
        content={this.props.content}
        loadPageFromUrl={this.props.loadPageFromUrl} />
      {
        content.links.length > 0 &&
          <div>
            Linki:
            <ol>
              {
                content.links.map((link, i) => {
                  return <li>
                    <a>{link.text}</a> <a href={link.url}>(oryginał)</a>
                  </li>;
                })
              }
            </ol>
          </div>
      }
      <div>
        Oryginalny artykuł: <a href={this.props.url}>{this.props.url}</a>
      </div>
      <NewUrlPrompt loadPageFromUrl={this.props.loadPageFromUrl} />
      <AvailableSpaceView />
    </div>;
  }
}

export class MainPage extends Component {
  render() {
    return this.props.content
      ? <MainPageWithContent
          loadingState={this.props.loadingState}
          content={this.props.content}
          url={this.props.url}
          loadPageFromUrl={this.props.loadPageFromUrl} />
      : <MainPageWithoutContent
          loadingState={this.props.loadingState}
          loadPageFromUrl={this.props.loadPageFromUrl} />;
  }
}
