from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import openai
import os
import io
import requests
import time

app = Flask(__name__)

# OpenAI setup
openai.api_key = os.getenv('OPENAI_API_KEY')
SERP_API_KEY = os.getenv('SERP_API_KEY')  # Replace with your SerpAPI key

# Home page to upload CSV
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle CSV upload and show column preview
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    data = pd.read_csv(file)
    columns = data.columns.tolist()
    preview = data.head().to_dict()
    return jsonify({"columns": columns, "preview": preview})

# Route to set prompt template
@app.route('/set-prompt', methods=['POST'])
def set_prompt():
    prompt_template = request.json.get("prompt")
    main_column = request.json.get("main_column")
    entities = request.json.get("entities")
    return jsonify({"message": "Prompt set", "entities": entities})

# Perform web search for each entity
def perform_web_search(entity, prompt_template):
    query = prompt_template.format(entity=entity)
    search_url = "https://serpapi.com/search"
    params = {
        "q": query,
        "api_key": SERP_API_KEY,
    }

    response = requests.get(search_url, params=params)
    if response.status_code == 200:
        return response.json().get('organic_results', [])
    else:
        time.sleep(1)  # Handle rate limiting
        return []

# Extract specific information using OpenAI
def extract_information_with_llm(entity, prompt_template, web_results):
    formatted_results = "\n".join([result.get('snippet', '') for result in web_results])
    llm_prompt = f"{prompt_template.format(entity=entity)}\n\n{formatted_results}"
    try:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo",
            prompt=llm_prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error processing entity {entity}: {str(e)}"

# Route to perform search and extract info
@app.route('/search', methods=['POST'])
def search_and_extract():
    entities = request.json.get("entities")
    prompt_template = request.json.get("prompt")
    results = {}

    for entity in entities:
        web_results = perform_web_search(entity, prompt_template)
        extracted_info = extract_information_with_llm(entity, prompt_template, web_results)
        results[entity] = {
            "search_results": web_results,
            "extracted_info": extracted_info,
        }

    return jsonify(results)

# Route to download extracted data as CSV
@app.route('/download', methods=['POST'])
def download_csv():
    data = request.json.get("data")
    df = pd.DataFrame([
        {"Entity": entity, "Extracted Info": info['extracted_info']}
        for entity, info in data.items()
    ])
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)
    return send_file(io.BytesIO(output.read().encode()), as_attachment=True, download_name="extracted_data.csv")

# Route to display extracted data in a table format
@app.route('/display', methods=['POST'])
def display_data():
    data = request.json.get("data")
    return jsonify({"message": "Data ready for display", "data": data})

if __name__ == '__main__':
    app.run(debug=True)
