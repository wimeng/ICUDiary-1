import React from 'react';
import PropTypes from 'prop-types';
import MicRecorder from 'mic-recorder-to-mp3';
import 'regenerator-runtime/runtime';
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition';
import { Navigate } from 'react-router-dom';

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
      <p style={{display: "none"}} id="transcriptId">{transcript}</p>
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
       audioFileURL: null,
       isRecording: false,
       file: new File([], ""),
       isBlocked: false,
       entryTitle: '',
       patientDropdown: [],
       patient: '',
       title: '',
       transcription: ''
    };

    this.submitEntry = this.submitEntry.bind(this);
    this.handlePatientChange = this.handlePatientChange.bind(this);
    this.handleTitleChange = this.handleTitleChange.bind(this);
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
          patient: (data.patients ? data.patients[0].username : ''),
          transcript: ''
        });
      })
      .catch((error) => console.log(error));
    }

  start = () => {
    if (this.state.isBlocked) {
      console.log('Permission Denied');
    } else {
      SpeechRecognition.startListening({continuous: true})
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
          lastModified: Date.now(),
        });

        this.setState({ file: file, isRecording: false, transcript: document.getElementById('transcriptId').innerHTML });
      }).catch((e) => console.log(e));
    SpeechRecognition.stopListening()
  };

  reset = () => {
    SpeechRecognition.resetTranscript();
  };

  submitEntry = (event) => {
    const { title, patient, transcript, file } = this.state;
    event.preventDefault();
    var formData = new FormData();

    formData.append("type", "audio");
    formData.append("title", title);
    formData.append("patient", patient);
    formData.append("transcript", transcript);
    formData.append("file", file);

    var request = new XMLHttpRequest();
    request.open("POST", "/newentry/");
    request.send(formData);
    window.location.replace("/archive/");
    <Navigate to="/archive/"/>



    // event.target.files = [];
    // event.target.files[0] = file;
    // event.target.href = "/newentry/";
    // document.dispatchEvent(event);
    // action: /newentry/
  }

  handlePatientChange(value) {
    debugger;
    this.setState(() => ({
        patient: value,
    }));
  }

  handleTitleChange(event) {
    event.preventDefault();
    this.setState(() => ({
        title: event.target.value,
    }));
  }

  handleTranscriptChange(event) {
    event.preventDefault();
    this.setState(() => ({
        transcript: event.target.value,
    }));
  }

  render() {
    let { patientDropdown, transcript } = this.state;
    return (
      <div>
        <button onClick={this.start} disabled={this.state.isRecording}>
          Record
        </button><button onClick={this.stop} disabled={!this.state.isRecording}>
          Stop
        </button><audio src={URL.createObjectURL(this.state.file)} controls="controls" />
        <form onSubmit={(e) => this.submitEntry(e)} method="post" enctype="multipart/form-data">
          <input type="hidden" name="type" value="audio"/>
          <div class="d-flex justify-content-center">
            <label for="patient"> Select a patient:</label>
            <select name="patient" id="patient" onChange={(e) => this.handlePatientChange(e.target.value)} required>
                {patientDropdown.map((patient) => <option key={patient.username} value={patient.username}>{patient.firstname} {patient.lastname}</option>)}
            </select>
          </div>
          <div class="d-flex justify-content-center">
            <input class="mr-sm-2" type="text" placeholder= "Entry Title" name="entrytitle" onChange={(e) => this.handleTitleChange(e)}/>
          </div>
          <Dictaphone></Dictaphone>
          Transcription:
          <br></br>
          <textarea style={{resize: "both", height: "300px", width: "300px"}} type="text" name="transcript" value={transcript} onChange={(e) => this.handleTranscriptChange(e)}/>
          <div class="d-flex justify-content-center">
            <input type="submit" name="createEntry" value="Create Entry"/>
          </div>
        </form>
      </div>
    );
  }
}

export default Audio;
