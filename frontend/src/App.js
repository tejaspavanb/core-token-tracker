import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import TokenList from './components/TokenList';
import TokenDetails from './components/TokenDetails';

function App() {
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <h1>Core Token Tracker</h1>
        </header>
        <main>
          <Switch>
            <Route path="/tokens/:address" component={TokenDetails} />
            <Route path="/" component={TokenList} />
          </Switch>
        </main>
      </div>
    </Router>
  );
}

export default App;