from flask import Flask, render_template, request, send_from_directory
import csv
import os


app = Flask(__name__, static_url_path='/static', static_folder='static')


@app.route('/', methods=['GET', 'POST'])
def survey():
    # Check if the form has been submitted

    if request.method == 'POST':
        questions = ['question1', 'question2', 'question3', 'question4', 'question5', 'question6', 'question7',
                     'question8', 'question9', 'question10', 'question11', 'question12']

        for question in questions:
            answer = request.form.get(question)
            if not answer:
                error_message = 'Please answer all questions.'
                return render_template('survey.html', error_message=error_message, **request.form)

        # Modify the response for the "agreement" parameter
        agreement = request.form.get('agreement')
        if agreement == 'on':
            agreement = 'agreed'
        else:
            agreement = 'refused'

        # Update the answers dictionary with the modified response
        answers = request.form.to_dict() # Answers = form answers
        answers['agreement'] = agreement
        write_to_csv(answers)
        submitted = True
        return render_template('survey.html', submitted=submitted, **answers)

    # If form has not been submitted yet, display the form to the user
    identifier = request.args.get('regid')
    return render_template('survey.html', identifier=identifier)


def write_to_csv(answers):
    fieldnames = ['identifier', 'date', 'time', 'agreement',
                  'question1', 'question2', 'question3', 'question4', 'question5', 'question6', 'question7',
                  'question8', 'question9', 'question10', 'question11', 'question12']
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


if __name__ == '__main__':
    app.run()
