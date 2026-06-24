import sqlite3
from flask import Flask
import random
db_name = 'quiz.sqlite'
conn = None
curor = None

def open():
    global conn, cursor
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

def close():
    cursor.close()
    conn.close()

def do(query):
    cursor.execute(query)
    conn.commit()

def clear_db():
    ''' удаляет все таблицы '''
    open()
    query = '''DROP TABLE IF EXISTS quiz_content'''
    do(query)
    query = '''DROP TABLE IF EXISTS question'''
    do(query)
    query = '''DROP TABLE IF EXISTS quiz'''
    do(query)
    close()

'''
def create():
    pass
'''
def show(table):
    query = 'SELECT * FROM ' + table
    open()
    cursor.execute(query)
    print(cursor.fetchall())
    close()

def show_tables():
    show('question')
    show('quiz')
    show('quiz_content')




def create():
    open()
    cursor.execute('''PRAGMA foreign_keys=on''')
    do('''CREATE TABLE IF NOT EXISTS quiz (id INTEGER PRIMARY KEY, name VARCHAR)''')
    do('''CREATE TABLE IF NOT EXISTS question (id INTEGER PRIMARY KEY, question VARCHAR, answer VARCHAR, wrong1 VARCHAR, wrong2 VARCHAR, wrong3 VARCHAR)''')
    do('''CREATE TABLE IF NOT EXISTS quiz_content (id INTEGER PRIMARY KEY, quiz_id INTENGER, question_id INTENGER, FOREIGN KEY (quiz_id) REFERENCES quiz (id), FOREIGN KEY (question_id) REFERENCES question (id))''')
    close()

def add_quiz():
    
    quizes = [
        ('Своя игра', ),
        ('Кто хочет стать миллионером?', ),
        ('Самый умный', )]
    
    open()
    cursor.executemany('''INSERT INTO quiz (name) VALUES (?)''', quizes)
    conn.commit()
    close()

def add_question():
    
    questions = [
        ('Сколько месяцев в году имеют 28 дней?', 'Все', 'Один', 'Ни одного', 'Два'),
        ('Каким станет зеленый утес, если упадет в Красное море?', 'Мокрым', 'Красным', 'Не изменится', 'Фиолетовым'),
        ('Какой рукой лучше размешивать чай?', 'Ложкой', 'Правой', 'Левой', 'Любой'),
        ('Что не имеет длины, глубины, ширины, высоты, а можно измерить?', 'Время', 'Глупость', 'Море', 'Воздух'),
        ('Когда сетью можно вытянуть воду?', 'Когда вода замерзла', 'Когда нет рыбы', 'Когда уплыла золотая рыбка', 'Когда сеть порвалась'),
        ('Что больше слона и ничего не весит?', 'Тень слона', 'Воздушный шар', 'Парашют', 'Облако')]
    
    open()
    cursor.executemany('''INSERT INTO question (question, answer, wrong1, wrong2, wrong3) VALUES (?,?,?,?,?)''', questions)
    conn.commit()
    close()

def add_links():
    open()
    cursor.execute('''PRAGMA foreign_key=on''')
    id_ques = [1,2,3,4,5,6]
    id_quize = [1,2,3,1,2,3]
    #while input('Добавить новую связь (y/n)? ') == 'y':
        #id_question = int(input('Введите id вопроса: '))
        #id_quiz = int(input('Введиту id викторины, с которым хотите связвать вопрос: '))
    for i in range(6):
        id_question = id_ques[i]
        id_quiz = id_quize[i]
        cursor.execute('''INSERT INTO quiz_content (quiz_id, question_id) VALUES (?,?)''',[id_quiz, id_question])
        conn.commit()
    close()



def get_question_after(question_id=0,quiz_id=1):
    open()
    cursor.execute('''SELECT quiz_content.id, question.question, question.answer, question.wrong1, question.wrong2, question.wrong3 FROM quiz_content, question WHERE quiz_content.question_id == question.id AND quiz_content.id > ? AND quiz_content.quiz_id == ? ORDER BY quiz_content.id''',[question_id,quiz_id])
    a = cursor.fetchone()
    print(a)
    close()
    return a

def get_quiz_form():
    open()
    cursor.execute('''SELECT * FROM quiz ORDER BY id''')
    a = cursor.fetchall()
    close()
    return a


def get_random_quiz():
    open()
    cursor.execute('''SELECT * FROM quiz ORDER BY id''')
    ids = cursor.fetchall()
    close()
    return ids[random.randint(0,len(ids)-1)][0]


def check_answer(question_id, answer):
    query = "SELECT answer FROM question WHERE question.id = ? "
    open()
    cursor.execute(query,[question_id])
    a = cursor.fetchall()
    close()
    print(a)
    return True if a[0][0] == answer else False

def main():
    clear_db()
    create()
    add_quiz()
    add_question()
    add_links()
    show_tables()

if __name__ == "__main__":
    main()
