import settings
from flask import Flask
from views import router
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "secret key"
app.register_blueprint(router)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=settings.API_DEBUG)
