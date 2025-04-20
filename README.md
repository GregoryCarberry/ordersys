# OrderSys Login System

Minimal working login/logout/session frontend + backend with Docker Compose.

## How to run

1. Build and start:
```bash
docker-compose up --build
```

2. Access:
- Frontend: http://localhost:3000
- Backend: http://localhost:5000

## Default credentials

- Username: `manager`
- Password: `password123`

or

- Username: `staff`
- Password: `password123`

## Features

- Session cookie persists across page refresh
- Role will be accessible after login
- Logout clears session cleanly