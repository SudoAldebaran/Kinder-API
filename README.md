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
   
   git clone https://github.com/SudoAldebaran/Kinder-API.git
   cd Kinder-API

Create a virtual environment:

    python -m venv venv

Activate the virtual environment:

    source venv/bin/activate

Run migrations:

    python manage.py migrate

Run the development server:

    python manage.py runserver


## API Reference

### Parent Endpoints

#### Get all parents

```http
GET /api/parents/
```

| Parameter | Type     | Description              |
| :-------- | :------- | :----------------------- |
| `None`    | `None`   | **Retrieve all parents** |

#### Create a new parent

```http
POST /api/parents/
```

| Parameter | Type     | Description                   |
| :-------- | :------- | :---------------------------- |
| `name`    | `string` | **Required**. Name of the parent. |
| `email`   | `string` | **Required**. Email of the parent (must be unique). |

#### Get a specific parent

```http
GET /api/parents/{id}/
```

| Parameter | Type     | Description                          |
| :-------- | :------- | :----------------------------------- |
| `id`      | `string` | **Required**. Id of the parent to fetch. |

#### Update a specific parent

```http
PUT /api/parents/{id}/
```

| Parameter | Type     | Description                          |
| :-------- | :------- | :----------------------------------- |
| `id`      | `string` | **Required**. Id of the parent to update. |
| `name`    | `string` | **Optional**. New name for the parent. |
| `email`   | `string` | **Optional**. New email for the parent. |

#### Delete a specific parent

```http
DELETE /api/parents/{id}/
```

| Parameter | Type     | Description                          |
| :-------- | :------- | :----------------------------------- |
| `id`      | `string` | **Required**. Id of the parent to delete. |

### Invitation Endpoints

#### Get all invitations

```http
GET /api/invitations/
```

| Parameter | Type     | Description               |
| :-------- | :------- | :------------------------ |
| `None`    | `None`   | **Retrieve all invitations** |

#### Send a new invitation

```http
POST /api/invitations/
```

| Parameter   | Type     | Description                                |
| :---------- | :------- | :----------------------------------------- |
| `recipient` | `string` | **Required**. Id of the recipient parent. |

#### Accept an invitation

```http
PUT /api/invitations/{id}/accept/
```

| Parameter | Type     | Description                                |
| :-------- | :------- | :----------------------------------------- |
| `id`      | `string` | **Required**. Id of the invitation to accept. |

#### Decline an invitation

```http
DELETE /api/invitations/{id}/
```

| Parameter | Type     | Description                                |
| :-------- | :------- | :----------------------------------------- |
| `id`      | `string` | **Required**. Id of the invitation to decline. |