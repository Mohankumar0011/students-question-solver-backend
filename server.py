from flask import Flask, request, jsonify
import google.generativeai as genai
import os

# Flask app banate hain
app = Flask(__name__)

# API key set karo (Render/Replit me env variable se ayega)
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route("/")
def home():
    return "Server is live 🚀"

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        question = data.get("question")

        if not question:
            return jsonify({"error": "No question provided"}), 400

        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(question)

        return jsonify({"answer": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Development ke liye local run
if __name__ == "__main__":
    app.run(debug=True)
