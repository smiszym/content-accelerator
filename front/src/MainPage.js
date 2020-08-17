import React, { Component } from 'react';
import { AvailableSpaceView } from "./AvailableSpaceView";
import { CacheService } from "./CacheService";
import { ContentView } from "./ContentView";
import { LoadingStateIndicator } from "./LoadingStateIndicator";
import { NewUrlPrompt } from "./NewUrlPrompt";
import {FetchService} from "./FetchService";

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
        this.props.content
        && <div>
             Oryginalny artykuł: <a href={this.props.content.url}>{this.props.content.url}</a>
           </div>
      }
      {
        this.props.content
        && this.props.content.cache_used === true && <div>Artykuł znajdował się w cache backendu</div>
      }
      {
        this.props.content
        && this.props.content.cache_used === false && <div>Artykułu nie było w cache backendu; został pobrany</div>
      }
      {
        this.props.content
        && <button onClick={evt => { CacheService.removeFromCache(this.props.content.url); }} >
             Usuń z cache frontendu
           </button>
      }
      {
        this.props.content
        && <button onClick={evt => {
                 CacheService.removeFromCache(this.props.content.url);
                 FetchService.removeFromBackendCache(this.props.content.url);
               }} >
             Usuń z cache frontendu oraz backendu
           </button>
      }
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
