from flask import Flask, render_template, request, redirect, url_for, flash
import pymongo
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os

load_dotenv()

# declare the global variables to store the URL to the Mongo database
# and the name of the database that we want to use
MONGO_URL = os.environ.get('MONGO_URL')
DB_NAME = "tgc8_animal_shelter"

# create the Mongo client
client = pymongo.MongoClient(MONGO_URL)
# as db variable is outside of every functions, it is a global variable
# we can use the db variable inside any functions
db = client[DB_NAME]

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')


@app.route('/animals')
def show_animals():
    all_animals = db.animals.find()
    return render_template('all_animals.template.html',
                           all_animals=all_animals)


@app.route('/animals/search')
def show_search_form():
    return render_template('search.template.html')


@app.route('/animals/search', methods=['POST'])
def process_search_form():
    animal_name = request.form.get('animal_name')
    species = request.form.get('species')
    tags = request.form.getlist('tags')

    print(tags)

    critera = {}

    if animal_name:
        critera['name'] = {
            '$regex': animal_name,
            '$options': 'i'  # i means 'case-insensitive'
        }

    if species:
        critera['species'] = {
            '$regex': species,
            '$options': 'i'
        }

    if len(tags) > 0:
        critera['tags'] = {
            '$in': tags
        }

    # put all the search critera into a list for easier processing
    searched_by = [animal_name, species]

    print(critera)

    results = db.animals.find(critera)
    return render_template('display_results.template.html',
                           all_animals=results,
                           searched_by=searched_by)


@app.route('/animals/create')
def show_create_animal():
    return render_template('create_animal.template.html')


@app.route('/animals/create', methods=['POST'])
def process_create_animal():
    name = request.form.get('animal_name')
    species = request.form.get('species')
    breed = request.form.get('breed')
    age = request.form.get('age')
    if age.isnumeric():
        age = float(age)
    microchip = request.form.get('microchip')

    if len(name) == 0:
        flash("Name cannot be empty", "error")
        return render_template('create_animal.template.html')

    new_record = {
        'name': name,
        'age': age,
        'species': species,
        'breed': breed,
        'microchip': microchip
    }

    db.animals.insert_one(new_record)
    flash("New animal created successful", "success")
    return redirect(url_for('show_animals'))


@app.route('/animals/edit/<animal_id>')
def show_edit_animal(animal_id):
    animal = db.animals.find_one({
        '_id': ObjectId(animal_id)
    })
    return render_template('edit_animal.template.html', animal=animal)


@app.route('/animals/edit/<animal_id>', methods=["POST"])
def process_edit_animal(animal_id):
    name = request.form.get('animal_name')
    species = request.form.get('species')
    breed = request.form.get('breed')
    age = float(request.form.get('age'))
    microchip = request.form.get('microchip')

    db.animals.update_one({
        "_id": ObjectId(animal_id)
    }, {
        '$set': {
            'name': name,
            'species': species,
            'breed': breed,
            'age': age,
            'microchip': microchip
        }
    })
    return redirect(url_for('show_animals'))


@app.route('/animals/delete/<animal_id>')
def show_confirm_delete(animal_id):
    # should use find_one if I am only expecting one result
    animal_to_be_deleted = db.animals.find_one({
        '_id': ObjectId(animal_id)
    })
    return render_template('show_confirm_delete.template.html',
                           animal=animal_to_be_deleted)


@app.route('/animals/delete/<animal_id>', methods=["POST"])
def confirm_delete(animal_id):
    db.animals.remove({
        "_id": ObjectId(animal_id)
    })
    return redirect(url_for('show_animals'))


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
