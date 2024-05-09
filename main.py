from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Annotated
import sqlite3
import json


connection = sqlite3.connect('my_database.db')
connection.row_factory = sqlite3.Row 
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Forms (
id INTEGER PRIMARY KEY,
title TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Questionstest (
id INTEGER PRIMARY KEY,
type TEXT NOT NULL,
body TEXT NOT NULL,
form_id INTEGER NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
result TEXT NOT NULL,
form_id INTEGER NOT NULL
)
''')
# cursor.execute('INSERT INTO Forms (title) VALUES (?)', ('TestForm',))
# cursor.execute('INSERT INTO Forms (title) VALUES (?)', ('NewForm',))
# cursor.execute('SELECT * FROM Forms WHERE title IS NOT NULL')
connection.commit()
connection.close()


async def get_form_from_db(
    form_title: str
):
    connection = sqlite3.connect('my_database.db')
    connection.row_factory = sqlite3.Row 
    cursor = connection.cursor()

    # if form_title==None:
    #         cursor.execute('SELECT * FROM Forms')
    #         dataForms = cursor.fetchall()

    #         data = []

    #         for form in dataForms:
    #             form_id = form['id']
    #             cursor.execute(f'SELECT * FROM Questions WHERE form_id IS (?)',(form_id,))
    #             dataQuestions = cursor.fetchall()

    #         data.append({'form':dataForm, 'questions': dataQuestions})
            
    #         connection.commit()

    try:
        cursor.execute('SELECT * FROM Forms WHERE title IS (?)',(form_title,))
        dataForm = cursor.fetchone()

        form_id = dataForm['id']

        cursor.execute('SELECT * FROM Questions WHERE form_id IS (?)',(form_id,))
        dataQuestions = cursor.fetchall()

        data = {'form':dataForm, 'questions': dataQuestions}
        
        connection.commit()

    except TypeError:
        data = 'ERROR: error by get_form_from_db() function'
    
    connection.close()
    return data


async def add_form_to_db(
    form_title: str,
    Qtype: str,
    Qbody: str,
):
    connection = sqlite3.connect('my_database.db')
    connection.row_factory = sqlite3.Row 
    cursor = connection.cursor()
    
    try:
        cursor.execute('INSERT INTO Forms (title) VALUES (?)', (form_title,))

        form_id = cursor.lastrowid

        cursor.execute('INSERT INTO Questions (type, body, form_id) VALUES (?, ?, ?)', (Qtype, Qbody, form_id,))
        
        connection.commit()
    except TypeError:
        data = 'ERROR: error by add_form_to_db() function'

    connection.close()

    return 'Sucessfull'




app = FastAPI()


@app.get("/")
async def read_root():
    forms = await get_form_from_db('TesrForm')
    return forms


@app.get("/forms/{formTitle}")
async def getForm(
    formTitle: str,
):
    forms = await get_form_from_db(formTitle)
    return forms

@app.post("/forms/")
async def getForm(data_json):
    data_json = json.loads(data_json)

    return { await add_form_to_db(data_json['form_title'], data_json['Qtype'], data_json['Qbody'])}