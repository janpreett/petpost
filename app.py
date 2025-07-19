from flask import Flask, render_template, request, redirect, url_for
import json
import uuid
import boto3
import os

app = Flask(__name__)

S3_BUCKET = 'petpost-images-1'
DATA_FILE = 'data/pets.json'

s3 = boto3.client('s3')

@app.route('/')
def index():
    # Load pets from JSON file
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

        photo_url = ""
        if photo:
            # Create unique filename for S3
            ext = os.path.splitext(photo.filename)[1]
            photo_filename = f"{uuid.uuid4()}{ext}"

            # Upload photo to S3 bucket
            s3.upload_fileobj(photo, S3_BUCKET, photo_filename)

            # Construct public URL to photo
            photo_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{photo_filename}"

        # Create new pet dict
        new_pet = {
            'name': name,
            'age': age,
            'breed': breed,
            'photo': photo_url
        }

        # Append new pet to JSON file
        with open(DATA_FILE, 'r+') as f:
            pets = json.load(f)
            pets.append(new_pet)
            f.seek(0)
            json.dump(pets, f, indent=2)
            f.truncate()

        return redirect(url_for('index'))

    return render_template('add_pet.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
