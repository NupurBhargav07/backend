# 📝 Dynamic Questionnaire App

## 📦 Backend Setup (Flask)

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/dynamic-questionnaire.git
cd dynamic-questionnaire/backend
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Initialize Database

```bash
python seed_data.py
```

This will:
- Drop and recreate all tables
- Seed questions, options, and question flows

### 5. Run the Backend Server

```bash
python run.py
```

API will be available at: `http://localhost:5000`

---
