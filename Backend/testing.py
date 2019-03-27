import requests
from util import reset_users, reset_attempts


# Makes a form filled with the input parameters and send it in a POST-request to the server.
# Returns the response from the server.
# Successful response has the field 'valid' set to True.
def test_post(name, email, phone, areacode, comment):
    form_content = {
        'name': name,
        'email': email,
        'phone': phone,
        'areacode': areacode,
        'comment': comment
    }
    response = requests.post("http://127.0.0.1:5000/", data=form_content)
    return response.json()

# Resets the contents of the databases, and runs some tests.
reset_users()
reset_attempts()
print(test_post("Kjetil Kværnum", "kjetil.kvrnum@gmail.com", "12345678", 7031, "Comment about me."))
print(test_post("Ole-Gunnar Hansen", "ole-g@stud.ntnu.com", "+4712675678", 1476, "Comment about me."))
print(test_post("Ole-Gunnar Hansen 2", "asd", "123456789", 14276, "Comment about me."))
print(test_post("Ole", "ole@email.com", "28473653", 1476, "Comment about me.); DROP TABLE users;--"))
