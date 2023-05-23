
from flask import (
    Blueprint,
    request,
    abort,
    jsonify
)
import openai
from settings import(
    OPEN_AI_KEY
)
from middleware import model_predict

router = Blueprint("app_router", __name__)

router.register_error_handler

openai.api_key = OPEN_AI_KEY

@router.route("/")
def index():
    return "hello world"


@router.route('/api/ask_gpt3', methods=['POST'])
def ask_gpt3():
    try:
        messages = request.json["messages"]
        user = request.json["user"]
        response = model_predict(messages, user)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return {
            "user": response["user"],
            "content": response["content"]
        }
    except Exception as e:
        error_message = str(e)
        abort(500, description=error_message)

    




