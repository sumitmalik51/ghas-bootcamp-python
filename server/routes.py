from flask import request, render_template, render_template_string, jsonify
from flask_login import login_required, current_user

from server.webapp import flaskapp, cursor
from server.models import Book
import logging
import subprocess


logging.basicConfig(filename="logs.log", filemode="w", level=logging.DEBUG)


@flaskapp.route("/")
def index():
    name = request.args.get("name")
    author = request.args.get("author")

    if name:
        cursor.execute("SELECT * FROM books WHERE name LIKE '%" + name + "%'")
        books = [Book(*row) for row in cursor]

    elif author:
        cursor.execute("SELECT * FROM books WHERE author LIKE '%" + author + "%'")
        books = [Book(*row) for row in cursor]

    else:
        cursor.execute("SELECT name, author, read FROM books")
        books = [Book(*row) for row in cursor]

    return render_template("books.html", books=books)

# Uncomment the following lines of code and make a pull request to see CodeQL in action

@flaskapp.route("/log_injections")
def log_injections():
    data = request.args.get("data")
    logging.debug(data)
    return jsonify(data="Log injection vulnerability"), 200


@flaskapp.route("/config/")
@login_required
def config():
    if current_user.is_admin:
        try:
            command = "cat prod.config.yaml"
            data = subprocess.check_output(command, shell=True)
            return data
        except:
            return jsonify(data="Command didn't run"), 200
    else:
        return jsonify(data="You are not an admin"), 403


@flaskapp.route("/read-bad-file")
def read_bad_file():
    file = request.args.get("file")
    with open(file, "r") as f:
        data = f.read()
    logging.debug(data)
    return jsonify(data="Uncontrolled data use in path expression"), 200


@flaskapp.route("/hello")
def hello():
    if request.args.get("name"):
        name = request.args.get("name")
        template = f"""<div><h1>Hello</h1>{name}</div>"""
        logging.debug(str(template))
        return render_template_string(template)


@flaskapp.route("/get_users")
def get_users():
    try:
        hostname = request.args.get("hostname")
        command = "dig " + hostname
        data = subprocess.check_output(command, shell=True)
        return data
    except:
        data = str(hostname) + " username not found"
        return data
