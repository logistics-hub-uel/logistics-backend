### System Requirements

- Python 3.8.10 (recommended for least compatibility issues)
- pip (Python package installer)
- Git
- Docker

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Installation

1. Create a virtual environment

```bash
python3 -m venv venv
```

2. Activate the virtual environment

Ubuntu, MacOS:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

3. Install the dependencies

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory of the project and fill in the necessary environment variables. You can refer to the `.env.example` file for the list of environment variables.

5. Data migration

```bash
alembic upgrade head
```

6. Run the application

```bash
uvicorn app.main:app --reload
```

7. Open your browser and navigate to `http://localhost:8000/docs` to see the Swagger UI.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
