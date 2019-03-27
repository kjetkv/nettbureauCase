import React, { Component } from "react";
import Form from "./components/form";
import "./App.css";

// This component is the main app.
class App extends Component {
  constructor(props) {
    // The state stores the user inputs for validation purposes,
    // and a message to show the user if invalid inputs are given.
    super(props);
    this.state = {
      name: "",
      email: "",
      phone: "",
      areacode: "",
      comment: "",
      message: ""
    };
  }

  // Input validation is handled the same way as in the backend:
  // Each field is matched to a regex and the field name is pushed to a list if
  // the input is invalid. In the end, the contents of the list is used to make
  // an error message if needed.
  // Returns true if input is valid and false if any field is invalid
  validateInputs = () => {
    let errorMessage = "";
    let errors = [];
    if (!/^[a-zæøå -]{2,}$/.test(this.state.name.toLowerCase())) {
      errors.push("navn");
    }
    if (
      !/^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$/.test(
        this.state.email.toLowerCase()
      )
    ) {
      errors.push("email-adresse");
    }
    if (!/^((\+47)?|(0047)?|(47)?)[0-9]{8}$/.test(this.state.phone)) {
      errors.push("telefonnummer");
    }
    if (!/^[0-9]{4}$/.test(this.state.areacode)) {
      errors.push("postnummer");
    }
    if (errors.length) {
      errorMessage = "Ugyldig " + errors.join(", ") + ".";
      // Sets the message in the state to the error message made by the invalid fields.
      this.setState({ message: errorMessage });
      return false;
    }
    return true;
  };

  // function for submitting the form.
  submitForm = e => {
    // prevents the default behaviour of redirecting users after the sumbission.
    e.preventDefault();
    // validates inputs and terminates the function if inputs are invalid.
    if (!this.validateInputs()) {
      return;
    }
    // if all inputs are valid, create a FormData-object from the contents of the form
    let formData = new FormData(e.target);
    // Then post the form data to the API.
    fetch("http://localhost:5000/", {
      method: "post",
      body: formData
    })
      // Wait for the response and set the message in the state to the returned message.
      // This could be an error message or a confirmation message.
      .then(resp => resp.json())
      .then(json => {
        this.setState({ message: json["message"] });
      })
      // Catches any error and logs it in the console.
      .catch(error => {
        console.log(error);
      });
  };

  // Handles changes made to any field in the form, updates the state of the app.
  handleChange = e => {
    this.setState({ [e.target.name]: e.target.value });
  };

  // Renders the form and the message in the state.
  // This message will change depending on user inputs and server response.
  render() {
    return (
      <div className="App">
        <Form
          submitForm={this.submitForm}
          name={this.state.name}
          email={this.state.email}
          phone={this.state.phone}
          areacode={this.state.areacode}
          comment={this.state.comment}
          handleChange={this.handleChange}
        />
        {this.state.message}
      </div>
    );
  }
}

export default App;
