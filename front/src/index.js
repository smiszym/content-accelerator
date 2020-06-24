import React from 'react';
import ReactDOM from 'react-dom';

import { App } from './App';
import {FetchService} from "./FetchService";

FetchService.initialize();

function retrieveTargetLocationFromUrl(url) {
  return new URL(url).searchParams.get("url");
}

const initialUrl = retrieveTargetLocationFromUrl(window.location.href);
const app = ReactDOM.render(
  <App initialUrl={initialUrl} />,
  document.getElementById('app'));

window.onpopstate = function(event) {
  app.loadPageFromUrl(
    retrieveTargetLocationFromUrl(window.location.href),
    true);
};

module.hot.accept();
