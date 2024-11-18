Automated Web Search and Information Extraction Tool
Project Description
This project provides a seamless way to automate the retrieval and extraction of specific information from web searches and structured data files. It combines the power of web APIs and language models to:

Upload and preview CSV files containing data.
Perform automated web searches for entities using customizable prompts.
Extract targeted information (e.g., emails, addresses) from search results using OpenAI's API.
View extracted data in a dashboard and download it as a CSV file for further use.
Optional features include error handling, rate-limiting for API calls, and integration with Google Sheets for data synchronization.

Setup Instructions
1. Prerequisites
Python 3.8 or higher
API keys for OpenAI and a web search provider (e.g., SerpAPI or ScraperAPI)
Flask framework and related libraries (install instructions below)
2. Installation Steps
Clone the repository:

bash
Copy code
git clone https://github.com/khushikpatel/project.git
cd project-name
Set up a virtual environment (optional):

bash
Copy code
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Set up environment variables: Create a .env file in the project directory and include the following:

makefile
Copy code
OPENAI_API_KEY=your_openai_api_key
SEARCH_API_KEY=your_search_api_key
SEARCH_ENGINE_ID=your_search_engine_id (if applicable)
Run the application:

bash
Copy code
python app.py
Access the dashboard:
Open your browser and navigate to http://127.0.0.1:5000.

Usage Guide
1. Upload CSV Files
On the homepage, use the file upload feature to select and upload a CSV file.
The application will display a preview of the column names and sample rows.
2. Perform Web Searches
Set up a custom prompt template, such as "Find the email address of {entity}".
Select the main column or entities for which to perform searches.
The app will automatically fetch relevant web results using the provided search API key.
3. Extract and View Information
The app uses OpenAI's API to extract targeted information (e.g., emails, phone numbers) from search results.
Extracted data is displayed in a structured table on the dashboard.
4. Download Data
Use the "Download" button to export the extracted data as a CSV file.
Optionally, you can configure the app to update a connected Google Sheet.
API Keys and Environment Variables
Required API Keys
OpenAI API Key:

Obtain from the OpenAI Platform.
Add to .env as OPENAI_API_KEY.
Search API Key:

Get from your preferred search API provider (e.g., SerpAPI or ScraperAPI).
Add to .env as SEARCH_API_KEY.
Search Engine ID (if applicable):

Required for some APIs like Google Custom Search.
Add to .env as SEARCH_ENGINE_ID.
Optional Features
Google Sheets Integration: Synchronize extracted data directly with a Google Sheet.
Error Handling: Includes retry mechanisms for failed requests and user-friendly error messages.
Rate-Limiting Management: Prevents exceeding API call limits by managing request rates.
