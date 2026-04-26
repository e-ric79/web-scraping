# Amazon Competitor Analysis Tool

A powerful web scraping and AI-driven competitive analysis tool for Amazon products. This application enables sellers and business analysts to extract product information, identify competitors, and generate actionable insights using advanced LLM analysis.

## Overview

The Amazon Competitor Analysis Tool automates the process of gathering competitive intelligence on Amazon marketplace. Using ScraperAPI for reliable web scraping and Langchain with Groq for intelligent analysis, it provides comprehensive market positioning insights and competitor recommendations.

### Key Capabilities

- **Product Data Extraction**: Scrape detailed Amazon product information by ASIN (Amazon Standard Identification Number)
- **Multi-Regional Support**: Analyze products across different Amazon domains (com, co.uk, co.ke, etc.) and geolocation contexts
- **Competitor Discovery**: Automatically identify and catalog competing products based on categories and search terms
- **AI-Powered Analysis**: Generate market positioning insights and competitive recommendations using LLM technology
- **Interactive Dashboard**: User-friendly Streamlit interface for browsing and analyzing products
- **Local Data Persistence**: Store scraped data in a local TinyDB database for offline access and historical tracking

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Features

### 🔍 Web Scraping

- **ScraperAPI Integration**: Reliable product data extraction with automatic parsing
- **Multi-Domain Support**: Compatible with multiple Amazon regional domains
- **Geolocation Awareness**: Scrape location-specific pricing and availability data
- **Error Handling**: Robust error management with detailed logging

### 🤖 AI Analysis

- **Intelligent Competitor Discovery**: LLM-powered competitor identification and categorization
- **Market Insights**: Automated analysis of pricing trends, positioning, and market opportunities
- **Recommendations**: Data-driven recommendations for competitive strategy
- **Structured Output**: Pydantic-based models for type-safe analysis results

### 💾 Data Management

- **TinyDB Storage**: Lightweight, file-based JSON database for local storage
- **Duplicate Prevention**: Intelligent duplicate detection and update logic
- **Data Relationships**: Support for parent-child product relationships (original vs. competitors)
- **Query Interface**: Simple yet powerful database query API

### 🎨 User Interface

- **Streamlit Dashboard**: Interactive web-based UI for product exploration
- **Pagination Support**: Browse large product collections efficiently
- **Product Cards**: Rich visualization with images, pricing, and key metrics
- **Real-time Analysis**: Launch competitor analysis directly from the UI

## Architecture

```
┌─────────────────────────────────────────────────┐
│         Streamlit UI (main.py)                  │
└────────┬────────────────────────────────────────┘
         │
    ┌────┴────────────────────────────────────────┐
    │                                             │
    ▼                                             ▼
┌──────────────────┐                    ┌──────────────────┐
│   Services       │                    │   Database       │
│  (services.py)   │◄──────────────────►│    (db.py)       │
└────────┬─────────┘                    └──────────────────┘
         │
    ┌────┴─────────────────────────────────────┐
    │                                           │
    ▼                                           ▼
┌──────────────────┐                  ┌──────────────────┐
│   ScraperAPI     │                  │   LLM Analysis   │
│   Client         │                  │   (llm.py)       │
│(scraperapi_...py)│                  │   Groq/LangChain │
└──────────────────┘                  └──────────────────┘
         │
         └────────────────┬───────────────────┘
                          ▼
                  ┌──────────────────┐
                  │   Amazon.com     │
                  │   (External API) │
                  └──────────────────┘
```

## Prerequisites

- **Python**: 3.8 or higher
- **pip**: Python package manager
- **API Keys**:
  - ScraperAPI key (free tier available at [scraperapi.com](https://www.scraperapi.com))
  - Optional: Groq API key for LLM features (get at [groq.com](https://groq.com))
- **Internet Connection**: Required for API calls and web scraping

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/web-scraping.git
cd web-scraping
```

### 2. Create a Virtual Environment (Recommended)

```bash
# Using venv
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root directory:

```env
# ScraperAPI Configuration
SCRAPERAPI_KEY=your_scraperapi_key_here

# LLM Configuration (Groq)
GROQ_API_KEY=your_groq_api_key_here

# Optional: Database Path
DATABASE_PATH=data.json
```

**Note**: Never commit `.env` files to version control. The project includes a `.gitignore` entry to prevent this.

## Configuration

### ScraperAPI Setup

1. Visit [scraperapi.com](https://www.scraperapi.com)
2. Create a free account or sign in
3. Navigate to your dashboard and copy your API key
4. Add the key to your `.env` file as `SCRAPERAPI_KEY`

### Groq LLM Setup (Optional)

1. Visit [groq.com](https://groq.com)
2. Create an account and generate an API key
3. Add the key to your `.env` file as `GROQ_API_KEY`

### Streamlit Configuration

For custom Streamlit settings, edit `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#FF9900"  # Amazon orange
```

## Usage

### Running the Application

```bash
streamlit run main.py
```

The application will open in your default browser at `http://localhost:8501`

### Basic Workflow

1. **Input Product Details**:
   - Enter an Amazon ASIN (e.g., B08N5WRWNW)
   - Provide a ZIP/Postal Code for geolocation
   - Select the Amazon domain (com, co.uk, co.ke, etc.)

2. **Scrape Product**:
   - Click "Scrape product..." button
   - Wait for the scraping to complete
   - Product data will be stored in the local database

3. **View Products**:
   - Browse all scraped products with pagination
   - View product images, prices, brands, and links
   - Each product card displays key information

4. **Analyze Competitors**:
   - Click "Start analyzing competitors" on any product card
   - The system will:
     - Find competitors in the same category
     - Scrape competitor data
     - Generate AI-powered insights
   - Review market positioning and recommendations

### Command-Line Usage

For programmatic access, import the service functions:

```python
from src.services import scrape_and_store_product, fetch_and_store_competitors
from src.llm import analyze_competitors

# Scrape a single product
product = scrape_and_store_product(asin="B08N5WRWNW", geo_location="83980", domain="com")

# Find and store competitors
competitors = fetch_and_store_competitors(
    parent_asin="B08N5WRWNW",
    domain="com",
    geo_location="83980",
    pages=2
)

# Analyze with LLM
insights = analyze_competitors("B08N5WRWNW")
```

## Project Structure

```
web-scraping/
├── main.py                      # Streamlit application entry point
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── LICENSE                      # MIT License
├── .env                        # Environment variables (not tracked)
├── data.json                   # Local TinyDB database (generated)
│
├── src/                        # Source code directory
│   ├── __init__.py
│   ├── db.py                  # Database abstraction layer (TinyDB)
│   ├── llm.py                 # LLM analysis and Groq integration
│   ├── scraperapi_Client.py   # ScraperAPI client and scraping logic
│   ├── services.py            # High-level business logic
│   └── test_api.py            # API testing utilities
│
├── tests/                      # Test suite directory
│   ├── __init__.py
│   ├── test_db.py             # Database tests
│   └── test_scraper.py        # Scraper tests
│
├── .streamlit/                # Streamlit configuration
│   └── config.toml
│
├── .github/                   # GitHub Actions and templates
├── .devcontainer/             # Development container configuration
└── .vscode/                   # VS Code settings
```

### Module Descriptions

| Module                   | Purpose                                                                 |
| ------------------------ | ----------------------------------------------------------------------- |
| **db.py**                | Database operations using TinyDB - handles CRUD operations for products |
| **scraperapi_Client.py** | ScraperAPI integration - scrapes Amazon product data with parsing       |
| **llm.py**               | Langchain + Groq integration - performs AI-powered analysis on products |
| **services.py**          | High-level service layer - orchestrates scraping and analysis workflows |
| **main.py**              | Streamlit UI - interactive dashboard for user interaction               |

## API Documentation

### Database (db.py)

```python
from src.db import Database

db = Database()

# Insert or update a product
db.insert_product(product_data)

# Retrieve a single product by ASIN
product = db.get_product(asin="B08N5WRWNW")

# Get all products
all_products = db.get_all_products()

# Search products with filters
results = db.search_products(query_dict)
```

### ScraperAPI Client (scraperapi_Client.py)

```python
from src.scraperapi_Client import scrape_product_details, search_competitors

# Scrape a single product by ASIN
product = scrape_product_details(
    asin="B08N5WRWNW",
    geo_location="83980",
    domain="com"
)

# Search for competitors
competitors = search_competitors(
    query_title="Product Title",
    domain="com",
    categories=["Electronics"],
    pages=2,
    geo_location="83980"
)
```

### LLM Analysis (llm.py)

```python
from src.llm import analyze_competitors, CompetitorInsights, AnalysisOutput

# Analyze competitors for a product
insights: AnalysisOutput = analyze_competitors(parent_asin="B08N5WRWNW")

# Access analysis results
print(insights.summary)
print(insights.positioning)
print(insights.recommendations)
```

## Testing

The project includes a comprehensive test suite using pytest.

### Run All Tests

```bash
pytest
```

### Run Specific Test File

```bash
pytest tests/test_db.py
pytest tests/test_scraper.py
```

### Run with Coverage

```bash
pytest --cov=src tests/
```

### Run with Verbose Output

```bash
pytest -v
```

### Test Structure

- **test_db.py**: Tests for database operations, CRUD functions, and query logic
- **test_scraper.py**: Tests for ScraperAPI client and data extraction functions

## Troubleshooting

### Common Issues and Solutions

#### Issue: "SCRAPERAPI_KEY not found in .env file"

**Solution**: Ensure your `.env` file exists in the project root with the correct API key:

```env
SCRAPERAPI_KEY=your_key_here
```

#### Issue: ScraperAPI returns 403 Forbidden

**Solution**:

- Verify your API key is correct and active
- Check your ScraperAPI account quotas
- Ensure the ASIN/domain combination is valid

#### Issue: "No such table: products"

**Solution**: This is normal for first run. The database table is created automatically on first insert. Just run the application and scrape a product.

#### Issue: Streamlit page not responding

**Solution**:

- Clear Streamlit cache: Delete `.streamlit/` directory
- Restart the application: `streamlit run main.py`
- Check for API timeouts in logs

#### Issue: LLM analysis fails or returns empty results

**Solution**:

- Verify Groq API key is set and valid
- Ensure competitors have been scraped first
- Check network connectivity
- Review error logs for specific API errors

### Debug Mode

Enable verbose logging by adding to your `.env`:

```env
DEBUG=true
LOG_LEVEL=DEBUG
```

## Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m 'Add amazing feature'`
4. **Push** to the branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

### Code Standards

- Follow PEP 8 style guidelines
- Use type hints where possible
- Write tests for new functionality
- Keep docstrings updated
- Run linter: `flake8 src/ tests/`

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```

## Support and Contact

For issues, questions, or suggestions:

- **Open an Issue**: Use GitHub Issues for bug reports and feature requests
- **Email**: eric@example.com (replace with actual contact)
- **Documentation**: Check the inline code comments and docstrings

## Roadmap

Planned features and improvements:

- [ ] Multi-threaded scraping for faster data collection
- [ ] Advanced filtering and sorting options in UI
- [ ] Export functionality (CSV, PDF reports)
- [ ] Historical price tracking and trend analysis
- [ ] Machine learning-based competitor recommendations
- [ ] API endpoint for programmatic access
- [ ] Docker containerization for deployment
- [ ] Database migration to PostgreSQL for scalability

## Acknowledgments

- [ScraperAPI](https://www.scraperapi.com) - For reliable web scraping
- [Langchain](https://python.langchain.com) - For LLM integration
- [Groq](https://groq.com) - For fast LLM inference
- [Streamlit](https://streamlit.io) - For the interactive UI framework
- [TinyDB](https://tinydb.readthedocs.io) - For lightweight database solution

---
```
