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