from flask import Flask, render_template, request, redirect, url_for, flash
import pymongo
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os

load_dotenv()

# declare the global variables to store the URL to the Mongo database
# and the name of the database that we want to use
MONGO_URL = os.environ.get('MONGO_URL')
DB_NAME = "code_buddy"
#if this does not work then restore to animal list by instructor

# create the Mongo client
client = pymongo.MongoClient(MONGO_URL)
# as db variable is outside of every functions, it is a global variable
# we can use the db variable inside any functions
db = client[DB_NAME]

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

@app.route('/about')
def show_about():
    return render_template('about.template.html')

@app.route('/threads')
def show_threads():
    all_threads = db.threads.find()
    return render_template('all_threads.template.html',
                           all_threads=all_threads)


@app.route('/threads/search')
def show_search_form():
    return render_template('search.template.html')


@app.route('/threads/search', methods=['POST'])
def process_search_form():
    threadname = request.form.get('threadname')
    category = request.form.get('category')
    tags = request.form.getlist('tags')

    print(tags)

    critera = {}

    if threadname:
        critera['name'] = {
            '$regex': threadname,
            '$options': 'i'  # i means 'case-insensitive'
        }

    if category:
        critera['category'] = {
            '$regex': category,
            '$options': 'i'
        }

    if len(tags) > 0:
        critera['tags'] = {
            '$in': tags
        }

    # put all the search critera into a list for easier processing
    searched_by = [threadname, category]

    print(critera)

    results = db.threads.find(critera)
    return render_template('display_results.template.html',
                           all_threads=results,
                           searched_by=searched_by)


@app.route('/threads/create')
def show_create_threads():
    return render_template('create_thread.template.html')


@app.route('/threads/create', methods=['POST'])
def process_create_thread():
    threadname = request.form.get('threadname')
    category = request.form.get('category')
    authorname = request.form.get('authorname')
    authorcontact = request.form.get('authorcontact')
    # if age.isnumeric():
    #     age = float(age)
    article = request.form.get('article')

    if len(threadname) == 0:
        flash("Name cannot be empty", "error")
        return render_template('create_thread.template.html')

    new_record = {
        'threadname': threadname,
        'category': category,
        'authorname': authorname,
        'article': article,
        'authorcontact': authorcontact,
    }

    db.threads.insert_one(new_record)
    flash("New thread posted successfully!", "success")
    return redirect(url_for('show_threads'))


@app.route('/threads/edit/<thread_id>')
def show_edit_thread(thread_id):
    threads = db.threads.find_one({
        '_id': ObjectId(thread_id)
    })
    return render_template('edit_thread.template.html', threads=threads)


@app.route('/threads/edit/<thread_id>', methods=["POST"])
def process_edit_thread(thread_id):
    threadname = request.form.get('threadname')
    category = request.form.get('category')
    authorname = request.form.get('authorname')
    article = (request.form.get('article'))
    authorcontact = request.form.get('authorcontact')

    db.threads.update_one({
        "_id": ObjectId(thread_id)
    }, {
        '$set': {
            'threadname': threadname,
            'category': category,
            'authorname': authorname,
            'article': article,
            'authorcontact': authorcontact,
        }
    })
    return redirect(url_for('show_threads'))


@app.route('/threads/delete/<thread_id>')
def show_confirm_delete(thread_id):
    # should use find_one if I am only expecting one result
    thread_to_be_deleted = db.threads.find_one({
        '_id': ObjectId(thread_id)
    })
    return render_template('show_confirm_delete.template.html',
                           threads=thread_to_be_deleted)


@app.route('/threads/delete/<thread_id>', methods=["POST"])
def confirm_delete(thread_id):
    db.threads.remove({
        "_id": ObjectId(thread_id)
    })
    return redirect(url_for('show_threads'))


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
