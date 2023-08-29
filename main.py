from io import BytesIO
from flask import Flask, render_template, send_file
from flask_bootstrap import Bootstrap
from dotenv import load_dotenv
import os
from form_classes import *

load_dotenv()
UPLOAD_FOLDER = r'static/files/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('CONFIG_KEY')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
Bootstrap(app)


CREATE_TABLE_SYNX = "CREATE TABLE portofolio(project_name, " \
                                            "date, " \
                                            "functie, " \
                                            "categorie, " \
                                            "discription, " \
                                            "photo BLOB NOT NULL," \
                                            "imbd link)"
try:
    db = sqlite3.connect("portofolio.db")
    cursor = db.cursor()
    cursor.execute(CREATE_TABLE_SYNX)
    db.commit()
    cursor.close()
except sqlite3.OperationalError:
    pass


def fetch_projects():
    try:
        db = sqlite3.connect("portofolio.db", check_same_thread=False)
        cursor = db.cursor()
        cursor.execute("SELECT * From portofolio")
        project_list = cursor.fetchall()
        cursor.close()
        return project_list
    except sqlite3.OperationalError as error:
        print(error)

        return "no data"


def write_to_file(data, filename):
    with open(filename, "wb") as file:
        file.write(data)


def calculate_rows():
    database = fetch_projects()
    num_projects = len(database)

    remainder_4 = num_projects % 4
    remainder_5 = num_projects % 5
    remainder_6 = num_projects % 6

    remainder_dict = {
        4: remainder_4,
        5: remainder_5,
        6: remainder_6
      }

    if remainder_4 == 0:
        return 4
    elif remainder_5 == 0:
        return 5
    elif remainder_6 == 0:
        return 6
    else:
        best_num_columns = max(remainder_dict, key=remainder_dict.get)
        return best_num_columns



@app.route("/image/<string:ident>")
def image_route(ident):
    db = sqlite3.connect("portofolio.db", check_same_thread=False)
    cursor = db.cursor()
    cursor.execute("SELECT photo From portofolio WHERE project_name = ?", (ident,))
    result = cursor.fetchone()

    blob_data = result[-1]
    bytes_io = BytesIO(bytes(blob_data))
    return send_file(bytes_io, mimetype='image/png')


@app.route("/image/cover.jpg")
def image_cover():
    img_file = "cover.jpg"
    return send_file(img_file)

@app.route("/")
def home():
    projects_data = fetch_projects()

    num_colums = calculate_rows()
    return render_template("index.html", projects=projects_data, num_colums=num_colums)


@app.route("/add", methods=["GET", "POST"])
def add():
    add_form = AddForm()
    if add_form.validate_on_submit():
        file = add_form.photo.data.read()

        project_name = add_form.project_name.data
        date = add_form.date.data
        functie = add_form.functie.data
        categorie = add_form.categorie.data
        discription = add_form.discription.data
        photo = sqlite3.Binary(file)
        link = add_form.link.data

        if not validate_no_dubble(add_form.project_name):
            project_data = (project_name, date, functie, categorie, discription, photo, link)

            db = sqlite3.connect("portofolio.db", check_same_thread=False)
            cursor = db.cursor()
            cursor.execute("INSERT INTO portofolio VALUES (?, ?, ?, ?, ?, ?, ?)", project_data)
            db.commit()

        return "File has been uploaded"

    return render_template("add.html", form=add_form)


if __name__ == "__main__":
    app.run(debug=True)
