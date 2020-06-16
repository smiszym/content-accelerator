import React, { Component } from 'react';
import parse from 'html-react-parser';
import sanitizeHtml from 'sanitize-html';

class AvailableSpaceView extends Component {
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

class ContentView extends Component {
  render() {
    const sanitizedHtml = sanitizeHtml(this.props.content.text, {
      allowedTags: sanitizeHtml.defaults.allowedTags.concat(
        ['dl', 'dt', 'dd']),
      allowedAttributes: {
        a: ['href', 'onclick']
      },
      transformTags: {
        'a': function(tagName, attribs) {
          return {
            tagName: 'a',
            attribs: {
              href: attribs.href,
              onclick: 'return false;'
            }
          };
        }
      }
    });
    const elements = parse(sanitizedHtml);
    return <div id="page-content">
      <h2>Treść artykułu</h2>
      <div>
        {elements}
      </div>
    </div>;
  }
}

class NewUrlPrompt extends Component {
  constructor(props) {
    super(props);
    this.state = { url: '' };
  }
  render() {
    return <div>
      Podaj adres strony internetowej do dynamicznego załadowania:
      <input type="url" value={this.state.url} onChange={evt => this.setState({ url: evt.target.value })} />
      <br />
      <button onClick={evt => this.props.loadPageFromUrl(this.state.url)}>Załaduj</button>
    </div>;
  }
}

class MainPageWithoutContent extends Component {
  render() {
    return <div>
      <h1>Content Accelerator</h1>
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
      <h1>{content.title}</h1>
      <div>
        Oryginalny artykuł: <a href={this.props.url}>{this.props.url}</a>
      </div>
      <ContentView content={this.props.content} />
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
      <NewUrlPrompt loadPageFromUrl={this.props.loadPageFromUrl} />
      <AvailableSpaceView />
    </div>;
  }
}

export class MainPage extends Component {
  render() {
    return this.props.content
      ? <MainPageWithContent
          content={this.props.content}
          loadPageFromUrl={this.props.loadPageFromUrl} />
      : <MainPageWithoutContent
          loadPageFromUrl={this.props.loadPageFromUrl} />;
  }
}
