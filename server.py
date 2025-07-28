from flask import Flask, request, jsonify
import google.generativeai as genai
import os

# Flask app initialization
app = Flask(__name__)

# Gemini API key from environment variables
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Default route to check if server is running
@app.route('/')
def home():
    return "✅ Student Question Solver API is Live!"

# Main API route to solve questions
@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json()
        question = data.get("question")

        if not question:
            return jsonify({"error": "❌ Question is missing!"}), 400

        # Generate answer using Gemini Pro model
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(question)

        return jsonify({"answer": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Local testing (won’t be used on Render)
if __name__ == "__main__":
    app.run(debug=True)
