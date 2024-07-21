# School Management Backend

This project is a Django-based backend for managing school operations, including all what the user need to manage a school.

## Features

- User Authentication (JWT)
- School Management
- Teacher Management
- Student Management
- Seance Management
- Calendar
- Notification System

## Project Structure

Take a look on code

## Getting Started

### Prerequisites

- Python 3.8+
- Django 3.2+
- Django REST Framework
- SimpleJWT

### Installation

1. Clone the repository:

   ```
   > git clone https://github.com/FouadEAF/schoolManagement.git
   > cd schoolManagement
   ```

2. Create and activate a virtual environment:

   > python -m venv venv

   # On Mac, use `source venv/bin/activate`

   # On Windows, use `./venv/Scripts/activate`

3. Install the dependencies:

   > pip install -r requirements.txt

4. Apply the migrations:

   > python manage.py migrations
   > python manage.py migrate

5. Create a superuser:

   > python manage.py createsuperuser

6. Run the development server:
   > python manage.py runserver

### Configuration

Update the settings.py file with your configuration. Key settings include:

- DATABASES
- AUTH_USER_MODEL
- REST_FRAMEWORK
- SIMPLE_JWT

### API Endpoints

1. Authentication
   POST /api/v1/auth/login/: User login
   GET /api/v1/auth/logout/: User logout
   POST /api/v1/auth/register/: User registration
   POST /api/v1/auth/password-reset/: Request password reset
   POST /api/v1/auth/password-reset-confirm/: Confirm password reset

2. School

3. Teacher

4. Student

5. Caldendar

### Contributing

Fork the repository
Create a new branch (git checkout -b feature-branch)
Make your changes
Commit your changes (git commit -m 'Add some feature')
Push to the branch (git push origin feature-branch)
Create a new Pull Request

### License

This project is licensed under the MIT License.

### Contact

For any inquiries, please contact [DevelopperEAF@gmail.com].
