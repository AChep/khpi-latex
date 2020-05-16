import React from 'react';
import {
  BrowserRouter as Router,
  Switch,
  Route
} from "react-router-dom";
import Admin from './Admin';
import TagComponent from './TagComponent';
import firebase from '../Firebase';
import './App.css';
import { ToastProvider } from 'react-toast-notifications'

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      resources: {},
      isLoading: true
    };
  }

  componentDidMount() {
    const database = firebase.database();
    database
      .ref('resources')
      .on('value', (snapshot) => {
        const v = snapshot.val();
        this.setState({
          resources: v ? v : {},
          isLoading: false
        });
      });
  }

  render() {
    const loader = this.state.isLoading ?
      (
        <div className="slider">
          <div className="line"></div>
          <div className="subline inc"></div>
          <div className="subline dec"></div>
        </div>
      )
      : null;
    return (
      <ToastProvider>
        <div>
          {loader}
          <div className="body">
            <Router>
              <Switch>
                <Route path="/admin-panel">
                  <Admin resources={this.state.resources} />
                </Route>
                <Route path="/">
                  <TagComponent resources={this.state.resources} />
                </Route>
              </Switch>
            </Router>
          </div>
        </div>
      </ToastProvider>
    );
  }
}

export default App;
