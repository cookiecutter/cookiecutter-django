import React, { Suspense } from 'react'
import { Route, Switch } from 'react-router-dom'

const App = React.lazy(() => import('./App'))

const Routes = () => (
  <Suspense fallback={<div>Loading...</div>}>
    <Switch>
      <Route path="/app/" component={App} />
    </Switch>
  </Suspense>
)

export default Routes
