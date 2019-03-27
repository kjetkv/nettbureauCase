from flask import Flask, request
from flask_restful import Resource, Api, abort
from flask_cors import CORS
import sqlite3
from util import init_users, init_attempts, get_attempts
import re
import requests

# Initiates the Flask app and makes it CORS-friendly, then makes an Api-object (Flask-restful).
app = Flask(__name__)
CORS(app)
api = Api(app)
# Initiates the database tables users and attempts and wipes them if they already exists.
# By not passing an argument to these functions, table contents will persist after the app
# restarts. This would be ideal for production, but i leave them as True for testing purposes.
init_users(True)
init_attempts(True)


class FormChecker(Resource):

    # This function is called when the server receives a POST-request.
    def post(self):
        # First check the number of connections received from the same ip and deny access if the number of attempts are higher than 5.
        if get_attempts(request.remote_addr) > 5:
            return {'valid':False, 'message': "Too many submissions, try again in 20 minutes."}, 403
        errors = []  # Placeholder array for errors.
        error_message = "" # Placeholder for the error message
        # Extract user input from the form.
        name = request.form['name'].lower()
        email = request.form['email'].lower()
        phone = request.form['phone']
        areacode = str(request.form['areacode'])
        comment = request.form['comment']

        # Validate name by matching it to a regular expression:
        # All validation checks add the name of the field to the errors array if they don't match.
        regex = "^[a-zæøå -]+$"
        if re.search(regex, name) is None:
            errors.append("name")

        # Validate email by matching it to a regular expression:
        regex = "^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$"
        if re.search(regex, email) is None:
            errors.append("email")

        # Validate phone by matching it to a regular expression:
        regex = "^((\+47)?|(0047)?|(47)?)[0-9]{8}$"
        if re.search(regex, phone) is None:
            errors.append("phone number")
        else:
            phone = phone[-8:]
        # Validate areacode by matching it to a regular expression:
        regex = "^[0-9]{4}$"
        if re.search(regex, areacode) is None:
            errors.append("area code")
        # If the areacode matches the regex, check its validity using Bring's API.
        else:
            bring_resp = requests.get("https://api.bring.com/shippingguide/api/postalCode.json?clientUrl=c&pnr="+areacode)
            bring_resp = bring_resp.json()
            if not bring_resp['valid']:
                errors.append("area code")

        '''
        Since the comment box is not validated using a regular expression preventing the user from inputting
        executable code, it is very important that any SQL statements are written on a format that prevents injections.
        Example (for sqlite3, other db modules might use other placeholder symbols):
        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?)", (name, email, phone, areacode, comment))
        This will prevent injections as the values are treated as strings, not runnable code.
        '''

        # Make a response and return it:
        # Make the error message if errors are not empty.
        if errors:
            error_message = "Invalid " + ', '.join(errors) + '.'
        else:
            # No invalid inputs, try to insert the record to the users table of the database.
            try:
                with sqlite3.connect("database.db") as connection:
                    cursor = connection.cursor()
                    cursor.execute("INSERT INTO users (name,email,phone,areacode,comment) VALUES (?,?,?,?,?)",
                                   (request.form['name'], email, phone, areacode, comment))
            except:
                # Catches the error if the unique fields email and phone are already in the database and adds an error message.
                connection.rollback()
                error_message = "Email or phone number already exists."
        # If error_message is not an empty string, return invalid response with the relevant error message.
        if error_message:
            print(error_message)
            return {'valid': False, 'message': error_message}, 400
        else:
            # Returns a valid response with a message if no errors are encountered.
            return {'valid': True, 'message': "Thank you for your submission."}

    # This function is called whenever the server receives a GET-request.
    def get(self):
        # Retrieve all the users from the DB and make them into a dictionary.
        con = sqlite3.connect("database.db")
        con.row_factory = sqlite3.Row
        users = []
        cur = con.cursor()
        cur.execute("SELECT * FROM users")
        columns = [column[0] for column in cur.description]
        for row in cur.fetchall():
            users.append(dict(zip(columns, row)))
        # Retrieve all the attempts from the DB and make them into a dictionary.
        attempts = []
        cur.execute("SELECT * FROM attempts")
        columns = [column[0] for column in cur.description]
        for row in cur.fetchall():
            attempts.append(dict(zip(columns, row)))
        # Returns all the users and attempts.
        # TODO: This should obviously not be in production.
        return {'users': users, 'attempts': attempts}

# Adds the resource class to the api on the index url (localhost:5000/).
api.add_resource(FormChecker, '/')


if __name__ == '__main__':
    app.run(debug=True)
