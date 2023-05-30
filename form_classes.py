import sqlite3
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import DataRequired


def convert_to_binary(filename):
    with open(filename, "rb") as file:
        blob_data = file.read()

    return blob_data


def allowed_file(filename, extentions):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in extentions

def fetch_projects():
    try:
        db = sqlite3.connect("portfolio.db", check_same_thread=False)
        cursor = db.cursor()
        cursor.execute("SELECT project_name, date, functie, categorie, discription, photo "
                       "FROM portfolio")
        project_list = cursor.fetchall()
        cursor.close()
        return project_list
    except sqlite3.OperationalError as error:
        print(error)


def validate_no_dubble(field):
    db = sqlite3.connect("portfolio.db", check_same_thread=False)
    cursor = db.cursor()
    cursor.execute("SELECT project_name "
                   "FROM portfolio")
    project_list = cursor.fetchone()
    cursor.close()

    try:
        if field.data in project_list:

            return True
        else:

            return False
    except TypeError as error:

        return False


class AddForm(FlaskForm):
    project_name = StringField(label="Project name", validators=[DataRequired()])
    date = DateField(label="When was this project? e.g. 'dd-mm-yy'", validators=[DataRequired()])
    functie = StringField(label="What was your function?", validators=[DataRequired()])
    categorie = StringField(label="what kind of project was it?", validators=[DataRequired()])
    discription = StringField(label="Descipe the project?", validators=[DataRequired()])
    photo = FileField(label="Upload photo", validators=[FileRequired()])
    submit_project = SubmitField("Add project")





