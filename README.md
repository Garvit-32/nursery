## Nursery app
### Installation:
Requirements:
- Python 3.8.2 runtime
- Django 3.0.0
- Other dependencies in `requirements.txt`



Procedure:
- Install [python](https://www.python.org/downloads/) in your environment(pre-installed on Ubuntu).
- Navigate to the cloned repository.
    ```
    cd <project_directory_name>     # varchas_iitj
    ```
- Install `pipenv` for dependency management
    ```
    pip install pipenv
    ```
- Use pip to install other dependencies from `requirements.txt`
    ```
    pip install -r requirements.txt
    ```

- Optionally activate virtual environment, if you don't want to activate env, use `pipenv run` to run python scripts
    ```
    source "$(pipenv --venv)"/bin/activate
    ```

- Make database migrations
    ``` 
    python manage.py makemigrations
    python manage.py migrate
    ```
    NOTE: If its your first time migrating, you may need to manually add migration module in each app.
    ```
    python manage.py makemigrations store
    python manage.py migrate
    ```
- Create a superuser
    ```
    python manage.py createsuperuser 
    ```
- Run development server on localhost
    ```
    python manage.py runserver 
    ```
    
    
