from flask import Flask, render_template, request, send_from_directory
import csv
import os


app = Flask(__name__, static_url_path='/static', static_folder='static')


@app.route('/', methods=['GET', 'POST'])
def survey():
    # Check if the form has been submitted

    if request.method == 'POST':
        question1 = request.form.get('question1')
        question2 = request.form.get('question2')
        question3 = request.form.get('question3')
        question4 = request.form.get('question4')
        question5 = request.form.get('question5')
        question6 = request.form.get('question6')

        if question1 and question2 and question3 and question4 and question5 and question6:
            answers = request.form.to_dict()  # Answers = form answers
            write_to_csv(answers)  # Write Answers to csv file
            submitted = True  # Set submitted to True
            return render_template('survey.html', submitted=submitted) # Return submitted screen
        else:
            error_message = 'Please answer all questions.'
            return render_template('survey.html', error_message=error_message)

    # If form has not been submitted yet, display the form to the user
    identifier = request.args.get('regid')
    return render_template('survey.html', identifier=identifier)


def write_to_csv(answers):
    fieldnames = ['identifier', 'date', 'time',
                  'question1', 'question2', 'question3', 'question4', 'question5', 'question6']
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
    app.run(debug=True)
