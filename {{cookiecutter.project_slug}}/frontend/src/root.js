import React from 'react'
import { Provider as AlertProvider } from 'react-alert'
import AlertTemplate from 'react-alert-template-basic'
import { Router } from 'react-router-dom'
import { ApolloProvider } from '@apollo/react-hooks'
import { createBrowserHistory as createHistory } from 'history'
import Raven from 'raven-js'

import client from 'apollo/client'
import Routes from './routes'

if (process.env.NODE_ENV === 'production') {
  Raven.config(process.env.REACT_APP_SENTRY_URL).install()
}

const history = createHistory()

const Root = () => (
  <ApolloProvider client={client}>
    <AlertProvider template={AlertTemplate}>
      <Router history={history}>
        <Routes />
      </Router>
    </AlertProvider>
  </ApolloProvider>
)

export default Root
