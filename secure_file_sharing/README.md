# File sharing system

- This is a django website to share files securely b/w 2 type of users: ops and client.
- ops user can upload files while clients can sign up, verify email, login and download.
- only .pptx, .docx, and .xlsx formats allowed.

# Features:

-User Authentication: Ops Users and Client Users can create accounts and log in.

-File Upload: Ops Users can upload files, limited to .pptx, .docx, and .xlsx formats.

-Email Verification: Client Users receive an email verification link upon sign-up.

-Secure File Download: Client Users can download files with secure, encrypted URLs.

-File Listing: Client Users can view a list of all uploaded files.

# Installation and Setup

1. Clone the repo.
2. Install all dependecies  (pip install -r requirements.txt)
3. Apply database migration (python manage.py makemigrations ,python manage.py migrate)
4. Create superuser (python manage.py createsuperuser)
5. Run development server (python manage.py runserver)

# Testing

**To run the included test cases, use the following command : python manage.py test

# Deployment

Deploying your Secure File Sharing System to a production environment involves a few steps :

1. You'll need a server to host your application. You can use services like AWS.
2. Install the necessary dependencies on your server.
3. Set up a production database for your application. (like PostgreSQL)
4. Configure static and media files (CSS, javascript and uploaded files)
5. Apllication and Web server to manage requests.
6. ssl/tls certificates. (encrypt the data and secure the sites)

PS:
-Dev. env :- I used github codespaces (cloud-based development environment integrated with github) for development of this project.