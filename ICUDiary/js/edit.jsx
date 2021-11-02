import React from 'react';
import PropTypes from 'prop-types';

class Edit extends React.Component {
  /* Display buttons to choose form
   * Reference on forms https://facebook.github.io/react/docs/forms.html
   */

  constructor(props) {
    // Initialize mutable state
    super(props);
    access = True;
  }

  componentDidMount() {
    // set state of entry type to begin with
    this.setState({ 
        access: True,
    });
    }

  handleTextClick() {
    this.setState({ 
        entryType: "text",
    });
  }  

  render() {
    let { access } = this.state;
    return (
      <div className="buttons">
        <div>
            <div class="d-flex justify-content-center">
                <input class="btn btn-outline-info my-2 my-sm-0" type="submit" value="Text Entry" onClick={this.handleTextClick}/>
            </div>
            <div class="d-flex justify-content-center">
                <input class="btn btn-outline-info my-2 my-sm-0" type="submit" value="Audio Entry" onClick={this.handleAudioClick}/>
            </div>

        </div>
      </div>
    );
  }
}

export default Edit;
