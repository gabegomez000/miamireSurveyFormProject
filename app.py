from flask import Flask, render_template, request
import requests
import datetime
import json
import os
from dotenv import load_dotenv
from questions import question_list

load_dotenv()  # Loads .env file

api_url = os.getenv('API_URL')  # Loads API_URL from .env
api_key = os.getenv('API_KEY')  # Loads API_KEY from .env

app = Flask(__name__, static_url_path='/static', static_folder='static')


@app.route('/', methods=['GET', 'POST'])
def survey():
    # Check if the form has been submitted
    if request.method == 'POST':
        surveyQuestions = ['ques_1', 'ques_2', 'ques_3', 'ques_4', 'ques_5', 'ques_6',
                           'ques_7', 'ques_8', 'ques_9', 'ques_10', 'ques_11', 'ques_12']
        questionTotal = 0  # Keeps a tally of the TOTAL question score (Each question is worth 1-5 points)

        for question in surveyQuestions:
            answer = request.form.get(question)
            if not answer:
                error_message = 'Please answer all questions.'
                return render_template('survey.html', error_message=error_message, **request.form)
            else:
                if question in ['ques_1', 'ques_2', 'ques_3', 'ques_5',
                                'ques_6', 'ques_7', 'ques_8', 'ques_9']:
                    questionTotal += int(answer)
        numQuestions = 8  # Number of questions that are 1-5 rankings (Do not include text response fields)
        questionAverage = questionTotal / numQuestions  # Gets the average from 1-5 (This is the Evaluation Score)

        # Modify the response for the "agreement" parameter
        agreement = request.form.get('agreement')  # Retrieves the agreement parameter from the form
        if agreement == 'on':
            agreement = 'agreed'  # Changes answer from 'on' to 'agreed' for when the form gets passed to RAMCO
        else:
            agreement = 'refused'  # Changes answer from 'off' to 'refused' for when the form gets passed to RAMCO

        # Update the answers dictionary with the modified response
        answers = request.form.to_dict()  # Answers = all form answers

        answers['agreement'] = agreement

        """write_to_csv(answers)"""  # Leftover code to call scrapped .csv function
        push_eval_to_RAMCO(answers, questionAverage, answers['regid'])  # Calls the RAMCO push function with parameters
        submitted = True  # Sets submitted to true (Useful for keeping track if answers need to be saved)
        return render_template('survey.html', submitted=submitted, **answers)
    # If form has not been submitted yet, display the form to the user
    regid = request.args.get('regid')  # Retrieves the regid parameter from the URL

    if regid:  # Check if regid was provided, and if so, retrieve course and contact details
        retrieveCourse = {  # Query and query parameters
            'Key': api_key,
            'Operation': 'GetEntity',
            'Entity': 'cobalt_classregistration',
            'Guid': regid,
            'Attributes': {'cobalt_contactid,cobalt_classid,ramcosub_evaluation'}
            }
        courseResponse = requests.post(api_url, data=retrieveCourse)  # Query
        responseJson = json.loads(courseResponse.text)  # Response
        print(responseJson["ResponseCode"])

        # Check if provided regid was valid
        if responseJson["ResponseCode"] == 200:
            courseName = responseJson["Data"]["cobalt_classid"]["Display"]  # Name of course
            contactOriginal = responseJson["Data"]["cobalt_contactid"]["Display"]  # Name of contact
            evalExists = responseJson["Data"]["ramcosub_evaluation"]  # Current Evaluation (If empty, returns None)

            # Separate the contact's first name
            index = contactOriginal.find(',')
            if index == -1:
                contactConverted = contactOriginal
            else:
                contactConverted = contactOriginal[index + 1:]

            if evalExists is not None:  # If an evaluation already exists in RAMCO for this class registration, display a redirect message
                return render_template('survey.html', regid=regid, contact=contactConverted, course=courseName, evalCheck=True)
            else:  # If there is no evaluation yet, proceed with returning the survey form
                return render_template('survey.html', regid=regid, contact=contactConverted, course=courseName, evalCheck=False)
        else:
            # Returns the fallback template for invalid regid; redirects to Miami Realtors website
            return render_template('survey.html', regid=None)
    else:
        # Returns the fallback template for empty regid; redirects to Miami Realtors website
        return render_template('survey.html', regid=None)


def push_eval_to_RAMCO(answers, questionAverage, regid):
    questionAverage = str(questionAverage)  # Converts questionAverage to a string to be saved for the RAMCO response
    api_string = ""  # Used to store the user's responses that will be passed to RAMCO
    index = 0  # Index for loop below
    for key, value in answers.items():  # Used to iterate and add alternating questions and answers for final response
        if key != 'regid':  # Does not iterate through the regid (it's not a question)
            api_string += f"{question_list[index]['question_text']}"
            index = index + 1
            api_string += f" ({value}) , "

    api_string = api_string[:-2]  # Trims extra comma and whitespace at the end of the string

    now = datetime.datetime.today()  # Gets current date
    current_date = now.strftime("%Y-%m-%d")  # Converts current date to string

    """print("api_string is: " + api_string)  # For testing
    print("Guid is: " + regid)
    print("Current Date is: " + current_date)"""

    updateEval = {  # Query and query parameters
        'Key': api_key,
        'Operation': 'UpdateEntity',
        'Entity': 'cobalt_classregistration',
        'Guid': regid,
        'AttributeValues': {'ramcosub_evaluationscoreavg=' + questionAverage +
                            ',ramcosub_evaluationdate=' + current_date +
                            ',ramcosub_evaluation=#' + api_string + '#'}
    }

    requests.post(api_url, data=updateEval)  # Query

    """
    body = json.loads(response.text)
    print("Response Status Code is: " + str(body["ResponseCode"]))  # For Testing
    print("Response Text is: " + str(body["ResponseText"]))
    """
    

"""def write_to_csv(answers):
    fieldnames = ['regid', 'agreement',
                  'ques_1', 'ques_2', 'ques_3', 'ques_4', 'ques_5', 'ques_6', 'ques_7',
                  'ques_8', 'ques_9', 'ques_10', 'ques_11', 'ques_12']
    static_dir = os.path.join(os.getcwd(), 'static')
    file_path = os.path.join(static_dir, 'responses.csv')
    file_exists = os.path.isfile(file_path)

    with open(file_path, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow(answers)


@app.route('/export', methods=['GET'])
def export_csv():
    static_folder = app.root_path + '/static'
    file_path = os.path.join(static_folder, 'responses.csv')

    if os.path.exists(file_path):
        return send_from_directory(static_folder, 'responses.csv', as_attachment=True)
    else:
        return "CSV file not found"
"""

if __name__ == '__main__':
    app.run()
