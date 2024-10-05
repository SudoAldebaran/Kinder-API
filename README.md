# Kinder API

## Description
Kinder API is a Django-based application that helps manage invitations and households for parents. It allows users to send invitations to other parents, accept or decline invitations, and manage their children and household information.

## Features
- Create and manage parent accounts.
- Send invitations to other parents.
- Accept or decline invitations.
- Manage children and household relationships.

## Requirements
- Python 3.x
- Django
- Django REST Framework
- Cloud Service (Heroku, AWS, DigitalOcean)
- PostgreSQL (deployment)

## Installation

### Local Setup

Clone the repository:
   ```bash
   git clone https://github.com/SudoAldebaran/Kinder-API.git
   cd Kinder-API
   ```

Create a virtual environment:

    ```bash
    python -m venv venv
    ```

Activate the virtual environment:

    ```bash
    source venv/bin/activate
    ```

Run migrations:

    ```bash
    python manage.py migrate
    ```

Run the development server:

    ```bash
    python manage.py runserver
    ````
