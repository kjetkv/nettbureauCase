import React, { Component } from "react";
import Form from "./components/form";
import "./App.css";

class App extends Component {
  constructor(props) {
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
      this.setState({ message: errorMessage });
      return false;
    }
    return true;
  };

  submitForm = e => {
    e.preventDefault();
    if (!this.validateInputs()) {
      return;
    }
    let formData = new FormData(e.target);
    fetch("http://localhost:5000/", {
      method: "post",
      body: formData
    })
      .then(resp => resp.json())
      .then(json => {
        this.setState({ message: json["message"] });
      })
      .catch(error => {
        console.log(error);
      });
    e.preventDefault();
  };

  handleChange = e => {
    this.setState({ [e.target.name]: e.target.value });
  };

  render() {
    return (
      <div className="App">
        <h1 className="display-4">Nettbureau Submission Form</h1>
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
