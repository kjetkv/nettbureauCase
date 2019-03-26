# Backend API
This Backend API will handle form submissions from POST-requests using the micro-framework Flask for python, and some packages related to this framework.

## Instructions
To run the project there are a few steps you need to do:
* Make sure you have Python 3 installed on your system ([Installation guide here](https://realpython.com/installing-python/)).
* Use the commandline to navigate to the *Backend* folder and run the command `pip install -r requirements.txt`
* Stay in the *Backend* folder and run the command `python form_api.py`.

The API is now up and running and will handle any form posted to localhost on port 5000.

To test the system, you can use curl or any frontend solution with a form on the right format, or you could navigate into the *Backend* 
folder with another commandline terminal and run the tests.py file. This will send some POST-requests to the API and print the responses.
