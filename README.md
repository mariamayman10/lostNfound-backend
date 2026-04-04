# LostNFound Backend

## Overview
This repository contains the backend API for the LostNFound system.

The backend is built using Flask and Firebase services. It provides secure authentication, database management, and RESTful APIs for handling reports, users, and interactions.

---

## Features

### Authentication and Authorization
- Firebase Authentication integration
- Email verification support
- Token-based authentication
- Protected API endpoints

### User Management
- Store user profile data
- Maintain report count per user

### Report Management (CRUD)
- Create reports
- Retrieve all reports
- Retrieve report by ID
- Update reports
- Filter and search functionality

### Comments System
- Add comments to reports
- Reply to comments
- Associate comments with users and reports

### Search and Filtering
- Filter by type (Lost / Found)
- Filter by status (Open / Claimed / Closed)
- Search by title, location, or category

---

## Tech Stack

- Flask (Python)
- Firebase Admin SDK
- Firestore (NoSQL Database)
- Marshmallow (Data validation)

---

## Database Design

### Users Collection
- uid
- name
- email
- phoneNumber
- imgUrl
- postsCount
- createdAt

### Reports Collection
- uid
- title
- description
- type
- location
- status
- imageUrls (array)
- userId
- createdAt

### Comments Collection
- uid
- content
- reportId
- userId
- parentId
- createdAt

---
## Authentication Flow
  1. User authenticates via Firebase on the frontend
  2. Frontend sends the authentication token to the backend
  3. Backend verifies the token using Firebase Admin SDK
  4. Access is granted to protected endpoints
## API Endpoints
Reports
  - POST /reports
  - GET /reports
  - GET /reports/<id>
  - PUT /reports/<id>
Comments
  - POST /comments
  - GET /reports/<id>/comments

## Key Design Decisions
  - Reference-based relationships to reduce data redundancy
  - Separate comments collection for scalability
  - Support for nested replies via parentId
  - Use of Firestore for flexible schema and scalability

## Related Repository
Frontend: https://github.com/mariamayman10/lostNfound-frontend

## Installation and Setup

```bash
git clone <backend-repository-url>
cd backend
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
flask run
```
### Create a .env file:
```bash
FIREBASE_CREDENTIALS=path/to/firebase_credentials.json
SECRET_KEY=your_secret_key
```
