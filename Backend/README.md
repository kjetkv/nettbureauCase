# Backend API
This Backend API will handle form submissions from POST-requests using the micro-framework Flask for python, and some packages related to this framework.

## Instructions
To run the project there are a few steps you need to do:
* Make sure you have Python 3 installed on your system ([Installation guide here](https://realpython.com/installing-python/)).
* Use the commandline to navigate to the *Backend* folder and run the command `pip install -r requirements.txt`
* Stay in the *Backend* folder and run the command `python form_api.py`.

The API is now up and running and will handle any form posted to localhost on port 5000.

To test the system, you can use curl or any frontend solution with a form on the right format, or you could navigate into the *Backend* 
folder with another commandline terminal and run the testing.py file. This will send some POST-requests to the API and print the responses.

The API is currently configured to respond with the contents of the database when it recieves a GET-request. This would of course not be used in production, but is useful for testing purposes as it easily lets you see the contents of both the tables *users* and *attempts* by sending a GET-request to localhost on port 5000, or opening your browser and going to [localhost:5000/](http://localhost:5000/)

## File Descriptions

### form_api.py
Main backend app. Binds to localhost on port 5000 and handles POST- and GET-requests to this adress. Functionality includes:
* Validation of the form fields and protection against injections.
* Storing the submissions in a database table.
* Spam submission prevention measures.

### utils.py
Provides some utility functions used in *form_api.py* and *testing.py*, including:
* Initialization of the tables in the DB.
* Wiping the contents of the tables.
* Function for retrieving the amount of submissions for a given ip in the last 20 minutes, and updating the *attempts* table.

### testing.py
A few simple test requests sent to the API to test some of the validations and sql-injection prevention.
