## Features

- User registration and login
- Token-based authentication using SimpleJWT
- Protected routes for authenticated users
- Logout functionality

## Technologies Used

- Django
- Django Rest Framework
- SimpleJWT
- React
- React Router
- Axios

## Installation

### Backend (Django)

1. Clone the repository:

   ```bash
   git clone https://github.com/pratikrk/Rudrastra_OSINT.git
   cd Django-React-Authentication
   ```

2. Set up a virtual environment and install dependencies:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Run migrations:

   ```bash
   python manage.py migrate
   ```

4. Start the Django development server:
   ```bash
   python manage.py runserver
   ```

# Frontend (React)

1. In a new terminal window, navigate to the project root:

   ```bash
   cd Django-React-Authentication
   ```

2. Install frontend dependencies:

   ```bash
   cd frontend
   npm install
   ```

3. Start the React development server:
   ```bash
   npm start
   ```

# Usage

1. Register a new account or log in with existing credentials.
2. Explore the protected routes available to authenticated users.
3. Log out when done.
