from flask import Flask, render_template, request, make_response
import csv
import os


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def survey():
    # Check if the form has been submitted

    if request.method == 'POST':
        question1 = request.form.get('Question 1')
        question2 = request.form.get('Question 2')
        question3 = request.form.get('Question 3')
        presentation_id = request.form.get('presentation')

        if question1 and question2 and question3:
            answers = request.form.to_dict()  # Answers = form answers
            write_to_csv(answers) # Write Answers to csv file
            submitted = True # Set submitted to True
            return render_template('survey.html', submitted=submitted) # Return submitted screen
        else:
            error_message = 'Please answer all questions.'
            return render_template('survey.html', error_message=error_message)

    # If form has not been submitted yet, display the form to the user
    presentation_id = request.args.get('regid')
    return render_template('survey.html', presentation_id=presentation_id)


def write_to_csv(answers):
    fieldnames = ['presentation', 'Question 1', 'Question 2', 'Question 3']
    file_exists = os.path.isfile('survey_responses.csv')

    with open('survey_responses.csv', 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow(answers)


@app.route('/export', methods=['GET'])
def export_csv():
    with open('survey_responses.csv', 'r') as file:
        response = make_response(file.read())
        response.headers.set('Content-Disposition', 'attachment', filename='survey_responses.csv')
        response.headers.set('Content-Type', 'text/csv')
        return response


if __name__ == '__main__':
    app.run()
