import React from 'react';
import './TagComponent.css';
import TagPersonalInfoComponent from './TagPersonalInfoComponent';
import TagEditorComponent from './TagEditorComponent';
import { stateToHTML } from 'draft-js-export-html';
import firebase from '../Firebase';

class TagComponent extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      resource: '',
      personalInfoIsValid: false,
      personalInfo: {}
    };
    this.onSubmit = this.onSubmit.bind(this);
    this.onSkip = this.onSkip.bind(this);
    this.onPersonalInfoChanged = this.onPersonalInfoChanged.bind(this);
  }

  componentDidUpdate(prevProps) {
    if (prevProps === this.props) {
      return;
    }

    this.updateContentFromRandomResource();
  }

  /** Submits the HTML */
  onSubmit(editorContent) {
    console.log(this.state);
    if (this.state.personalInfoIsValid) {
      let html = stateToHTML(editorContent);
      var htmlDoc = new DOMParser().parseFromString(html, 'text/html');

      // Go through each of the 'complex' words and 
      // add additional attributes. 
      var tags = htmlDoc.getElementsByTagName("strong");
      for (var i = 0, len = tags.length; i < len; i++) {
        let text = tags[i].innerHTML;
        tags[i].setAttribute("length-symbols", "" + text.length);
        tags[i].setAttribute("length-words", "" + this.countWords(text));
        console.log(tags[i]);
      }

      const object = {
        info: this.state.personalInfo,
        html: htmlDoc.documentElement.getElementsByTagName("p")[0].innerHTML
      };

      const database = firebase.database();
      const key = database.ref('results').push().key;
      database.ref('results').child(key).set(object).then(() => {
        this.updateContentFromRandomResource();

        window.scrollTo(0, 0);
        alert("Thanks for your contribution.");
      });
    } else {
    }
  }

  countWords(str) {
    return str.split(' ').length;
  }

  onSkip() {
    this.updateContentFromRandomResource();
    window.scrollTo(0, 0);
  }

  onPersonalInfoChanged(info) {
    let isValid = info.age && !isNaN(info.age) &&
      info.academicDegree &&
      info.languageProficiencyLevel &&
      info.domainExpertise;
    this.setState({
      personalInfoIsValid: isValid,
      personalInfo: info
    });
  }

  render() {
    return (
      <div className="container">
        <TagEditorComponent onSubmit={this.onSubmit} onSkip={this.onSkip} resource={this.state.resource} personalInfoIsValid={this.state.personalInfoIsValid} />
        <TagPersonalInfoComponent onStateChanged={this.onPersonalInfoChanged} />
      </div>
    );
  }

  updateContentFromRandomResource() {
    let resources = [];
    Object.entries(this.props.resources).forEach((value, index) => {
      resources.push(value[1]);
    });
    let resource = 'Loading...';
    if (resources) {
      resource = resources[resources.length * Math.random() | 0];
    }

    this.setState({ resource: resource });
  }
}

export default TagComponent;
