import React from 'react';
import PropTypes from 'prop-types';
import MicRecorder from 'mic-recorder-to-mp3';
import 'regenerator-runtime/runtime'
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition'

const Mp3Recorder = new MicRecorder({ bitRate: 128 });

const Dictaphone = () => {
  const {
    transcript,
    listening,
    resetTranscript,
    browserSupportsSpeechRecognition
  } = useSpeechRecognition();

  if (!browserSupportsSpeechRecognition) {
    return <span>Browser doesn't support speech recognition.</span>;
  }

  return (
    <div>
      <p>Microphone: {listening ? 'on' : 'off'}</p>
      <button onClick={SpeechRecognition.startListening}>Start</button>
      <button onClick={SpeechRecognition.stopListening}>Stop</button>
      <button onClick={resetTranscript}>Reset</button>
      <p>{transcript}</p>
    </div>
  );
};

class Audio extends React.Component {
  /* Display buttons to choose from
   * Reference on audio player https://github.com/Matheswaaran/react-mp3-audio-recording
   */

  constructor(props) {
    // Initialize mutable state
    super(props);
    this.state = { 
       isRecording: false,
       file: null,
       isBlocked: false,
       entryTitle: '',
       patientDropdown: [],
    };
  }

  componentDidMount() {
    // set state of entry type to begin with
      navigator.mediaDevices.getUserMedia({ audio: true },
        () => {
          console.log('Permission Granted');
          this.setState({ isBlocked: false });
        },
        () => {
          console.log('Permission Denied');
          this.setState({ isBlocked: true })
        },
      );
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
          patientDropdown : data.patients,
        });
      })
      .catch((error) => console.log(error));
    }

  start = () => {
    if (this.state.isBlocked) {
      console.log('Permission Denied');
    } else {
      Mp3Recorder
        .start()
        .then(() => {
          this.setState({ isRecording: true });
        }).catch((e) => console.error(e));
    }
  };

  stop = () => {
    Mp3Recorder
      .stop()
      .getMp3()
      .then(([buffer, blob]) => {
        console.log(buffer, blob);
        const file = new File(buffer, 'music.mp3', {
          type: blob.type,
          lastModified: Date.now()
        });

        this.setState({ file: file, isRecording: false });
      }).catch((e) => console.log(e));
  };

  reset = () => {
    this.state.resetTranscript();
    
  };

  render() {
    let { patientDropdown } = this.state;
    const options = patientDropdown.map((patient) => <option key={patient.username} value={patient.username}>{patient.firstname} {patient.lastname}</option>)
    return (
      <div>
        <Dictaphone></Dictaphone>
        <button onClick={this.start} disabled={this.state.isRecording}>
          Record
        </button><button onClick={this.stop} disabled={!this.state.isRecording}>
          Stop
        </button><audio src={URL.createObjectURL(this.state.file)} controls="controls" />
        <form action="/newentry/" method="post" enctype="multipart/form-data">
          <input type="hidden" name="type" value="audio"/>
          <input type="hidden" name="entry" value={this.state.blobURL}/>
          <div class="d-flex justify-content-center">
            <label for="patient"> Select a patient:</label>
            <select name="patient" id="patient" required>
                {options}
            </select>
          </div>
          <div class="d-flex justify-content-center">
            <input class="mr-sm-2" type="text" placeholder= "Entry Title" name="entrytitle"/>
          </div>
          
          <div class="d-flex justify-content-center">
            <input type="submit" name="createEntry" value="Create Entry"/>
          </div>
        </form>
      </div>
    );
  }
}

export default Audio;
