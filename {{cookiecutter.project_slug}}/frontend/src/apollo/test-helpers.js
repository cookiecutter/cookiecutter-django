import { assign } from 'lodash'
import { baseMocks } from './mocks'
import { graphql } from 'graphql'
import { addMockFunctionsToSchema } from 'graphql-tools'
import { mockSchema } from './schema-parser'
import { print as gqlToString } from 'graphql/language'


export const mockQuery = ({query, mocks, variables = { id: 'id' }, log = false}) => {
  // Arguments:
  // (required) QUERY
  // (optional) Mock object : to override base mocks
  // (optional) Variables : If not passed, it will use a fake id only (most frequently used)
  // (optional) Log : In case you want the query result to be shown with test results.

  /// MOCKING SCHEMA:
  const schema = mockSchema()
  const combinedMocks = mocks ? assign({}, baseMocks, mocks) : baseMocks
  addMockFunctionsToSchema({ schema, mocks: combinedMocks })

  // need the first 'return' so that the final output is the promise result
  return graphql(schema, gqlToString(query), null, null, variables).then(result => {
    if (log) console.log('mockQuery result', result)
    const { data, errors } = result
    expect(errors).toBe()
    return data
  })
}
