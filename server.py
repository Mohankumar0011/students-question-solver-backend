# server.py
import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

# --- Flask ऐप सेटअप ---
app = Flask(__name__)
CORS(app)  # यह आपके ऐप और सर्वर को बात करने की अनुमति देता है

# --- API की कॉन्फ़िगरेशन ---
# यह API की यहाँ सुरक्षित है। यह यूज़र को कभी नहीं दिखेगी।
API_KEY = os.environ.get("GEMINI_API_KEY") 
genai.configure(api_key=API_KEY)

# --- AI मॉडल का आरंभीकरण ---
model_text = genai.GenerativeModel('gemini-1.5-flash')
model_vision = genai.GenerativeModel('gemini-pro-vision') # Vision मॉडल फोटो के लिए

# --- राउट 1: टेक्स्ट-आधारित AI हेल्पर ---
@app.route('/ask-ai', methods=['POST'])
def ask_ai_route():
    try:
        data = request.json
        prompt = data.get('prompt')
        if not prompt:
            return jsonify({'error': 'No prompt provided'}), 400
            
        response = model_text.generate_content(prompt)
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- राउट 2: इमेज-आधारित Scan & Solve ---
@app.route('/solve-with-image', methods=['POST'])
def solve_with_image_route():
    try:
        data = request.json
        image_data = data.get('image') # Base64 इमेज डेटा
        prompt_text = data.get('prompt', "इस फोटो में क्या सवाल है? इसे विस्तार से हल करें और समझाएं।")
        
        if not image_data:
            return jsonify({'error': 'No image data provided'}), 400

        image_parts = [{
            "mime_type": "image/jpeg",
            "data": image_data
        }]
        
        response = model_vision.generate_content([prompt_text, image_parts[0]])
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- सर्वर चलाने के लिए ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)