import React, { Component } from 'react';
import { AvailableSpaceView } from "./AvailableSpaceView";
import { ContentView } from "./ContentView";
import { LoadingStateIndicator } from "./LoadingStateIndicator";
import { NewUrlPrompt } from "./NewUrlPrompt";

export class MainPage extends Component {
  render() {
    const content = this.props.content;

    return <div>
      <LoadingStateIndicator loadingState={this.props.loadingState} />
      <h1 id="content-title">{content ? content.title : "Content Accelerator"}</h1>
      {
        content
          ? <ContentView
              content={this.props.content}
              loadPageFromUrl={this.props.loadPageFromUrl} />
          : <p>
              To jest aplikacja wspomagająca dostęp do treści internetowych w warunkach
              słabego łącza.
            </p>
      }
      {
        content && content.links.length > 0 &&
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
      {
        this.props.lastPageLoadTime &&
          <div>Ostatni artykuł załadowano w {this.props.lastPageLoadTime.toFixed(0)} ms</div>
      }
      {
        this.props.frontendCachedPages &&
          <div>
            Strony w cache'u po stronie frontendu:
            <ul>
              {
                this.props.frontendCachedPages.map((page, i) => {
                  return <li key={page.url}>
                    <a>{page.title}</a> <a href={page.url}>(oryginał)</a>
                  </li>;
                })
              }
            </ul>
          </div>
      }
    </div>;
  }
}
