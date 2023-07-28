# question_list.py

question_list = []

question_1 = {
    'question_text': '1. Instructions regarding the rules on attendance, break, etc. were clearly stated at the '
                     'beginning of the course.'
}

question_2 = {
    'question_text': '2. This course met my expectations.'
}

question_3 = {
    'question_text': '3. This course fulfilled its stated objectives.'
}

question_4 = {
    'question_text': '4. Did the course finish on time?'
}

question_5 = {
    'question_text': '5. In-depth knowledge of the subject.'
}

question_6 = {
    'question_text': '6. Overall evaluation of the instructor.'
}

question_7 = {
    'question_text': '7. Instructor was professional and well-prepared for the course.'
}

question_8 = {
    'question_text': '8. Was the instructor completely neutral about his/her affiliation with a company, proprietary '
                     'school, etc.?'
}

question_9 = {
    'question_text': '9. Was the MIAMI staff professional?'
}

question_10 = {
    'question_text': '10. Would you recommend this course to a person considering this program? Please explain why.'
}

question_11 = {
    'question_text': '11. What is the most important thing you will utilize from this class? Please explain why.'
}

question_12 = {
    'question_text': '12. How did you hear about this class?'
}

question_13 = {
    'question_text': 'I authorize the MIAMI REALTORS® to utilize my comments as testimonials.'
}

question_list.append(question_1)
question_list.append(question_2)
question_list.append(question_3)
question_list.append(question_4)
question_list.append(question_5)
question_list.append(question_6)
question_list.append(question_7)
question_list.append(question_8)
question_list.append(question_9)
question_list.append(question_10)
question_list.append(question_11)
question_list.append(question_12)
question_list.append(question_13)

# Print the question_list.
for index, question in enumerate(question_list):
    print(question.get('question_text'))
