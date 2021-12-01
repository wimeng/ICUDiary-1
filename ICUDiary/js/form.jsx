import React from 'react';
import PropTypes from 'prop-types';
import Text from './textentry.jsx';
import Audio from './audioentry.jsx';
import Photo from './photoentry.jsx';
import Video from './videoentry.jsx';

class Form extends React.Component {
  /* Display buttons to choose form
   * Reference on forms https://facebook.github.io/react/docs/forms.html
   */

  constructor(props) {
    // Initialize mutable state
    super(props);
    this.handleTextClick = this.handleTextClick.bind(this);
    this.handleAudioClick = this.handleAudioClick.bind(this);
    this.handlePhotoClick = this.handlePhotoClick.bind(this);
    this.handleVideoClick = this.handleVideoClick.bind(this);
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

  handlePhotoClick() {
    this.setState({ 
        entryType: "photo",
    });
  }
  
  handleVideoClick() {
    this.setState({ 
        entryType: "video",
    });
  }

  

  render() {
    let { entryType } = this.state;
    return (
      <div className="buttons" style={{backgroundColor: "#F5F5F5", borderStyle: "solid", borderColor: "#E5E5E5", marginLeft: "30%", marginRight: "30%"}}>
        <div>
            <span class="d-flex justify-content-center" style={{paddingTop: "10px", }}>
                <input class="btn btn-outline-primary btn-block btn-lg ms-3" style={{backgroundColor: "lightgray"}} type="submit" value="Text Entry" onClick={this.handleTextClick}/>
            </span>
            <br></br>
            <span class="d-flex justify-content-center" style={{paddingBottom: "10px", }}>
                <input class="btn btn-outline-primary btn-block btn-lg ms-3" style={{backgroundColor: "lightgray", }} type="submit" value="Audio Entry" onClick={this.handleAudioClick}/>
            </span>
            <br></br>
            <span class="d-flex justify-content-center" style={{paddingBottom: "10px", }}>
                <input class="btn btn-outline-primary btn-block btn-lg ms-3" style={{backgroundColor: "lightgray", }} type="submit" value="Photo Entry" onClick={this.handlePhotoClick}/>
            </span>
            <br></br>
            <span class="d-flex justify-content-center" style={{paddingBottom: "10px", }}>
                <input class="btn btn-outline-primary btn-block btn-lg ms-3" style={{backgroundColor: "lightgray", }} type="submit" value="Video Entry" onClick={this.handleVideoClick}/>
            </span>
          {entryType === "text" && <Text/>}

          {entryType === "audio" && <Audio/>}

          {entryType === "photo" && <Photo/>}

          {entryType === "video" && <Video/>}
          <script>
          </script>
        </div>
      </div>
    );
  }
}

export default Form;
