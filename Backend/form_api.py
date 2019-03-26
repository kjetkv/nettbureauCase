from flask import Flask, request
from flask_restful import Resource, Api, abort
from flask_cors import CORS
import sqlite3
from util import init_users, init_attempts, get_attempts
import re
import requests

app = Flask(__name__)
CORS(app)
api = Api(app)
init_users()
init_attempts(True)


class FormChecker(Resource):

    def post(self):
        if get_attempts(request.remote_addr) > 5:
            abort(403, message="Too many sumbissions in the last 20 minutes.")
        errors = []  # Placeholder array for error messages.
        error_message = ""
        name = request.form['name'].lower()
        email = request.form['email'].lower()
        phone = request.form['phone']
        areacode = str(request.form['areacode'])
        comment = request.form['comment']

        # Validate name:
        regex = "^[a-zæøå -]+$"
        if re.search(regex, name) is None:
            errors.append("name")

        # Validate email:
        regex = "^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$"
        if re.search(regex, email) is None:
            errors.append("email")

        # Validate phone:
        regex = "^((\+47)?|(0047)?|(47)?)[0-9]{8}$"
        if re.search(regex, phone) is None:
            errors.append("phone number")
        else:
            phone = phone[-8:]
        # Validate areacode:
        regex = "^[0-9]{4}$"
        if re.search(regex, areacode) is None:
            errors.append("area code")
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
        if errors:
            error_message = "Invalid " + ', '.join(errors) + '.'
        else:
            try:
                with sqlite3.connect("database.db") as connection:
                    cursor = connection.cursor()
                    cursor.execute("INSERT INTO users (name,email,phone,areacode,comment) VALUES (?,?,?,?,?)", (request.form['name'], email, phone, areacode, comment))
            except:
                connection.rollback()
                error_message = "email or phone number already exists"
        if error_message:
            return {'valid': False, 'error': error_message}, 400
        else:
            return {'valid': True}

    def get(self):
        con = sqlite3.connect("database.db")
        con.row_factory = sqlite3.Row
        users = []
        cur = con.cursor()
        cur.execute("SELECT * FROM users")
        columns = [column[0] for column in cur.description]
        for row in cur.fetchall():
            users.append(dict(zip(columns, row)))
        attempts = []
        cur.execute("SELECT * FROM attempts")
        columns = [column[0] for column in cur.description]
        for row in cur.fetchall():
            attempts.append(dict(zip(columns, row)))

        return {'users': users, 'attempts': attempts}


api.add_resource(FormChecker, '/')


if __name__ == '__main__':
    app.run(debug=True)