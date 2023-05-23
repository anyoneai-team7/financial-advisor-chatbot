
from flask import (
    Blueprint,
    request,
    abort,
    jsonify
)
import openai
from settings import(
    OPEN_AI_KEY,
    AI_MAX_TOKENS,
    AI_TEMP
)

router = Blueprint("app_router", __name__)

router.register_error_handler

openai.api_key = OPEN_AI_KEY

@router.route("/")
def index():
    return "hello world"


@router.route('/api/ask_gpt3', methods=['POST'])
def ask_gpt3():
    try:
        print(OPEN_AI_KEY)
        messages = request.json["messages"]
        user = request.json["user"]
        print(messages)
        print(user)
        responseChatGpt = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages= messages,
            temperature = float(AI_TEMP),
            max_tokens = int(AI_MAX_TOKENS),
            user = user
            
        )

        
        response = jsonify(responseChatGpt.choices[0].message) # CITISCM
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    except Exception as e:
        error_message = str(e)
        abort(500, description=error_message)

    




