from flask import Flask, render_template, request, redirect, url_for, flash
import pymongo
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os
import datetime
import re

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
#comments db
comments = db.comments

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

@app.route('/about')
def show_about():
    return render_template('about.html')

@app.route('/threads')
def show_threads():
    all_threads = db.threads.find()
    return render_template('all_threads.html',
                           all_threads=all_threads)


@app.route('/threads/search')
def show_search_form():
    return render_template('search_threads.html')


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
    return render_template('display_results.html',
                           all_threads=results,
                           searched_by=searched_by)


@app.route('/threads/create')
def show_create_threads():
    return render_template('create_thread.html')


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
        return render_template('create_thread.html')

    new_record = {
        'threadname': threadname,
        'category': category,
        'authorname': authorname,
        'article': article,
        'authorcontact': authorcontact,
        'datetime': datetime.datetime.now(),
        # time_created : datetime.now (google it & how to format)
    }

    db.threads.insert_one(new_record)
    flash("New thread posted successfully!", "success")
    return redirect(url_for('show_threads'))


@app.route('/threads/edit/<thread_id>')
def show_edit_thread(thread_id):
    threads = db.threads.find_one({
        '_id': ObjectId(thread_id)
    })
    return render_template('edit_thread.html', threads=threads)


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
    return render_template('confirm_delete_thread.html',
                           threads=thread_to_be_deleted)


@app.route('/threads/delete/<thread_id>', methods=["POST"])
def confirm_delete(thread_id):
    db.threads.remove({
        "_id": ObjectId(thread_id)
    })
    return redirect(url_for('show_threads'))

# show single thread
@app.route('/threads/<thread_id>', methods=["GET"])
def display_thread(thread_id):
    threads = db.threads.find_one({
        '_id': ObjectId(thread_id)
    })
    return render_template('single_thread.html', threads=threads)

#route for create comment
@app.route('/threads/comments', methods=["POST"])
def comments_new():
    thread_id = request.form.get('thread_id')
    comment = request.form.get('comment')
    commenter_name = request.form.get('commenter_name')
    commenter_email = request.form.get('commenter_email')
    if len(comment) == 0:
        flash("Comment cannot be empty", "error")
        return redirect(url_for('display_thread', thread_id=request.form.get('thread_id')))

    new_comment = {
        'thread_id': thread_id,
        'comment': comment,
        'commenter_name': commenter_name,
        'commenter_email': commenter_email,
        'comment_datetime': datetime.datetime.now(),
    }

    db.comments.insert_one(new_comment)
    flash("New comment posted successfully!", "success")
    return redirect(url_for('display_thread', thread_id=request.form.get('thread_id')))

# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
