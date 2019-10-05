import { SchemaLink } from 'apollo-link-schema'
import { addMockFunctionsToSchema } from 'graphql-tools'
import { assign } from 'lodash'

import { mockSchema } from '../schema-parser'

export const baseMocks = {}

// Use this devMocks object for your development mock override
// Make sure to empty this part before your pull request
const devMocks = {}

const combinedMocks = assign({}, baseMocks, devMocks)

const schema = mockSchema()

addMockFunctionsToSchema({ schema, mocks: combinedMocks })

export const mockLink = new SchemaLink({ schema })
