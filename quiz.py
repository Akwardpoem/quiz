# Здесь будет код веб-приложения
# Здесь будет код веб-приложения
# Здесь будет код веб-приложения
from flask import Flask, redirect, url_for, session, request, render_template
import random
import db_scripts
import os

#quiz_id = 0
#last_question = 0

def start_quiz(id):
    session['quiz_id'] = id
    session['last_question'] = 0
    session['answers'] = 0
    session['total'] = 0

def end_quiz():
    session.clear()

def html_form(quizs):
    html_start = '''<html><body><h3>Выберите номер квиза</h3>'''
    form = '''<form method="post" action="/">'''
    elements = '''<select name="quiz">'''

    for id, name in quizs:
        elements += f'''<option value='{id}'>{name}</option>'''

    elements += '''</select>'''
    frm_submit = '''<p><input type="submit" value="Выбрать"> </p>'''
    return html_start + form + elements + frm_submit + '''</form></body></html>'''

def save_answers():
    answer = request.form.get('ans_text')
    quest_id = request.form.get('quest_id')

    session['last_question'] = quest_id
    session['total'] += 1

    if db_scripts.check_answer(quest_id,answer):
        session['answers'] += 1


def index():
    if request.method == 'GET':
        start_quiz(-1)
        #session['quiz_id'] = db_scripts.get_random_quiz()
        #session['last_question'] = 0
        quiz = db_scripts.get_quiz_form()
        return render_template('start.html',quiz_list=quiz)

    if request.method == 'POST':
        start_quiz(request.form.get('quiz'))
        return redirect(url_for('question'))


def question():
    if int(session['quiz_id']) < 0 or not ('quiz_id' in session):
        return redirect(url_for('index'))

    if request.method == 'POST':
        save_answers()

    quest = db_scripts.get_question_after(session['last_question'],session['quiz_id'])

    if quest == None:
        return redirect(url_for('result'))
    
    session['last_question'] = quest[0]

    answers = [quest[2], quest[3], quest[4], quest[5]]
    random.shuffle(answers)

    return render_template('test.html', question=quest[1], question_id=quest[0], answers=answers)

def result():
    answers = session['answers']
    total = session['total']
    end_quiz()
    return render_template('result.html', answers = answers, total = total)

folder = os.getcwd()
app = Flask(__name__, template_folder=folder, static_folder=folder)

app.config['SECRET_KEY'] = 'qwertyuiop['

#session['quiz_id'] = 0


app.add_url_rule('/','index',index,methods=['GET','POST'])
app.add_url_rule('/question','question',question, methods=['GET','POST'])
app.add_url_rule('/result','result',result)


if __name__ == "__main__":
    db_scripts.main()
    app.run(host='0.0.0.0', port=5000)
    #192.168.1.10