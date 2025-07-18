# from flask import Flask, render_template, request, redirect
# import json
# import boto3
# import uuid

# app = Flask(__name__)

# # S3 setup (bucket name only for now — IAM role or credentials must be configured on EC2)
# S3_BUCKET = 'your-s3-bucket-name'
# s3 = boto3.client('s3')

# # Path to pets.json on EC2 instance
# DATA_FILE = 'data/pets.json'


# # Home page: display all pets
# @app.route('/')
# def index():
#     with open(DATA_FILE, 'r') as f:
#         pets = json.load(f)
#     return render_template('index.html', pets=pets)


# # Add new pet form
# @app.route('/add', methods=['GET', 'POST'])
# def add_pet():
#     if request.method == 'POST':
#         name = request.form['name']
#         age = request.form['age']
#         breed = request.form['breed']
#         photo = request.files['photo']

#         # Upload photo to S3
#         if photo:
#             photo_filename = f"{uuid.uuid4()}_{photo.filename}"
#             s3.upload_fileobj(photo, S3_BUCKET, photo_filename)
#             photo_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{photo_filename}"
#         else:
#             photo_url = ""

#         # Add pet info to JSON file
#         new_pet = {
#             'name': name,
#             'age': age,
#             'breed': breed,
#             'image_url': photo_url
#         }

#         with open(DATA_FILE, 'r+') as f:
#             pets = json.load(f)
#             pets.append(new_pet)
#             f.seek(0)
#             json.dump(pets, f, indent=2)

#         return redirect('/')

#     return render_template('add_pet.html')


# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0')


from flask import Flask, render_template, request, redirect, url_for
import json
import os
import uuid

app = Flask(__name__)

DATA_FILE = 'data/pets.json'
LOCAL_IMG_FOLDER = 'static/img'

@app.route('/')
def index():
    with open(DATA_FILE, 'r') as f:
        pets = json.load(f)
    return render_template('index.html', pets=pets)

@app.route('/add', methods=['GET', 'POST'])
def add_pet():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        breed = request.form['breed']
        photo = request.files['photo']

        if photo:
            ext = os.path.splitext(photo.filename)[1]
            filename = f"{uuid.uuid4()}{ext}"
            filepath = os.path.join(LOCAL_IMG_FOLDER, filename)
            photo.save(filepath)
            photo_url = url_for('static', filename=f'img/{filename}')
        else:
            photo_url = ""

        new_pet = {
            'name': name,
            'age': age,
            'breed': breed,
            'image_url': photo_url
        }

        with open(DATA_FILE, 'r+') as f:
            pets = json.load(f)
            pets.append(new_pet)
            f.seek(0)
            json.dump(pets, f, indent=2)

        return redirect('/')

    return render_template('add_pet.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
