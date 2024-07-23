### School Management Backend

This project is a Django-based backend for managing school operations, including all what the user need to manage a school.

### Features

- User Authentication (JWT)
- School Management
- Teacher Management
- Student Management
- Seance Management
- Calendar
- Notification System

### Installation

1. Setup

   - Prerequisites:
     - Python 3.x
     - PostgreSQL or other supported database

2. Installation

   - Clone the Repository: `https://github.com/FouadEAF/school_management.git`
   - Acceder to Repository: `cd school_management`

3. Create and Activate a Virtual Environment

   `python -m venv venv`

- On macOS `source venv/bin/activate`

- On Windows use `.\venv\Scripts\activate`

4. Install Dependencies

   `pip install -r requirements.txt`

5. Configure Environment Variables

Create a `.env` file in the root directory and add the following:

makefile:

    DEBUG=True
    SECRET_KEY=your_secret_key
    DATABASE_URL=your_database_url
    ALLOWED_HOSTS=localhost,127.0.0.1
    Ensure you replace your_secret_key and your_database_url with actual values.

6. Apply Migrations

   `python manage.py migrate`

7. Create a Superuser

   `python manage.py createsuperuser`

8. Run the Server

   `python manage.py runserver`

The API should now be running at http://127.0.0.1:8000.

## API Endpoints

1. Authentication:
   - POST /api/v1/auth/login/ - Log in and receive JWT tokens.
   - GET /api/v1/auth/logout/ - Log out and delete tokens.
   - GET /api/v1/auth/refresh/ - Refresh JWT tokens.
   - POST /api/v1/auth//change-password/ - change the password.
   - POST /api/v1/auth/reset-password/ - Reset user password.
   - POST /api/v1/auth/create/ - Create a new user.
   - PUT /api/v1/auth/edit/ - Update user information.
   - POST /api/v1/auth/me/ - Get the authenticated user’s information.

## Testing

You can test the API using tools like _*Postman*_ or any HTTP client. Make sure to include the Authorization header with the Bearer token for authenticated endpoints.

## Contributing

- Fork the repository.
- Create a new branch (`git checkout -b feature-branch`).
- Commit your changes (`git commit -am 'Add new feature`').
- Push to the branch (`git push origin feature-branch`).
- Create a new Pull Request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

Developper Fouad El Azbi &copy; 2024,
For any questions or issues, please contact [DevelopperEAF@gmail.com].
