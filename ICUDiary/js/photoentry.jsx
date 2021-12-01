import React from 'react';
import PropTypes from 'prop-types';

class Photo extends React.Component {
  /* Display buttons to choose form
   * Reference on forms https://facebook.github.io/react/docs/forms.html
   */

  constructor(props) {
    // Initialize mutable state
    super(props);

    this.state = {
        caption: "",
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
          caption: "",
          entryTitle: "",
          patientDropdown : data.patients,
        });
      })
      .catch((error) => console.log(error));
  }

handleChange(event) {
    event.preventDefault();
    this.setState(() => ({
        caption: event.target.value,
    }))
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
            <input type="hidden" name="type" value="photo"/>
            <div class="d-flex justify-content-center">
              <label for="patient"> Select a patient:</label>
              <select name="patient" id="patient" required>
                  {options}
              </select>
            </div>
            <div class="d-flex justify-content-center">
                <input class="mr-sm-2" type="text" placeholder= "Entry Title" name="entrytitle" value={this.state.entryTitle} onChange={(e) => {this.handleTitleChange(e)}}/>
            </div>
            <br/>
            <div class="d-flex justify-content-center">
                Upload photo: <input type="file" name="file" required/>
            </div>
            <br/>
            <div class="d-flex justify-content-center">
                <input type="text" placeholder="Type Your Caption" name="entry" value={this.state.caption} onChange={(e) => {this.handleChange(e)}}/>              
            </div>
            <br/>
            <div class="d-flex justify-content-center" style={{paddingBottom: "10px", }}>
              <input class="btn btn-outline-primary btn-block btn-lg ms-3" style={{backgroundColor: "lightgray", }} type="submit" name="createEntry" value="Create Entry"/>
            </div>
        </form>
      </div>
    );
  }
}

export default Photo;
