import React from 'react';
import PropTypes from 'prop-types';
import Text from './textentry.jsx';
import Audio from './audioentry.jsx';

class Form extends React.Component {
  /* Display buttons to choose form
   * Reference on forms https://facebook.github.io/react/docs/forms.html
   */

  constructor(props) {
    // Initialize mutable state
    super(props);
    this.handleTextClick = this.handleTextClick.bind(this);
    this.handleAudioClick = this.handleAudioClick.bind(this);
    this.state = { 
        entryType: "",
    };
  }

  componentDidMount() {
    // set state of entry type to begin with
    this.setState({ 
        entryType: "none",
    });
    }

  handleTextClick() {
    this.setState({ 
        entryType: "text",
    });
  }

  handleAudioClick() {
    this.setState({ 
        entryType: "audio",
    });
  }

  

  render() {
    let { entryType } = this.state;
    return (
      <div className="buttons" style={{backgroundColor: "#F5F5F5", borderStyle: "solid", borderColor: "#E5E5E5", marginLeft: "30%", marginRight: "30%"}}>
        <div>
            <span class="d-flex justify-content-center" style={{paddingTop: "10px", }}>
                <input className="btn btn-outline-info my-2 my-sm-0" type="submit" value="Text Entry" onClick={this.handleTextClick}/>
            </span>
            <br></br>
            <span class="d-flex justify-content-center" style={{paddingBottom: "10px", }}>
                <input className="btn btn-outline-info my-2 my-sm-0" type="submit" value="Audio Entry" onClick={this.handleAudioClick}/>
            </span>
          {entryType === "text" && <Text/>}

          {entryType === "audio" && <Audio/>}
          <script>
          </script>
        </div>
      </div>
    );
  }
}

export default Form;
