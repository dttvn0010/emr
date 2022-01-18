import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

import { BrowserRouter } from 'react-router-dom';
import { Provider } from 'react-redux'
import axios from 'axios';
import store from './redux/store';

axios.defaults.baseURL = 'http://127.0.0.1:8000';
axios.defaults.headers.post['Content-Type'] = 'application/json';

axios.interceptors.request.use(request => {
  const token = localStorage.getItem('token');
  if(token) {
    request.headers.common.Authorization = 'Bearer ' + token;
  }
  return request;
});

axios.interceptors.response.use(response => {
  return response
}, err => {
  if(err?.response?.status === 403) {
    localStorage.removeItem('token');
    window.location.href = '/';
  }
  return Promise.reject(err);
});

ReactDOM.render(
  <React.StrictMode>
    <BrowserRouter>
      <Provider store={store}>
        <App />
      </Provider>
    </BrowserRouter>
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
