# SmartProfile - Professional Portfolio Website

A modern, responsive portfolio website built with Django and Tailwind CSS to showcase Satyajeet Suryawanshi's professional experience, skills, and projects.

## Features

- Dynamic content management through Django Admin
- Responsive design with Tailwind CSS
- Dark/Light mode toggle
- Project filtering by category
- Skills visualization with progress bars
- Contact form with email notifications
- Analytics dashboard for page visits
- GitHub integration for displaying recent activities
- SEO-friendly meta tags
- Resume download functionality

## Tech Stack

- Backend: Django 4.x, Django REST Framework
- Database: PostgreSQL
- Frontend: HTML5, Tailwind CSS, Alpine.js, HTMX
- Authentication: Django's built-in auth system
- Email: SMTP (Gmail)
- Form Protection: reCAPTCHA
- Static Files: Whitenoise
- PDF Generation: WeasyPrint

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/satyajeet1400/smartprofile.git
   cd smartprofile
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory with the following variables:
   ```env
   DEBUG=True
   SECRET_KEY=your_secret_key
   DATABASE_URL=postgres://user:password@host:port/dbname
   EMAIL_HOST_USER=your_email@gmail.com
   EMAIL_HOST_PASSWORD=your_app_password
   DEFAULT_FROM_EMAIL=your_email@gmail.com
   RECAPTCHA_PUBLIC_KEY=your_recaptcha_public_key
   RECAPTCHA_PRIVATE_KEY=your_recaptcha_private_key
   ```

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

8. Visit http://127.0.0.1:8000/admin to add your profile, skills, projects, and experiences.

## Deployment Instructions

### Deploying to Heroku

1. Install Heroku CLI and login:
   ```bash
   heroku login
   ```

2. Create a new Heroku app:
   ```bash
   heroku create your-app-name
   ```

3. Add PostgreSQL addon:
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

4. Configure environment variables in Heroku dashboard or via CLI:
   ```bash
   heroku config:set SECRET_KEY=your_secret_key
   heroku config:set EMAIL_HOST_USER=your_email@gmail.com
   # ... set all other environment variables
   ```

5. Deploy the code:
   ```bash
   git push heroku main
   ```

6. Run migrations:
   ```bash
   heroku run python manage.py migrate
   ```

7. Create superuser:
   ```bash
   heroku run python manage.py createsuperuser
   ```

### Deploying to Render

1. Sign up for a Render account

2. Create a new Web Service:
   - Connect your GitHub repository
   - Choose Python environment
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `gunicorn smartprofile.wsgi:application`

3. Add environment variables in Render dashboard

4. Deploy and monitor the build process

## Regular Maintenance

1. Keep dependencies updated:
   ```bash
   pip install -U pip
   pip install -U -r requirements.txt
   ```

2. Backup database regularly:
   ```bash
   python manage.py dumpdata > backup.json
   ```

3. Monitor error logs and analytics in the admin panel

## License

This project is licensed under the MIT License - see the LICENSE file for details.