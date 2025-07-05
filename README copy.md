# Task Upload Dashboard Extension

This project provides an end-to-end solution for uploading PDF, PPTX, and TXT files from a browser extension dashboard, storing them in a PostgreSQL database using a FastAPI backend.

---

## Features
- Upload PDF, PPTX, and TXT files from your dashboard
- Files and metadata stored in PostgreSQL (file content as BYTEA)
- List and download uploaded files
- Simple HTML+JS frontend for integration with browser extensions

---

## Setup Instructions

### 1. **Database (PostgreSQL)**
- Install PostgreSQL if not already installed.
- Create a database (default: `postgres`).
- Run the schema to create the table:
  ```sh
  psql -U postgres -d postgres -f schema.sql
  ```
  Adjust `-U` and `-d` as needed for your setup.

### 2. **Backend (FastAPI)**
- Install Python dependencies:
  ```sh
  pip install -r requirements.txt
  ```
- Set the database URL if needed (default is for local Postgres):
  ```sh
  set DATABASE_URL=postgresql://username:password@host:port/dbname  # Windows
  export DATABASE_URL=postgresql://username:password@host:port/dbname  # Mac/Linux
  ```
- Start the FastAPI server:
  ```sh
  uvicorn main:app --reload
  ```
- The API will be available at `http://localhost:8000`.

### 3. **Frontend**
- Open `task_upload.html` in your browser, or integrate its code into your extension dashboard.
- Make sure the `API_URL` in the JS matches your backend address.

---

## API Endpoints
- `POST /upload` — Upload a file (PDF, PPTX, TXT)
- `GET /files` — List uploaded files
- `GET /files/{id}` — Download a file

---

## Security & API Keys
- **Do not expose secret API keys in frontend code.**
- For user authentication, use tokens (e.g., JWT) and send them in the `Authorization` header from the frontend.
- If you need to use a third-party API key, make requests from the backend, not the frontend.
- For production, restrict CORS in `main.py` to your extension's origin.

---

## Example: Sending Auth Token from Frontend
```js
fetch(`${API_URL}/upload`, {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer ' + token
  },
  body: formData
});
```

---

## Customization
- Integrate the HTML/JS into your extension as needed (plain HTML, React, etc.).
- Adjust allowed file types or size limits in `main.py` as required.

---

## License
MIT 