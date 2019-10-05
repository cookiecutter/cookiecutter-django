import { InMemoryCache } from 'apollo-cache-inmemory'
import { persistCache } from 'apollo-cache-persist'
import localForage from 'localforage'

const cache = new InMemoryCache()

persistCache({cache, storage: localForage})

export default cache
