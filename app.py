from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__, template_folder='templates')  # Ensures HTML loads from templates/

# Your original function - unchanged
def get_gpt_reply(message):
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": "Bearer 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",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-3.5-turbo",
                "messages": [
                    {"role": "user", "content": message}
                ]
            }
        )
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')  # Loads upgraded UI

@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json.get('message')
    if not user_msg:
        return jsonify({"reply": "⚠️ No message received"}), 400

    bot_reply = get_gpt_reply(user_msg)
    return jsonify({"reply": bot_reply})  # Passes reply back to frontend

if __name__ == '__main__':
    app.run(debug=True)
