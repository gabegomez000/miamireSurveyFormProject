from flask import Flask, render_template, request
import datetime
import requests
import os
from dotenv import load_dotenv
from questions import question_list

load_dotenv()

api_url = os.getenv('API_URL')
api_key = os.getenv('API_KEY')

app = Flask(__name__, static_url_path='/static', static_folder='static')


@app.route('/', methods=['GET', 'POST'])
def survey():
    # Check if the form has been submitted
    if request.method == 'POST':
        surveyQuestions = ['ques_1', 'ques_2', 'ques_3', 'ques_4', 'ques_5', 'ques_6',
                           'ques_7', 'ques_8', 'ques_9', 'ques_10', 'ques_11', 'ques_12']
        questionTotal = 0

        for question in surveyQuestions:
            answer = request.form.get(question)
            if not answer:
                error_message = 'Please answer all questions.'
                return render_template('survey.html', error_message=error_message, **request.form)
            else:
                if question in ['ques_1', 'ques_2', 'ques_3', 'ques_5',
                                'ques_6', 'ques_7', 'ques_8', 'ques_9']:
                    print(question + " is equal to " + answer)
                    questionTotal += int(answer)
                    print("questionTotal is equal to " + str(questionTotal))

        numQuestions = 8  # Number of questions that are 1-5 rankings (Do not include text response fields)
        questionAverage = questionTotal / numQuestions
        print("questionAverage is " + str(questionAverage))

        # Modify the response for the "agreement" parameter
        agreement = request.form.get('agreement')
        if agreement == 'on':
            agreement = 'agreed'
        else:
            agreement = 'refused'

        now = datetime.date.today()
        # Update the answers dictionary with the modified response
        answers = request.form.to_dict()  # Answers = form answers
        answers['agreement'] = agreement
        answers['submissionDate'] = now.strftime("%Y-%m-%d")
        """write_to_csv(answers)"""
        push_eval_to_RAMCO(answers, questionAverage)
        submitted = True
        return render_template('survey.html', submitted=submitted, **answers)
    # If form has not been submitted yet, display the form to the user
    regid = request.args.get('regid')
    return render_template('survey.html', regid=regid)


def push_eval_to_RAMCO(answers, questionAverage):
    questionAverage = str(questionAverage)
    regid = request.args.get('regid')
    print("the regid is: " + str(regid))
    api_string = ""
    index = 0
    for key, value in answers.items():
        if key != 'submissionDate' and key != 'regid':
            api_string += f"{question_list[index]['question_text']}"
            index = index + 1
            api_string += f' ({value}) , '

    api_string = api_string[:-2]
    print("api_string is: " + api_string)

    updateEval = {
        'Key': api_key,
        'Operation': 'UpdateEntity',
        'Entity': 'cobalt_classregistration',
        'Guid': regid,
        'AttributeValues': {'ramcosub_evaluationscore=' + questionAverage +
                            ',ramcosub_evaluation=#' + api_string + '#' +
                            ',ramcosub_evaluationdate=#' + answers['submissionDate'] + '#'}
    }

    response = requests.post(api_url, data=updateEval)


"""def write_to_csv(answers):
    fieldnames = ['submissionDate', 'agreement',
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
