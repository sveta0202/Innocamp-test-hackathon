from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

@app.get("/")
def index():
    return render_template("register.html")

@app.post("/collect-registration")
def collect_registration():
    data = request.get_json(silent=True)
    registration = data.get("registration", {})
    email = registration.get("email", "")
    password = registration.get("password", "")

    normalized = {
        "event": "user_registration",
        "user": {
            "first_name": registration["first_name"],
            "last_name": registration["last_name"],
            "email": email.lower(),
            "role": registration.get("role", "user").lower()
        },
        "meta": data.get("source", {})
    }
    microservice_response = microservice(normalized)
    return jsonify({
        "ok": True,
        "stage": "accepted",
        "normalized_payload": normalized,
        "microservice_response": microservice_response
    })

def microservice(payload: dict):
    return {
        "service": "auth-profile-service",
        "status": "queued",
        "message": "Регистрация принята и отправлена в микросервис",
        "payload_echo": payload
    }

if __name__ == "__main__":
    app.run(debug=True, port=5000)
