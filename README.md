\# Task Manager API



A RESTful Task Management API built using Django REST Framework. It allows users to register, log in, and perform CRUD operations on tasks.



\## Technologies Used



\- Python

\- Django

\- Django REST Framework

\- SQLite

\- Pytest

\- Pytest-Django

\- Pytest-Cov



\## Features



\- User registration and login

\- Token-based authentication

\- Create, read, update, and delete tasks

\- Task status management

\- Task priority management

\- Input validation

\- Error handling

\- API testing with Pytest



\## Project Structure



```text

task-manager-api/

│

├── config/

├── tasks/

│   ├── migrations/

│   ├── tests/

│   │   ├── test\_unit.py

│   │   └── test\_api.py

│   ├── models.py

│   ├── serializers.py

│   ├── views.py

│   └── urls.py

│

├── manage.py

├── pytest.ini

├── requirements.txt

└── README.md

```



\## Installation



Clone the repository:



```bash

git clone https://github.com/Anuja319/Task\_Manager\_API.git

```



Navigate to the project folder:



```bash

cd Task\_Manager\_API/task-manager-api

```



Create a virtual environment:



```bash

python -m venv venv

```



Activate the virtual environment on Windows:



```powershell

.\\venv\\Scripts\\Activate

```



Install dependencies:



```bash

pip install -r requirements.txt

```



\## Database Setup



Run migrations:



```bash

python manage.py migrate

```



\## Run the Project



```bash

python manage.py runserver

```



The API will be available at:



```text

http://127.0.0.1:8000/

```



\## API Endpoints



| Method | Endpoint | Description |

|---|---|---|

| POST | `/api/register/` | Register a user |

| POST | `/api/login/` | User login |

| GET | `/api/tasks/` | Get all tasks |

| POST | `/api/tasks/` | Create a task |

| GET | `/api/tasks/<id>/` | Get a specific task |

| PUT | `/api/tasks/<id>/` | Update a task |

| DELETE | `/api/tasks/<id>/` | Delete a task |



Task endpoints require token authentication.



\## Testing



Run all tests:



```bash

pytest

```



Run tests with coverage:



```bash

pytest --cov=tasks --cov-report=term-missing

```



Generate an HTML coverage report:



```bash

pytest --cov=tasks --cov-report=html

```



Open the HTML report:



```bash

start htmlcov/index.html

```



Check the minimum 80% coverage requirement:



```bash

pytest --cov=tasks --cov-report=term-missing --cov-fail-under=80

```



\## Test Results



\- Total test cases: 17

\- Passed: 17

\- Failed: 0

\- Code coverage: 96.36%



\## Author



Anuja Kokitkar

