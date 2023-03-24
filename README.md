# lab-test-app
This is an app I built with the help of ChatGPT with GPT4

The goal of the app is to allow users to upload Lab Test results in pdf format, and have server side code extract that data into tabular format for tracking, analysis, etc.

As of now, user sign up and authentication is completed using Flask, and the front end code uses vanilla JavaScript.

You can see how I worked on this project with the help of ChatGPT in the txt file in this repository which I exported using Chrome Extension called "Save ChatGPT"


##Background
the backend application will upload the .pdf file to a Google Cloud Storage bucket, using a service account. Anyone using this code will need to replace 'storage-key.json' with their own service account key in order for this to work properly in your own environment. 

The application front end includes javascript code that will make http calls to the backend running in python using the Flask framework. As this is still in development this will only work locally, but will eventually live on a Cloud Run container. Stay tuned. 

To run the app locally, clone this repo and complete the follow steps.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```
navigate to http://localhost:5000 to access the app. It will not upload files correctly unless you have a GCS bucket with the service account properly set up. 
