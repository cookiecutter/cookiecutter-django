import React from 'react'
import { Router } from 'react-router-dom'
import { createBrowserHistory as createHistory } from 'history'
import Raven from 'raven-js'

import Routes from './routes'

if (process.env.NODE_ENV === 'production') {
  Raven.config(process.env.REACT_APP_SENTRY_URL).install()
}

const history = createHistory()

const Root = () => (
  <Router history={history}>
    <Routes />
  </Router>
)

export default Root
