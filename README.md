# Business Card OCR System

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/404-dev-notFound/VCard)

A production-level web application that extracts contact information from business card images using OCR (Optical Character Recognition) and generates vCard and CSV files.

## Features

- 🖼️ **Image Processing**: Supports multiple image formats (JPG, PNG, BMP, TIFF, WebP)
- 🔍 **OCR Technology**: Uses Rapid OCR for accurate text extraction
- 🤖 **AI-Powered Parsing**: Leverages Google's Gemini-2.5-pro for intelligent data extraction
- 📱 **vCard and CSV Generation**: Creates standard vCard (.vcf) files for contact import and CSV files for database management.
- 🌐 **Web Interface**: User-friendly web application (JS/CSS/HTML)
- 📊 **REST API**: Full API for programmatic access 
- ✅ **Data Validation**: Robust input validation and error handling

## Architecture

The system consists of several modular services:

- **OCR Service**: Handles image preprocessing and text extraction using RapidOCR
- **Parser Service**: Uses Google Gemini-2.5-pro to extract structured data from raw OCR text  
- **vCard Service**: Generates standard vCard format from structured data
- **CSV Service**: Generates CSV format from a structured database
- **FastAPI Application**: Provides a web interface and REST API endpoints

## Installation

### Prerequisites

1. **Python 3.8+**
2. **Rapid OCR**:
- Ubuntu/Debian: `sudo apt-get install rapid-ocr`
- macOS: `brew install rapid-ocr`
- Windows: Download from [GitHub](https://github.com/RapidAI/RapidOCR)
3. **OpenAI API Key** (for structured data extraction)

### Setup

1. **Clone and install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Configure environment**:
Create a `.env` file with:
```env
GEMINI_API_KEY="YOUR API_KEY (FROM GOOGLE AI STUDIO)"
```

3. **Run the application**:
```bash
python main.py
```

The application will be available at `http://localhost:8000`

## Usage

### Web Interface

1. Navigate to `http://localhost:8000`
2. Upload a business card image
3. Click "Process Business Card"
4. View extracted information and download vCard and CSV files.

### API Usage

#### Process Business Card

```bash
curl -X POST "http://localhost:8000/process-card" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@business_card.jpg" \
     -F "include_vcard=true" \
     -F "include_raw_text=true"
```

#### Response Format

```json
{
  "success": true,
  "raw_text": "Dev Dahiya\nSoftware Engineer\n...",
  "structured_data": {
    "first_name": "Dev",
    "last_name": "Dahiya",
    "company_name": "ZincPlus",
    "position": "Software Engineer",
    "email": "dev@zp.com",
    "mobile": "+1234567890",
    "website": "https://zincplus.in"
  },
  "vcard": "BEGIN:VCARD\nVERSION:3.0\n...",
  "error_message": null
}
```

## Configuration

Key configuration options in `config.py`:

- `MAX_FILE_SIZE`: Maximum upload size (default: 10MB)
- `ALLOWED_EXTENSIONS`: Supported image formats
- `GOOGLE_MODEL`: Google model to use (default: gemini-2.5-pro)

## Data Models

### BusinessCardData

The system extracts the following fields:

- **Required**: `first_name`, `last_name`, `company_name`, `position`
- **Optional**: `middle_name`, `department`, `mobile`, `telephone`, `email`, `address`, `extension`, `website`, `notes`

### vCard Format

Generated vCards follow the vCard 3.0 standard and include:

- Contact information (name, company, title)
- Phone numbers (mobile, work, extension)
- Email and website
- Business address
- Additional notes

## Error Handling

The system includes comprehensive error handling:

- **File validation**: Size, format, and content checks
- **OCR failures**: Graceful handling of unreadable images
- **API errors**: Proper error responses with detailed messages
- **Data validation**: Pydantic models ensure data integrity

## Performance Optimisation

- **Image preprocessing**: Automatic resizing and format conversion
- **Efficient OCR**: Optimised RapidOCR configuration for business cards
- **Async operations**: FastAPI async support for better concurrency
- **Resource cleanup**: Automatic temporary file cleanup

## Deployment

### Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    rapid-ocr \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Production Considerations

1. **Environment Variables**: Use proper secret management
2. **File Storage**: Consider cloud storage for uploaded files
3. **Rate Limiting**: Implement API rate limiting
4. **Monitoring**: Add logging and monitoring
5. **Security**: Implement authentication if needed
6. **Load Balancing**: Use reverse proxy (nginx) for production

## API Documentation

Once running, visit `http://localhost:8000/docs` for interactive API documentation (Swagger UI).

## Troubleshooting

### Common Issues

1. **RapidOCR not found**:
   - Ensure Rapid is installed

2. **GOOGLE API errors**:
   - Verify API key is valid
   - Check API usage limits
   - Ensure sufficient credits

3. **Image processing errors**:
   - Check image format is supported
   - Verify the image is not corrupted
   - Ensure image contains readable text

4. **Poor OCR results**:
   - Try higher resolution images
   - Ensure good lighting and contrast
   - Avoid blurry or skewed images

## License

This project is licensed under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For issues and questions:
- Check the troubleshooting section
- Review API documentation
- Create an issue on GitHub
