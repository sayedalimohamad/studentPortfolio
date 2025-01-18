from flask import Blueprint, jsonify, request, current_app
from models import db, Email, User  # Import necessary models
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

    # New Email API Endpoints
    @bp.route("/emails/send", methods=["POST"])
    def send_email():
        """
        Endpoint to send an email.
        Expects JSON payload with sender_email, recipient_email, subject, and message.
        """
        try:
            data = request.json
            sender_email = data.get("sender_email")
            recipient_email = data.get("recipient_email")
            subject = data.get("subject")
            message = data.get("message")

            if not (sender_email and recipient_email and subject and message):
                return jsonify({"error": "All fields (sender_email, recipient_email, subject, message) are required"}), 400

            sender = User.query.filter_by(email=sender_email).first()
            recipient = User.query.filter_by(email=recipient_email).first()

            if not sender or not recipient:
                return jsonify({"error": "Sender or recipient email address is invalid"}), 404

            # Create and save the email
            email = Email(
                sender_id=sender.user_id,  # Use sender_id instead of sender_email
                recipient_id=recipient.user_id,  # Use recipient_id instead of recipient_email
                subject=subject,
                message=message
            )
            db.session.add(email)
            db.session.commit()

            return jsonify({"message": "Email sent successfully!", "email": email.to_dict()}), 201
        except Exception as e:
            current_app.logger.error(f"Error sending email: {e}")
            return jsonify({"error": "Failed to send email"}), 500

    @bp.route("/emails/inbox/<email>", methods=["GET"])
    def inbox(email):
        """
        Endpoint to fetch the inbox of a specific email address.
        """
        try:
            # Fetch the user ID for the given email
            user = User.query.filter_by(email=email).first()
            if not user:
                return jsonify({"error": "User not found"}), 404

            # Fetch emails where the recipient_id matches the user's ID
            emails = Email.query.filter_by(recipient_id=user.user_id).order_by(Email.timestamp.desc()).all()
            return jsonify([email.to_dict() for email in emails]), 200
        except Exception as e:
            current_app.logger.error(f"Error fetching inbox for {email}: {e}")
            return jsonify({"error": "Failed to fetch inbox"}), 500

    @bp.route("/emails/sent/<email>", methods=["GET"])
    def sent_emails(email):
        """
        Endpoint to fetch sent emails of a specific email address.
        """
        try:
            # Fetch the user ID for the given email
            user = User.query.filter_by(email=email).first()
            if not user:
                return jsonify({"error": "User not found"}), 404

            # Fetch emails where the sender_id matches the user's ID
            emails = Email.query.filter_by(sender_id=user.user_id).order_by(Email.timestamp.desc()).all()
            return jsonify([email.to_dict() for email in emails]), 200
        except Exception as e:
            current_app.logger.error(f"Error fetching sent emails for {email}: {e}")
            return jsonify({"error": "Failed to fetch sent emails"}), 500