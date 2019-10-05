import { ApolloClient } from 'apollo-client'
import { ApolloLink } from 'apollo-link'

import { authLink, restLink, stateLink, uploadLink } from './links'
import cache from './cache'
import { mockLink } from './mocks'

const defaultOptions = {
  watchQuery: {
    fetchPolicy: 'cache-and-network',
    errorPolicy: 'ignore',
  },
  query: {
    fetchPolicy: 'cache-and-network',
    errorPolicy: 'all',
  },
  mutate: {
    // NOTE: Using 'none' will allow Apollo to recognize errors even if the response
    // includes {data: null} in it (graphene does this with each unsuccessful mutation!)
    errorPolicy: 'none',
  },
}

const link = ApolloLink.from([stateLink, restLink, authLink.concat(uploadLink)])

const client = new ApolloClient({
  link:
    process.env.NODE_ENV === 'production'
      ? link // never use mock for production
      : ApolloLink.split(operation => operation.getContext().mock, mockLink, link),
  cache,
  connectToDevTools: process.env.NODE_ENV === 'production' ? false : true,
  defaultOptions,
})

export default client
