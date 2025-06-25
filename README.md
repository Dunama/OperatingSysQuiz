# CSC201 Python Quiz Application

A web-based quiz platform designed for the CSC201 (Python Programming) course.

## Setup Instructions

1. **Clone the repository**
2. **Create a virtual environment:**  
   `python -m venv venv`
3. **Activate the virtual environment and install dependencies:**  
   `pip install -r requirements.txt`
4. **Configure environment variables:**  
   Create a `.env` file in the project root with the following (replace placeholders with your values):
   ```
   FLASK_APP=src.app
   FLASK_ENV=development
   DATABASE_URL=your_database_url
   SECRET_KEY=your_secret_key
   OAUTH2_CLIENT_ID=your_google_client_id
   OAUTH2_CLIENT_SECRET=your_google_client_secret
   PAYSTACK_SECRET_KEY=your_paystack_key
   ```
5. **Run database migrations:**  
   `flask db upgrade`
6. **Start the development server:**  
   `flask run`

## Features

- Python programming quizzes
- Practice and demo modes
- Question bank for CSC201 topics
- Pro features with payment integration

## License

MIT License – see the [LICENSE](LICENSE) file for details.
