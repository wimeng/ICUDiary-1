import React from 'react';
import PropTypes from 'prop-types';
import PasswordStrengthBar from 'react-password-strength-bar';

class StrengthChecker extends React.Component {
  /* Display buttons to choose form
   * Reference on forms https://facebook.github.io/react/docs/forms.html
   */

  constructor(props) {
    // Initialize mutable state
    super(props);
    this.state = { 
        password: ""
    };
  }

  componentDidMount() {
    // set state of entry type to begin with
    this.setState({ 
        password: "",
    });
    }

    handleChange(event) {
        event.preventDefault();
            this.setState(() => ({
                password: event.target.value,
            }));
        }
      
  render() {
    let { password } = this.state;
    return (
      <span className="buttons">
        <span>Password </span>
        <input type="password" name="password" onChange={(e) => {this.handleChange(e)}} value={password} required/>
        <PasswordStrengthBar password={password} onChangeScore={(score, feedback) => {console.log(feedback); console.log(document.getElementById("strengthCheckedPassword").lastElementChild.lastElementChild.lastElementChild.innerHTML);}}></PasswordStrengthBar>
      </span>
    );
  }
}

export default StrengthChecker;
