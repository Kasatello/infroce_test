# Restaurant

## Installation
1. Clone this repository:

    ```
    git clone https://github.com/Kasatello/infroce_test.git
    ```
 2. Create .env file and define environmental variables following .env.sample:
    ```
    DJANGO_SECRET_KEY=Create youurs at https://djecrety.ir/
    DEBUG=1 for Debug view
    POSTGRES_HOST=your db host
    POSTGRES_DB=name of your db
    POSTGRES_USER=username of your db user
    POSTGRES_PASSWORD=your db password
    ```
 ### 3. To run it locally
> **Warning:** Don't use .env file if You run it locally
1. Create virtual environment and activate it:
   * Tooltip for windows:
     - ```python -m venv venv``` 
     - ```venv\Scripts\activate```
   * Tooltip for mac:
     - ```python -m venv venv```
     - ```source venv/bin/activate```

2. Install dependencies:
    - ```pip install -r requirements.txt```
3. Apply all migrations in database:
   - ```python manage.py migrate```
4. Run server
   - ```python manage.py runserver```

### 3. To run it from docker
1. Run command:
      ```
      docker-compose up --build
      ```

## Used technologies
    - Django framework
    - Django Rest Framework
    - PostgreSQL
    - Docker

## Endpoints
    "restaurants": "http://0.0.0.0:8080/api/v1/restaurants/",
    "menus": "http://0.0.0.0:8080/api/v1/menus/",
    "votes": "http://0.0.0.0:8080/api/v1/votes/"

