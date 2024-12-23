
from flask import Blueprint, request, jsonify
from app.services.rag_model import rag_chain

api = Blueprint('api', __name__)

@api.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    try:
        response = rag_chain.invoke(user_input)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
