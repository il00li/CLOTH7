# Arabic Clothing Store

## Overview

This is a Flask-based Arabic clothing store web application that provides a bilingual (Arabic/English) e-commerce platform for selling children's clothing. The application features a customer-facing storefront with product browsing and filtering capabilities, plus an admin panel for managing products and store settings.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 templates with Bootstrap 5 RTL for Arabic language support
- **Styling**: Custom CSS with CSS variables for theming, Google Fonts (Cairo) for Arabic typography
- **JavaScript**: Vanilla JavaScript for interactivity, Bootstrap components for UI elements
- **Responsive Design**: Mobile-first approach with Bootstrap grid system

### Backend Architecture
- **Framework**: Flask (Python) with session management
- **Data Storage**: JSON files for products and settings (file-based storage)
- **Authentication**: Simple session-based admin authentication
- **API**: RESTful endpoints for CRUD operations on products and settings

## Key Components

### Core Application Files
- `app.py`: Main Flask application with route handlers and business logic
- `main.py`: Application entry point for development server
- `templates/`: Jinja2 HTML templates for pages
- `static/`: CSS, JavaScript, and asset files
- `data/`: JSON files for persistent data storage

### Data Models
- **Products**: ID, name, price, category, image URL, colors, sizes, material, description
- **Settings**: Store configuration including name, WhatsApp number, colors, social links, delivery areas

### User Interface Components
- **Customer Storefront**: Product catalog with category filtering, responsive card layout
- **Admin Panel**: Product management, settings configuration, tabbed interface
- **Authentication**: Modal-based admin login (triggered by triple-clicking header)

## Data Flow

### Customer Experience
1. User visits homepage displaying all products
2. Products can be filtered by category (أولاد/بنات/شتوي)
3. Product information displayed in Arabic with RTL layout
4. Contact options available through WhatsApp integration

### Admin Workflow
1. Admin accesses panel by triple-clicking header and entering credentials
2. CRUD operations on products through modal forms
3. Store settings management (branding, social links, delivery areas)
4. Real-time updates to JSON data files

### Data Persistence
- Products stored in `data/products.json`
- Settings stored in `data/settings.json`
- File-based storage with JSON encoding for Arabic text support

## External Dependencies

### Frontend Dependencies
- **Bootstrap 5 RTL**: UI framework with right-to-left language support
- **Font Awesome**: Icon library for enhanced UI elements
- **Google Fonts (Cairo)**: Arabic-optimized typography
- **Unsplash**: External image hosting for product photos

### Backend Dependencies
- **Flask**: Web framework for Python
- **Python Standard Library**: JSON, logging, os modules for core functionality

### Third-party Integrations
- **WhatsApp Business**: Customer communication through wa.me links
- **Social Media**: Configurable links to Facebook, Telegram platforms

## Deployment Strategy

### Development Setup
- Flask development server on port 5000
- Debug mode enabled for development
- Environment variable support for session secrets

### Data Management
- JSON files created automatically if missing
- UTF-8 encoding for proper Arabic text handling
- Directory structure created automatically for data files

### Security Considerations
- Session-based authentication for admin access
- Secret key configuration through environment variables
- Input validation and error handling for data operations

### Scalability Notes
- Current file-based storage suitable for small to medium catalogs
- Easy migration path to database solutions (JSON structure compatible)
- Modular design allows for future API integrations and payment processing