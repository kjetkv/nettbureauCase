import React, { Component } from "react";

// This class contains the same form as provided in the case description.
// The value of the fields are passed as props to the main App (App.js), and
// they all share a common onChange-function for handling user input.
// The onSubmit function is also passed as a prop.
class Form extends Component {
  render() {
    return (
      <div className="formMain">
        <form onSubmit={this.props.submitForm} ref="form">
          <div class="form-group">
            <fieldset>
              <legend>Informasjon</legend>
              <label>Navn:</label>
              <input
                type="text"
                name="name"
                class="form-control"
                value={this.props.name}
                onChange={this.props.handleChange}
                placeholder="Ola Nordmann"
              />
              <br />
              <label>E-post:</label>
              <input
                type="email"
                name="email"
                class="form-control"
                value={this.props.email}
                onChange={this.props.handleChange}
                placeholder="navn@domene.no"
              />
              <br />
              <label>Telefon:</label>
              <input
                type="tel"
                name="phone"
                class="form-control"
                value={this.props.phone}
                onChange={this.props.handleChange}
                placeholder="XXX XX XXX"
              />
              <br />
              <label>Postnummer:</label>
              <input
                type="number"
                name="areacode"
                class="form-control"
                value={this.props.areacode}
                onChange={this.props.handleChange}
                max="9999"
                placeholder="1234"
              />
              <br />
              <label>Kommentar:</label>
              <textarea
                name="comment"
                class="form-control"
                value={this.props.comment}
                onChange={this.props.handleChange}
              />
              <br />
              <input type="hidden" name="applicant" value="Kjetil Kværnum" />
              <button class="btn btn-dark" type="submit">
                Send inn!
              </button>
            </fieldset>
          </div>
        </form>
      </div>
    );
  }
}

export default Form;
