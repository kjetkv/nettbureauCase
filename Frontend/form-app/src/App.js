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
      errorMessage: ""
    };
  }

  validateInputs = () => {
    return true;
  };

  submitForm = e => {
    if (!this.validateInputs()) {
      this.setState({ errorMessage: "Inputs Are wrong!" });
    }
    let formData = new FormData(e.target);
    fetch("http://localhost:5000/", {
      method: "post",
      body: formData
    })
      .then(resp => resp.json())
      .then(json => {
        this.setState({ errorMessage: json["error"] });
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
        {this.state.errorMessage}
      </div>
    );
  }
}

export default App;
