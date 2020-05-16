import React from 'react';
import * as JSZip from 'jszip';
import firebase from '../Firebase';
import './Admin.css';
import * as FileSaver from 'file-saver';

class Admin extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      isLoading: false
    };

    this.handleFileChosen = (file) => {
      this.setState({
        isLoading: true
      });

      JSZip.loadAsync(file).then((zip) => {
        const promises = [];
        zip.forEach((key, zipEntry) => {
          if (key.match(/(\/|^)\./g)) {
            return;
          }

          const p = zipEntry.async("text").then((text) => {
            return {
              key: key.replace(/\./g, '_'),
              value: text
            };
          });
          promises.push(p);
        });
        Promise.all(promises).then((list) => {
          const object = {};
          list.forEach(function (item) {
            object[item.key] = item.value;
          });

          const database = firebase.database();
          database.ref('resources').set(object).then(() => {
            this.setState({
              isLoading: false
            });
          });
        })
      });
    };

    this.deleteUserSubmits = () => {
      const database = firebase.database();
      database.ref('results').set({});
    };
    
    this.downloadUserSubmits = () => {
      const database = firebase.database();
      database.ref('results').once('value').then((snapshot) => {
        let json = JSON.stringify(snapshot.val());
        var blob = new Blob([json], { type: "text/plain;charset=utf-8" });
        FileSaver.saveAs(blob, "submits.json");
      });
    };
  }

  render() {
    let loader;
    if (this.state.isLoading) {
      loader = <div>Loading...</div>;
    } else {
      loader = <div></div>;
    }

    let resources = [];
    Object.entries(this.props.resources).forEach((value, index) => {
      const element = <li key={value[0]}>{value[0]}</li>;
      resources.push(element);
    });

    return (
      <div>
        <div className="header">
          <div className="btn" onClick={this.deleteUserSubmits}>delete user submits</div>
          <div className="btn" onClick={this.downloadUserSubmits}>download user submits</div>
        </div>
        <div className="divider"></div>
        <div>
          <div>Pick a .zip file to upload:</div>
          <input type='file'
            id='file'
            className='input-file'
            accept='.zip'
            onChange={e => this.handleFileChosen(e.target.files[0])}
          />
          <div>it will replace previously uploaded text resources but <i>will not</i> delete existing user submits.</div>
          {loader}
        </div>
        <div className="divider"></div>
        <ul>
          {resources}
        </ul>
      </div>
    );
  }
}

export default Admin;
