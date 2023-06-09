import logging
from uuid import uuid4
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
        job_id = str(uuid4())

        ## Validation to get the last 8 messages to the conversation
        if len(messages) > 8:
            messages = messages[-8:]
        response = model_predict(messages, job_id)
        return {"content": response}
    except Exception as e:
        error_message = str(e)
        logging.error(error_message)
        abort(500, description=error_message)
