from flask import Blueprint, jsonify, request, current_app
from services.ai_service import ask_ai

def register_routes(bp: Blueprint):
    @bp.route("/status", methods=["GET"])
    def status() -> None:
        return jsonify({"status": "API is running"}), 200

    @bp.route("/test", methods=["GET"])
    def test() -> None:
        return "<h1>API blueprint is working!</h1>"

    @bp.route("/ask", methods=["POST"])
    def ask() -> None:
        try:
            data = request.get_json()
            if not data or "question" not in data:
                return jsonify({"error": "Question is required"}), 400

            question = data["question"]
            response = ask_ai(question)
            return jsonify({"question": question, "response": response})
        except Exception as e:
            current_app.logger.error(f"Error processing request: {e}")
            return jsonify({"error": "Invalid request"}), 400