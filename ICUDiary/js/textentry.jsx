import React from 'react';
import PropTypes from 'prop-types';

class Text extends React.Component {
  /* Display buttons to choose form
   * Reference on forms https://facebook.github.io/react/docs/forms.html
   */

  constructor(props) {
    // Initialize mutable state
    super(props);

    this.state = { 
        maxChars: 0,
        textInput: "",
        entryTitle: "",
        patientDropdown: []
    };
  }

componentDidMount() {
    // set state of character count to begin with
    const url = "/api/patientdropdown/";

    // Call REST API to get post info
    fetch(url, { credentials: 'same-origin', method: 'GET'})
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
          return response.json();
      })
      .then((data) => {
        this.setState({
          maxChars: 500,
          textInput: "",
          entryTitle: "",
          patientDropdown : data.patients,
        });
      })
      .catch((error) => console.log(error));
  }

handleChange(event) {
    event.preventDefault();
    if (500 - event.target.value.length >= 0) {
        this.setState(() => ({
            textInput: event.target.value,
            maxChars: 500 - event.target.value.length,
        }));
    }
  }

handleTitleChange(event) {
    event.preventDefault();
    this.setState({ 
        entryTitle: event.target.value,
        
     });
}

  render() {
    let { patientDropdown } = this.state;
    const options = patientDropdown.map((patient) => <option key={patient.username} value={patient.username}>{patient.firstname} {patient.lastname}</option>)
    return (
      <div>
      <br/>
      <br/>
        <form action="/newentry/" method="post" enctype="multipart/form-data">
            <input type="hidden" name="type" value="text"/>
            <div class="d-flex justify-content-center">
              <label for="patient"> Select a patient:</label>
              <select name="patient" id="patient" required>
                  {options}
              </select>
            </div>
            <br/>
            <div class="d-flex justify-content-center">
                <input class="mr-sm-2" type="text" placeholder= "Entry Title" name="entrytitle" value={this.state.entryTitle} onChange={(e) => {this.handleTitleChange(e)}}/>
            </div>
            <br/>
            <div class="d-flex justify-content-center">
                <textarea style={{resize: 'both'}} type="text" placeholder="Type Your Entry Here" name="entry" value={this.state.textInput} onChange={(e) => {this.handleChange(e)}}/>              
            </div>
            <p class="d-flex justify-content-center">Characters Remaining: {this.state.maxChars}</p> 
            <div class="d-flex justify-content-center">
              <input type="submit" name="createEntry" value="Create Entry"/>
            </div>
        </form>
      </div>
    );
  }
}

export default Text;
