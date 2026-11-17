
from flask import Flask, request, jsonify
import logging
import sys
import os

from db import Database
from service import (
    NumberService,
    DuplicateNumberError,
    SequenceError,
    InvalidNumberError
)

app = Flask(__name__)

# Логирование только в stdout
logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format="%(asctime)s %(levelname)s %(message)s",
    force=True
)

logger = logging.getLogger(__name__)

db = Database(
    os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:12345@localhost:5432/number_system"
    )
)

service = NumberService(db)


@app.route("/process", methods=["POST"])
def process():

    data = request.get_json(silent=True)

    if not isinstance(data, dict) or "number" not in data:
        return jsonify({
            "error": "InvalidRequest"
        }), 400

    number = data["number"]

    try:
        result = service.process(number)

        return jsonify({
            "input": number,
            "result": result
        }), 200

    except InvalidNumberError as e:
        logger.error("Invalid number: %s", e)
        return jsonify({"error": str(e)}), 400

    except DuplicateNumberError as e:
        logger.error("EXCEPTION 1: %s", e)
        return jsonify({"error": str(e)}), 409

    except SequenceError as e:
        logger.error("EXCEPTION 2: %s", e)
        return jsonify({"error": str(e)}), 409

    except Exception:
        logger.exception("Internal server error")
        return jsonify({
            "error": "Internal Server Error"
        }), 500


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        threaded=True
    )
