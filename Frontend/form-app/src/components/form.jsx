import React, { Component } from "react";

class Form extends Component {
  render() {
    return (
      <div className="formMain">
        <div className="header">
          <form onSubmit={this.props.submitForm} ref="form">
            <fieldset>
              <legend>Informasjon</legend>
              <label>Navn:</label>
              <input
                type="text"
                name="name"
                value={this.props.name}
                onChange={this.props.handleChange}
                placeholder="Ola Nordmann"
              />
              <br />
              <label>E-post:</label>
              <input
                type="email"
                name="email"
                value={this.props.email}
                onChange={this.props.handleChange}
                placeholder="navn@domene.no"
              />
              <br />
              <label>Telefon:</label>
              <input
                type="tel"
                name="phone"
                value={this.props.phone}
                onChange={this.props.handleChange}
                placeholder="XXX XX XXX"
              />
              <br />
              <label>Postnummer:</label>
              <input
                type="number"
                name="areacode"
                value={this.props.areacode}
                onChange={this.props.handleChange}
                max="9999"
                placeholder="1234"
              />
              <br />
              <label>Kommentar:</label>
              <textarea
                name="comment"
                value={this.props.comment}
                onChange={this.props.handleChange}
              />
              <br />
              <input type="hidden" name="applicant" value="Kjetil Kværnum" />
              <button type="submit">Send inn!</button>
            </fieldset>
          </form>
        </div>
      </div>
    );
  }
}

export default Form;
