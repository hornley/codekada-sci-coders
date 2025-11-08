# Rekada Lens - Flask Frontend Application

A Flask-served frontend application for product analysis. This application serves static HTML pages with Bootstrap styling and JavaScript functionality.

## Project Structure

```
codekada-sci-coders/
├── app.py                 # Flask application main file
├── requirements.txt       # Python dependencies
├── templates/            # Flask HTML templates
│   ├── landing.html      # Landing page
│   ├── user-setup.html   # User registration/setup
│   ├── dashboard.html    # User dashboard
│   ├── product-analyzer.html  # Product category selection
│   └── product-scanner.html   # Product scanning interface
├── static/              # Static files (CSS, JS, images)
│   ├── css/
│   │   └── style.css    # Custom styles
│   ├── js/
│   │   ├── product-analyzer.js
│   │   ├── product-scanner.js
│   │   └── main.js
│   └── assets/          # Images and other assets
└── README.md
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python app.py
```

The application will be available at: `http://localhost:5000`

### 3. Application Routes

- `/` - Landing page
- `/setup` - User setup/registration
- `/dashboard` - User dashboard
- `/analyzer` - Product analyzer (category selection)
- `/scanner?category=<food|drinks|beauty>` - Product scanner

### 4. API Endpoints (for future backend integration)

- `POST /api/analyze` - Product analysis endpoint
- `GET /api/search` - Product search endpoint
- `POST /api/upload-image` - Image upload and barcode scanning

## Features

### Frontend Features
- **Responsive Design**: Bootstrap 5.3.8 for mobile-first responsive design
- **Product Categories**: Food, Drinks, and Beauty products
- **Multi-step User Setup**: Comprehensive user profile creation
- **Product Analysis Interface**: Multiple input methods (barcode scan, search, manual entry)
- **Toast Notifications**: User feedback for all actions

### Ready for Backend Integration
- **Flask API Routes**: Placeholder endpoints for product analysis
- **Image Upload**: Ready for barcode scanning integration
- **Product Search**: Ready for database integration
- **User Profile Storage**: Currently uses localStorage, ready for database

## Development

### Adding New Features

1. **New Pages**: Add HTML templates to `templates/` directory
2. **New Routes**: Add Flask routes in `app.py`
3. **Static Files**: Add CSS/JS files to `static/` directory
4. **API Integration**: Implement actual logic in the API endpoints

### Frontend Technologies
- **Bootstrap 5.3.8**: UI framework
- **Font Awesome 6.0**: Icons
- **Vanilla JavaScript**: Frontend functionality
- **Local Storage**: Client-side data persistence

### Backend Integration Points
- Product analysis algorithms
- Barcode scanning and OCR
- Product database
- User authentication
- Image processing

## Production Deployment

1. Set `debug=False` in `app.py`
2. Use a production WSGI server like Gunicorn
3. Configure environment variables for production settings
4. Set up proper static file serving (nginx, CDN)

## API Documentation

### Product Analysis API

```python
POST /api/analyze
Content-Type: application/json

{
    "name": "Product Name",
    "brand": "Brand Name",
    "ingredients": "List of ingredients",
    "category": "food|drinks|beauty"
}

Response:
{
    "status": "success",
    "data": {
        "safety_score": 85,
        "recommendations": ["..."],
        "analysis_result": "..."
    }
}
```

### Product Search API

```python
GET /api/search?q=search_term

Response:
{
    "status": "success",
    "results": [
        {
            "id": 1,
            "name": "Product Name",
            "brand": "Brand Name",
            "category": "food"
        }
    ]
}
```