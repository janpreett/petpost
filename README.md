# PetPost

PetPost is a simple website to list adoptable pets. Volunteers can add pets by uploading their name, breed, age, and photo. The website is hosted on AWS EC2. Images are saved in Amazon S3. Pet details are stored in a JSON file.

## Features

- See a list of pets with their info and photo
- Add new pets using a form
- No database needed, uses JSON file
- Hosted on EC2 with images on S3

## Technologies

- Python 3
- Flask (web framework)
- Boto3 (AWS SDK for Python)
- AWS EC2 and S3
- HTML and CSS

## How to run

1. Clone this repo:
    - git clone https://github.com/janpreett/petpost.git
    - cd petpost

2. Install Python packages:
    - pip3 install -r requirements.txt

3. Set up AWS credentials or use IAM role for S3 access.

4. Start the app:
    - python3 app.py

5. Open the website using your EC2 public IP or DNS.

## Project files

- app.py: main Flask app
- requirements.txt: needed Python packages
- data/pets.json: stores pet info
- static/css/style.css: styles
- templates/index.html: pet list page
- templates/add_pet.html: form page
