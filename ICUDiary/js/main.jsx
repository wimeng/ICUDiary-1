import React from 'react';
import ReactDOM from 'react-dom';
import Form from './form';
import StrengthChecker from './strengthchecker';
// import MicRecorder from 'mic-recorder-to-mp3'

class Test extends React.Component {
  constructor(props) {
    // Initialize mutable state
    super(props);
  }

  render() {
    return (
      <div> Hello! </div>
    );
  }
}

if (document.getElementById('test')) {
  ReactDOM.render(<Test/>,document.getElementById('test'));
}
else if (document.getElementById('strengthCheckedPassword')) {
  ReactDOM.render(<StrengthChecker/>,document.getElementById('strengthCheckedPassword'));
}

// This method is only called once
ReactDOM.render(
  // Insert the post component into the DOM
  <Form/>,
  document.getElementById('reactEntry'), 
);
