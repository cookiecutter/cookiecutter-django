import cookie from 'react-cookies'
import { setContext } from 'apollo-link-context'
import { createHttpLink } from 'apollo-link-http'
import { RestLink } from 'apollo-link-rest'
import { withClientState } from 'apollo-link-state'
import { createUploadLink } from 'apollo-upload-client'
import { merge } from 'lodash'

import cache from './cache'

// docs: https://www.apollographql.com/docs/link/links/http.html
export const httpLink = createHttpLink({
  uri: '/graphql/',
  credentials: 'same-origin',
})

// docs: https://github.com/jaydenseric/apollo-upload-client
export const uploadLink = createUploadLink({
  uri: '/graphql/',
  credentials: 'same-origin',
})

// docs: https://www.apollographql.com/docs/link/links/rest.html
export const restLink = new RestLink({
  uri: '/api/',
  endpoints: {},
})

// docs: https://www.apollographql.com/docs/link/links/state.html
export const stateLink = withClientState({
  cache,
  ...merge({}),
})

export const authLink = setContext((_, { headers }) => {
  return {
    headers: {
      ...headers,
      'X-CSRFToken': cookie.load('csrftoken'),
      Authorization: `JWT ${cookie.load('jwt')}`,
    },
  }
})
