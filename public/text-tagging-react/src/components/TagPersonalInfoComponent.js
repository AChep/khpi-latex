import React from 'react';
import './TagPersonalInfoComponent.css';

class TagPersonalInfoComponent extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      age: '',
      academicDegree: '',
      languageProficiencyLevel: '',
      domainExpertise: ''
    };
  }

  handleChange(field, event) {
    const stateNew = { ...this.state };
    stateNew[field] = event.target.value;

    this.props.onStateChanged(stateNew);
    this.setState(stateNew);
  }

  render() {
    return (
      <form>
        <label>
          Age:
        <input type="text" onChange={this.handleChange.bind(this, "age")} value={this.state.age} />
          {this.state.age && !isNaN(this.state.age) ? null : <i>Must be a number</i>}
        </label>
        <label>
          Academic degree:
        <select type="text" required onChange={this.handleChange.bind(this, "academicDegree")} value={this.state.academicDegree}>
            <option value="" style={{ display: 'none' }}></option>
            <option name="Doctoral degree">Doctoral degree</option>
            <option name="Master's degree">Master's degree</option>
            <option name="Bachelor's degree">Bachelor's degree</option>
            <option name="Associate's degree">Associate's degree</option>
          </select>
          {this.state.academicDegree ? null : <i>Must not be empty</i>}
        </label>
        <label>
          Language proficiency level (ILR scale):
        <select type="text" required onChange={this.handleChange.bind(this, "languageProficiencyLevel")} value={this.state.languageProficiencyLevel}>
            <option value="" style={{ display: 'none' }}></option>
            <option name="Native">Native</option>
            <option name="Professional Working">Professional Working</option>
            <option name="Limited Working">Limited Working</option>
            <option name="Elementary">Elementary</option>
            <option name="No">No</option>
          </select>
          {this.state.languageProficiencyLevel ? null : <i>Must not be empty</i>}
        </label>
        <label>
          Domain expertise:
          <select type="text" required onChange={this.handleChange.bind(this, "domainExpertise")} value={this.state.domainExpertise}>
            <option value="" style={{ display: 'none' }}></option>
            <option name="Expert">Expert</option>
            <option name="Non-expert">Non-expert</option>
          </select>
          {this.state.domainExpertise ? null : <i>Must not be empty</i>}
        </label>
      </form>
    );
  }
}

export default TagPersonalInfoComponent;
