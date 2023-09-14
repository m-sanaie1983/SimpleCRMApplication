
# Django CRM Application

This is a simple Customer Relationship Management (CRM) application built with Python Django and Dockerized for easy deployment. The application provides basic CRM functionalities for managing customers, deals, and tasks.


## Features
- User authentication and authorization.

- Management of customer records.

- Recording and tracking customer interactions.
## Prerequisites
Before you begin, ensure you have met the following requirements:

- Docker and Docker Compose installed on your system.

- Basic knowledge of Docker and Django.
## Getting Started
1- Clone the repository:

git clone https://github.com/m-sanaie1983/SimpleCRMApplication.git

2- Navigate to the project directory:

cd SimpleCRMApplication

3- Create a .env file in the project root directory and configure your environment variables. You can use the provided .env.example file as a template.

4- Uncomment the PostgreSQL database settings in the project's settings.py file and comment out the SQLite settings if you wish to use PostgreSQL as your database.

## Usage

1- Build and start the Docker containers:

docker-compose up -d --build

2- Collect static files:

docker-compose exec web python manage.py collectstatic

3- Create database migrations:

docker-compose exec web python manage.py makemigrations

4- Apply database migrations:

docker-compose exec web python manage.py migrate

5- Access the CRM application in your web browser:

http://ip-address/

6- You can now log in with the provided admin credentials or create new user accounts to start using the CRM features.

## Acknowledgments

- Django
- Docker
- PostgreSQL
- nginx
