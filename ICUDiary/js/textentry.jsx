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
    };
  }

  componentDidMount() {
    // set state of character count to begin with
    this.setState({ 
        maxChars: 250,
        textInput: "",
        entryTitle: "",
    });
  }

handleChange(event) {
    event.preventDefault();
    if (250 - event.target.value.length >= 0) {
        this.setState(() => ({
            textInput: event.target.value,
            maxChars: 250 - event.target.value.length,
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
    let {  } = this.state;
    return (
      <div>
        <form action="/newentry/" method="post" enctype="multipart/form-data">
            <div class="d-flex justify-content-center">
                <input class="mr-sm-2" type="text" placeholder= "Entry Title" name="entrytitle" value={this.state.entryTitle} onChange={(e) => {this.handleTitleChange(e)}}/>
            </div>
            <div class="d-flex justify-content-center">
                <textarea style={{resize: 'both'}} type="text" placeholder="Type Your Entry Here" name="entry" value={this.state.textInput} onChange={(e) => {this.handleChange(e)}}/>              
            </div>
            <p class="d-flex justify-content-center">Characters Remaining: {this.state.maxChars}</p>  
            <input type="submit" name="createEntry" value="Create Entry"/>
        </form>
      </div>
    );
  }
}

export default Text;
