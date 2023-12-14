# Django REST Project

Welcome to the Django REST project! This project provides a RESTful API built with Django.

## Prerequisites

Before you begin, make sure you have the following installed on your machine:

- Python (3.x recommended)
- pip (Python package installer)

## Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/Ramses-Njasap/Django-Group.git
    cd DJANGOPROJECT
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Make migrations
    ```bash
    python manage.py makemigrations
    ```

4. Apply database migrations:

    ```bash
    python manage.py migrate
    ```

5. Create a superuser (admin account):

    ```bash
    python manage.py createsuperuser
    ```

    Follow the prompts to set up your superuser account.

## Run the Development Server

Start the development server:

```bash
python manage.py runserver
