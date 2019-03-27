# Frontend Interface
Simple web-app for submitting the form to the API. Found in the *form-app* folder. If you don't want to go through the effort
of installing the requirements of the web-app, you can submit data to the API using the *index.html* file in the *includedFiles* folder.

## Instructions
To run the web-app, there are a few steps you need to do:
* Make sure Node.js and npm is installed on your system ([install guide here](https://www.npmjs.com/get-npm)).
* Navigate to the *form-app* folder with a command line terminal and run the command `npm i`
* After the dependencies are installed, you can run `npm start` to run the app. The app will open in your browser automatically.
* **NB!** Make sure the API is running before trying to submit the form to avoid errors.

## Basic functionality
The app is created using Facebook's *create-react-app* function. This sets up the structure of the app for me and the only 
files I have changed are *src/components/form.jsx*, *src/App.js*, *src/App.css* and *public/index.html*. The first two files 
are the only ones providing utility, while the other two are for styling. 

I did not put alot of effort into the frontend, as I mainly
focused on the backend, and have therefore made a very simple app styled with basic bootstrap. The functionality is mainly:
* Input validation before sending the form
* Posting the form to the API, and collecting the response.
* Desplaying error messages for invalid inputs or messages passed from the API.
