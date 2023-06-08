import logging
from flask import Blueprint, request, abort
from middleware import model_predict

router = Blueprint("app_router", __name__)

router.register_error_handler


@router.route("/")
def index():
    return "hello world"


@router.route("/api/ask_model", methods=["POST"])
def ask_model():
    """
    This function is used to get the response from the agent model
    """
    try:
        messages = request.json["messages"]
        user = request.json["user"]

        ## Validation to get the last 8 messages to the conversation
        if len(messages) > 8:
            messages = messages[-8:]
        response = model_predict(messages, user)
        return {"user": user, "content": response}
    except Exception as e:
        error_message = str(e)
        logging.error(error_message)
        abort(500, description=error_message)
