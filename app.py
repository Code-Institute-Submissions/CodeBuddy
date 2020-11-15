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
# comments = db.comments

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
    thread_title = request.form.get('thread_title')
    # category = request.form.get('category')
    # tags = request.form.getlist('tags')
    # print(tags)

    critera = {}

    if thread_title:
        critera['name'] = {
            '$regex': thread_title,
            '$options': 'i'  # i means 'case-insensitive'
        }

    # if category:
    #     critera['category'] = {
    #         '$regex': category,
    #         '$options': 'i'
    #     }

    # if len(tags) > 0:
    #     critera['tags'] = {
    #         '$in': tags
    #     }

    # put all the search critera into a list for easier processing
    searched_by = [thread_title]
    # [,category]

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
    thread_title = request.form.get('thread_title')
    thread_article = request.form.get('thread_article')
    thread_author = request.form.get('thread_author')
    thread_author_email = request.form.get('thread_author_email')
    # convert email to lowercase
    # remove first and last space of email input
    thread_author_email = thread_author_email.lower()
    thread_author_email = thread_author_email.strip()

    if len(thread_title) == 0 or len(thread_author) == 0 or len(thread_author_email) == 0 or len(thread_article) == 0:
        flash("Please ensure all fields are filled!", "error")
        return render_template('create_thread.html')

    new_record = {
        'thread_title': thread_title,
        'thread_article': thread_article,
        'thread_author': thread_author,
        'thread_author_email': thread_author_email,
        'thread_datetime': datetime.datetime.now(),
    }

    db.threads.insert_one(new_record)
    flash("Thread created successfully!", "success")
    return redirect(url_for('show_threads'))


@app.route('/threads/edit/<thread_id>')
def show_edit_thread(thread_id):
    threads = db.threads.find_one({
        '_id': ObjectId(thread_id)
    })
    return render_template('edit_thread.html', threads=threads)

@app.route('/threads/edit/<thread_id>', methods=["POST"])
def process_edit_thread(thread_id):
    threads = db.threads.find_one({
        '_id': ObjectId(thread_id)
    })
    thread_title = request.form.get('thread_title')
    thread_article = request.form.get('thread_article')
    thread_author = request.form.get('thread_author')
    thread_author_email = request.form.get('thread_author_email')
    auth_email = thread_author_email.lower()
    auth_email = auth_email.strip()
    # grab email from mongodb
    original_email = threads["thread_author_email"]
    # if email from mongodb dont match email from user input
    if original_email != auth_email:
        flash("Your email does not match the original record for this post. Edit was unsuccessful, changes were not saved.", "error")
        return render_template('edit_thread.html', threads=threads)

    # ensure edited fields have content
    elif len(thread_title) == 0 or len(thread_article) == 0:
        flash("Please ensure all field are filled! Your changes were not saved.", "error")
        return render_template('edit_thread.html', threads=threads)

    db.threads.update_one({
        '_id': ObjectId(thread_id)
    }, {
        '$set': {            
            'thread_title': thread_title,
            'thread_article': thread_article,
            # 'thread_author': thread_author,
            # 'thread_author_email': thread_author_email,
            'thread_datetime_edited': datetime.datetime.now(),
        }
    })
    flash("Article updated successfully!", "success")
    threads = db.threads.find_one({'_id': ObjectId(thread_id)})
    comments = db.comments.find({'thread_id': thread_id})
    return render_template('single_thread.html', threads=threads, comments=comments)

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
        '_id': ObjectId(thread_id)
    })
    return redirect(url_for('show_threads'))

# show single thread
@app.route('/threads/<thread_id>')
def display_thread(thread_id):
    threads = db.threads.find_one({'_id': ObjectId(thread_id)})
    comments = db.comments.find({'thread_id': thread_id})
    return render_template('single_thread.html', threads=threads, comments=comments)

# create comment
@app.route('/threads/comments', methods=["POST"])
def comments_new():
    thread_id = request.form.get('thread_id')
    comment = request.form.get('comment')
    commenter_name = request.form.get('commenter_name')
    commenter_email = request.form.get('commenter_email')
    if len(comment) == 0 or len(commenter_name) == 0 or len(commenter_email) == 0:
        flash("Please ensure all comments field are filled!", "error")
        return redirect(url_for('display_thread', thread_id=request.form.get('thread_id')))
    # convert email input to lowercase
    # remove first and last spaces of input
    commenter_email = commenter_email.lower()
    commenter_email = commenter_email.strip()
    new_comment = {
        'thread_id': thread_id,
        'comment': comment,
        'commenter_name': commenter_name,
        'commenter_email': commenter_email,
        'comment_datetime': datetime.datetime.now(),
    }

    db.comments.insert_one(new_comment)
    flash("Comment posted successfully!", "success")
    return redirect(url_for('display_thread', thread_id=request.form.get('thread_id')))

# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
