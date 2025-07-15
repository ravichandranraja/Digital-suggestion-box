# Digital Suggestion Box

A modern web application built with Django and Tailwind CSS for managing campus suggestions and feedback. Users can submit suggestions anonymously or with their identity, and administrators can review, respond to, and manage these suggestions.

## Features

### For Users
- **User Registration & Authentication**: Secure user accounts with login/logout functionality
- **Anonymous Submissions**: Submit suggestions without revealing identity
- **Suggestion Tracking**: Monitor the status of submitted suggestions (Under Review, Accepted, Rejected)
- **Dashboard**: Personal dashboard showing all submitted suggestions
- **Category-based Organization**: Submit suggestions under specific categories

### For Administrators
- **Admin Panel**: Dedicated interface for managing suggestions and categories
- **Status Management**: Update suggestion status (Under Review, Accepted, Rejected)
- **Reply System**: Respond to suggestions with detailed feedback
- **Category Management**: Add new categories for better organization
- **Full Access**: View all suggestions from all users

### Technical Features
- **Modern UI**: Clean, responsive design using Tailwind CSS
- **Real-time Updates**: AJAX-powered status updates without page refresh
- **Role-based Access**: Different interfaces for users and administrators
- **Database**: SQLite database (easily configurable for MySQL/PostgreSQL)

## Technology Stack

- **Backend**: Django 4.x (Python)
- **Frontend**: HTML5, Tailwind CSS (via CDN)
- **Database**: SQLite (default), MySQL/PostgreSQL (configurable)
- **Authentication**: Django's built-in authentication system

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd Digital_Suggestion_Box
```

### Step 2: Install Dependencies
```bash
pip install django
```

### Step 3: Run Migrations
```bash
python manage.py migrate
```

### Step 4: Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### Step 5: Create Default Categories
```bash
python manage.py create_default_categories
```

### Step 6: Run the Development Server
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Usage

### For Regular Users

1. **Register/Login**: Create an account or log in to existing account
2. **Submit Suggestions**: 
   - Go to the home page
   - Fill out the suggestion form
   - Choose a category
   - Optionally submit anonymously
3. **Track Progress**: 
   - Visit your dashboard to see all submitted suggestions
   - Check status updates
   - View admin responses

### For Administrators

1. **Access Admin Panel**: Use the "Admin Panel" link in navigation
2. **Manage Categories**: Add new categories for better organization
3. **Review Suggestions**: 
   - View all pending suggestions
   - Update status (Under Review, Accepted, Rejected)
   - Add detailed replies
4. **Monitor Activity**: Track all user submissions and responses

## Database Configuration

### SQLite (Default)
The application uses SQLite by default, which requires no additional setup.


## Project Structure

```
Digital_Suggestion_Box/
├── core/                          # Main application
│   ├── models.py                  # Database models
│   ├── views.py                   # View functions
│   ├── forms.py                   # Django forms
│   ├── urls.py                    # URL patterns
│   ├── templates/core/            # HTML templates
│   └── management/commands/       # Custom management commands
├── suggestion_box/                # Django project settings
│   ├── settings.py               # Project configuration
│   └── urls.py                   # Main URL configuration
├── manage.py                     # Django management script
└── README.md                     # This file
```

## Models

### Category
- `name`: Category name (unique)
- `created_by`: User who created the category
- `created_at`: Creation timestamp

### Suggestion
- `user`: User who submitted (optional for anonymous)
- `is_anonymous`: Boolean flag for anonymous submissions
- `category`: Associated category
- `title`: Suggestion title
- `content`: Detailed suggestion content
- `status`: Current status (under_review, accepted, rejected)
- `created_at`: Submission timestamp
- `updated_at`: Last update timestamp

### Reply
- `suggestion`: Associated suggestion
- `admin`: Admin user who replied
- `content`: Reply content
- `created_at`: Reply timestamp

## Customization

### Adding New Categories
Use the admin panel or run the management command:
```bash
python manage.py create_default_categories
```

### Styling
The application uses Tailwind CSS via CDN. To customize styles:
1. Modify the Tailwind configuration in `core/templates/core/base.html`
2. Update CSS classes in templates
3. Consider installing Tailwind locally for production

### Features
To add new features:
1. Update models in `core/models.py`
2. Create migrations: `python manage.py makemigrations`
3. Apply migrations: `python manage.py migrate`
4. Update views, forms, and templates as needed

## Security Features

- CSRF protection on all forms
- User authentication and authorization
- Role-based access control
- Input validation and sanitization
- Secure password handling

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request
 