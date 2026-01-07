# Todo List

### Description
This project is a task management application that helps users organize and track their daily tasks. It allows users to create, update, and delete todo items, mark tasks as complete or incomplete, and manage their workflow efficiently. Additionally, users can create custom tags and assign them to tasks, making it easier to categorize, filter, and organize tasks based on their needs.

## Getting Started

### Dependencies
- Python
- pip
- Virtual environment tool
- SQLite

### Installing

1. Clone the repository
```
git clone https://github.com/illa-j/Todo-List.git
```

2. Create and activate virtual environment
```
python -m venv venv
source venv/bin/activate
# On Windows: venv\Scripts\activate
```

3. Install required packages
```
pip install -r requirements.txt
```

4. Set up environment variables
```
cp .env.sample .env
# Edit .env with your configuration
```

5. Run migrations
```
python manage.py migrate
```

### Executing program

1. Start the development server
```
python manage.py runserver
```

2. Access the application at `http://127.0.0.1:8000/`

3. Access admin panel at `http://127.0.0.1:8000/admin/`

## Help

Common issue and solution:
- **Migration errors**: Make sure all migrations are applied
```
python manage.py makemigrations
python manage.py migrate
```
