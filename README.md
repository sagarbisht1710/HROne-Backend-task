# HROne Backend Task

This is a backend project built with **FastAPI** and **MongoDB Atlas**, demonstrating RESTful APIs and basic CRUD operations. It is container-ready and deployable on platforms like Render.

---

## 🚀 Features
- **FastAPI** for high-performance backend development.
- **MongoDB Atlas** for database storage.
- **Pydantic** for request/response data validation.
- Modular and scalable project structure.
- Environment configuration via `.env`.
- Ready-to-deploy setup with `run.sh`.

---

## 🛠 Tech Stack
- **Python 3.10+**
- **FastAPI**
- **Uvicorn** (ASGI server)
- **Motor** (Async MongoDB driver)
- **Pydantic** (Data validation)
- **python-dotenv**

---

## 📂 Project Structure
```

HROne-Backend-task/
│
├── app/               # Application code
│   ├── core/          # Core configuration
│   ├── db/            # Database connection logic
│   ├── models/        # Data models
│   ├── routers/       # API routes
│   ├── schemas/       # Pydantic schemas
│   └── utils/         # Helper functions
│
├── main.py            # FastAPI entry point
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
uvicorn main:app --reload
```

The API documentation will be available at:

```
http://127.0.0.1:8000/docs
```

---

## 🌐 Deployment

You can deploy this project on Render or other cloud platforms. The `run.sh` script can be used as a start command:

```bash
bash run.sh
```

---

## 🔗 Connect with Me

* **GitHub Repository:** [https://github.com/sagarbisht1710/HROne-Backend-task](https://github.com/sagarbisht1710/HROne-Backend-task)
* **LinkedIn:** [https://www.linkedin.com/in/sagar-bisht1710/](https://www.linkedin.com/in/sagar-bisht1710/)

```
