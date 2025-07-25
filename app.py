from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__, template_folder='templates')

# ✅ Replace with your actual Gemini API key
GOOGLE_API_KEY = "AIzaSyBi-u0kJEwnDK8IIwq8IDL7QeziRycSkbY"

# ✅ Configure Gemini with the API key
genai.configure(api_key=GOOGLE_API_KEY)

# ✅ Choose a supported model
model = genai.GenerativeModel("gemini-1.5-flash")  # You can also use "gemini-1.0-pro" or "gemini-1.5-pro"

# Function to get a response from Gemini
def get_gemini_reply(message):
    try:
        response = model.generate_content(message)
        return response.text.strip()
    except Exception as e:
        return f"⚠️ Gemini Error: {str(e)}"

# Route for the chat interface
@app.route('/')
def index():
    return render_template('index.html')  # Load the chatbot UI

# Endpoint to handle chat requests
@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json.get('message')
    if not user_msg:
        return jsonify({"reply": "⚠️ No message received"}), 400

    bot_reply = get_gemini_reply(user_msg)
    return jsonify({"reply": bot_reply})

# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
