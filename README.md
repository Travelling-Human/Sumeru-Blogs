# Sumeru Blog

A simple blogging platform built with Django where users can write, manage, and discover blog posts.

## Features

- User registration and login with a custom user model
- Profile page with avatar and bio
- Create, edit, and delete blog posts
- Attach media files to posts
- Organize posts by category and tags
- Comment on posts
- Search posts by title, content, author, tags, or category
- Browse posts by user

## Project Structure

```
sumeru_blog/
    accounts/       - User authentication and profiles
    posts/          - Blog posts, comments, and categories
    templates/      - Base HTML template
    media/          - Uploaded files and avatars
```

## Requirements

- Python 3.12
- Django
- crispy-forms
- Pillow (for image uploads)

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/Travelling-Human/Sumeru-Blogs.git
   cd Sumeru-Blogs
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install django crispy-forms pillow
   ```

4. Apply migrations:
   ```
   python manage.py migrate
   ```

5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

7. Open your browser and go to `http://127.0.0.1:8000`

## Notes

- The project uses SQLite as its database, which is suitable for development.
- Media files are stored in the `media/` directory.
- Debug mode is enabled by default. Do not deploy to production without changing the secret key and disabling debug mode.
