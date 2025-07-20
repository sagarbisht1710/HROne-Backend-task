# HROne Backend Task

This is a sample backend project built with **FastAPI** and **MongoDB Atlas**, designed to demonstrate RESTful APIs and basic CRUD operations. It is container-ready and deployable on platforms like Render.

---

## 🚀 Features
- Built using **FastAPI** for high-performance backend.
- **MongoDB Atlas** as the database.
- **Pydantic** for data validation.
- Ready for deployment (e.g., Render).
- Environment-based configuration using `.env`.
- Modular project structure.

---

## 🛠 Tech Stack
- **Python 3.10+**
- **FastAPI**
- **Uvicorn** (ASGI server)
- **Motor** (async MongoDB driver)
- **Pydantic** (data validation)
- **python-dotenv**

---

## 📂 Project Structure
```

HROne-Backend-task/
│
├── src/               # Application source code
│   ├── main.py        # FastAPI entry point
│   ├── routes/        # API route files
│   ├── models/        # Pydantic models
│   └── database/      # MongoDB connection logic
│
├── run.sh             # Script to run the application
├── requirements.txt   # Python dependencies
├── .env               # Environment variables
└── README.md          # Project documentation

````

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/sagarbisht1710/HROne-Backend-task.git
cd HROne-Backend-task
````

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up `.env`

Create a `.env` file and add your environment variables:

```
MONGO_URI=<your-mongodb-atlas-uri>
DB_NAME=<your-database-name>
```

### 5. Run the server

```bash
uvicorn src.main:app --reload
```

The API will be available at:
`https://hrone-backend-task.onrender.com/docs`

---

