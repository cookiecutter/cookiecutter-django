import { findIndex, remove } from 'lodash'
import { buildClientSchema } from 'graphql'

import * as jsonFile from './schema'

export const mockSchema = () => {
  // new json loader update adds a `defulat` parent level to json
  const x = jsonFile.default

  // Apollo won't accept introspection that has any '__debug' values in json file, so the parser should remove them first
  // To read more: https://github.research.chop.edu/DGD/nexus/issues/1318#issuecomment-18281

  const queryTypeIndex = findIndex(x.data.__schema.types, ['name', 'Query'])
  const mutationTypeIndex = findIndex(x.data.__schema.types, ['name', 'Mutation'])

  // remove the fields:

  remove(x.data.__schema.types[queryTypeIndex].fields, field => field.name === '__debug')
  remove(x.data.__schema.types[mutationTypeIndex].fields, field => field.name === '__debug')

  const schema = buildClientSchema(x.data)

  return schema
}
