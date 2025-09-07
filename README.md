# Event_Management_API

## 1) Project structure
    event_management_api/
    ├─ manage.py
    ├─ pyproject.toml
    ├─ .env
    ├─ config/
    │  ├─ __init__.py
    │  ├─ settings.py
    │  ├─ urls.py
    │  ├─ wsgi.py
    │  └─ asgi.py
    ├─ users/
    │  ├─ __init__.py
    │  ├─ models.py
    │  ├─ admin.py
    │  ├─ serializers.py
    │  ├─ views.py
    │  ├─ permissions.py
    │  ├─ urls.py
    │  └─ tests.py
    ├─ events/
    │  ├─ __init__.py
    │  ├─ models.py
    │  ├─ admin.py
    │  ├─ serializers.py
    │  ├─ views.py
    │  ├─ permissions.py
    │  ├─ filters.py
    │  ├─ signals.py
    │  ├─ urls.py
    │  └─ tests.py
    ├─ registrations/
    │  ├─ __init__.py
    │  ├─ models.py
    │  ├─ serializers.py
    │  ├─ views.py
    │  ├─ permissions.py
    │  ├─ urls.py
    │  └─ tests.py
    ├─ tickets/
    │  ├─ __init__.py
    │  ├─ models.py
    │  ├─ serializers.py
    │  ├─ views.py
    │  ├─ urls.py
    │  └─ tests.py
    └─ notifications/
    ├─ __init__.py
    ├─ tasks.py
    ├─ services.py
    └─ apps.py

## 2) User Endpoints
🔐 Authentication & User Management
1. *User Register*
    - *POST* /api/users/register/
    - *Request Body:* 
        json
        {
            "username": "johndoe",
            "email": "john@example.com",
            "password": "StrongPass123",
            "first_name": "John",
            "last_name": "Doe",
            "role": "attendee"
        }
    - *Response 201::*
        json
        {
            "id": 2,
            "username": "johndoe",
            "email": "john@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "role": "attendee"
        }
2. *Get JWT Token*
    - *POST* /auth/token/
    - *Request Body:* 
        json
        {
            "username": "johndoe",
            "password": "StrongPass123"
        }
    - *Response 200:*
        json
        {
            "refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9. ...",
            "access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9. ..."
        }
3. *Refresh Token*
    - *POST* /auth/token/refresh/
    - *Request Body:* 
        json
        {
            "refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9. ..."
        }
    - *Response 200:*
        json
        {
            "access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9. ..."
        }
4. *Get Current User Profile*
    - *GET* /api/users/me/
    - *Authorization:* Bearer Token
        Access Token
    - *Response 200:*
        json
        {
            "id":2,
            "username":"johndoe",
            "email":"john@example.com",
            "first_name":"John",
            "last_name":"Doe",
            "role":"attendee"
        }
🎫 Events & Categories
1. *List Categories
    - *GET* /api/events/categories/
    - *Authorization:* No Auth
    - *Response 200:*
        json
        [
            {
                "id": 1,
                "name": "Technology",
                "slug": "technology"
            }
        ]
2. *Create Event (Organizer only)*
    - *POST* /api/events/create/
    - *Authorization:* Bearer Token
        Access Token
    - *Request Body:*
        json
        {
            "title": "Tech Conference 2025",
            "description": "Future of AI and Web",
            "date_time": "2025-12-15T10:00:00Z",
            "location": "New York",
            "capacity": 100,
            "visibility": "public",
            "category": 1
        }
    - *Response 200:*
        json
        {
            "id": 7,
            "title": "Tech Conference 2025",
            "description": "Future of AI and Web",
            "date_time": "2025-12-15T10:00:00Z",
            "location": "New York",
            "capacity": 100,
            "created_at": "2025-09-07T12:58:51.068830Z",
            "organizer": 1,
            "visibility": "public",
            "image": null,
            "category": 1,
            "sessions": [],
            "ticket_types": []
        }
3. *List Events*
    - *GET* /api/events/
    - *Authorization:* No Auth
    - *Response 200:*
        json
        [
            {
                "id": 4,
                "title": "Tech Conference 2025",
                "description": "Future of AI and Web",
                "date_time": "2025-12-15T10:00:00Z",
                "location": "New York",
                "capacity": 100,
                "created_at": "2025-09-04T13:21:45.475714Z",
                "organizer": 1,
                "visibility": "public",
                "image": null,
                "category": 1,
                "sessions": [],
                "ticket_types": [
                    {
                        "id": 1,
                        "name": "General",
                        "price": "50.00",
                        "quantity": 80
                    },
                    {
                        "id": 2,
                        "name": "VIP",
                        "price": "150.00",
                        "quantity": 20
                    }
                ]
            },
            {
                "id": 5,
                "title": "Tech Conference 2025",
                "description": "Future of AI and Web",
                "date_time": "2025-12-15T10:00:00Z",
                "location": "New York",
                "capacity": 100,
                "created_at": "2025-09-07T12:51:42.338108Z",
                "organizer": 1,
                "visibility": "public",
                "image": null,
                "category": 1,
                "sessions": [],
                "ticket_types": []
            }
        ]
4. *Get Single Event*
    - *GET* /api/events/{id}/
    - *Authorization:* No Auth
    - *Response 200:*
        json
        {
            "id": 5,
            "title": "Tech Conference 2025",
            "description": "Future of AI and Web",
            "date_time": "2025-12-15T10:00:00Z",
            "location": "New York",
            "capacity": 100,
            "created_at": "2025-09-07T12:51:42.338108Z",
            "organizer": 1,
            "visibility": "public",
            "image": null,
            "category": 1,
            "sessions": [],
            "ticket_types": []
        }
5. *Update Event (Organizer only)*
    - *PUT* /api/events/{id}/update/
    - *Authorization:* Bearer Token
        Access Token
    - *Request Body:*
        json
        {
            "title": "Tech Conference 2025",
            "description": "Future of AI",
            "date_time": "2025-12-15T10:00:00Z",
            "location": "New York",
            "capacity": 100,
            "visibility": "public",
            "category": 1
        }
    - *Response 200:*
        json
        {
            "id":5,
            "title":"Tech Conference 2025",
            "description":"Future of AI",
            "date_time":"2025-12-15T10:00:00Z",
            "location":"New York",
            "capacity":100,
            "created_at":"2025-09-07T12:51:42.338108Z",
            "organizer":1,
            "visibility":"public",
            "image":null,
            "category":1,
            "sessions":[],
            "ticket_types":[
                {
                    "id":3,
                    "name":"General",
                    "price":"100.00",
                    "quantity":100
                },
                {
                    "id":4,
                    "name":"VIP",
                    "price":"300.00",
                    "quantity":20
                }
            ]
        }
6. *Delete Event (Organizer only)*
    - *DELETE* /api/events/{id}/delete/
    - *Authorization:* Bearer Token
        Access Token

📝 Registrations
1. *Register for Event*
    - *POST* /api/registrations/{event_id}/register/
    - *Authorization:* Bearer Token
        Access Token
    - *Request Body:*
        json
        {
            "ticket_type": 1
        }
    - *Response 200:*
        json
        {
            "id": 1,
            "user": 2,
            "event": 1,
            "ticket_type": 1,
            "registered_at": "2025-09-04T12:30:00Z",
            "is_waitlisted": false,
            "ticket": {
                "code": "5e2a4d53-7b31-4d80-8b61-12ecf0eaa999",
                "issued_at": "2025-09-04T12:30:00Z",
                "is_checked_in": false
            }
        }
2. My Registrations
    - *GET* /registrations/me/
    - *Authorization:* Bearer Token
        Access Token
    - *Response 200:*
        json
        [
            {
                "id": 10,
                "event": 5,
                "ticket_type": 1,
                "registered_at": "2025-09-04T12:00:00Z",
                "is_waitlisted": false
            }
        ]