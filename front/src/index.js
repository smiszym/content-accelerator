import React from 'react';
import ReactDOM from 'react-dom';

import { App } from './App';

const initialUrl = new URL(window.location.href).searchParams.get("url");

ReactDOM.render(
  <App initialUrl={initialUrl} />,
  document.getElementById('app')
);

module.hot.accept();
