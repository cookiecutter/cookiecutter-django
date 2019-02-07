import React, { Component } from 'react'
import logo from './logo.svg'
import './App.css'

import axios from 'axios'


class App extends Component {
  onClick = (e) => {
    console.log("Sending a GET API Call !!!");
    axios.get('/api/')
    .then(res => {
      console.log(res);
    }).then(response => {
      console.log(JSON.stringify(response));
    })
  }

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Welcome to React</h1>
        </header>
        <p className="App-intro">
          To get started, edit <code>src/App.js</code> and save to reload.
        </p>
        <button type="button" onClick={this.onClick}>Send API request</button>
      </div>
    )
  }
}


export default App
