from dotenv import load_dotenv
load_dotenv()
import os
import re
from flask import Flask, request, jsonify

app = Flask(__name__)

FULL_NAME = os.getenv("FULL_NAME", "john_doe")
DOB_DDMMYYYY = os.getenv("DOB", "17091999")
EMAIL = os.getenv("EMAIL", "john@xyz.com")
ROLL_NUMBER = os.getenv("ROLL_NUMBER", "ABCD123")

number_re = re.compile(r"^-?\d+$")

def is_integer_string(s: str) -> bool:
    return bool(number_re.match(s))

def is_alpha_string(s: str) -> bool:
    return s.isalpha()

def alternating_caps_from_reversed_charlist(chars):
    rev = list(reversed(chars))
    out_chars = []
    make_upper = True
    for ch in rev:
        if make_upper:
            out_chars.append(ch.upper())
        else:
            out_chars.append(ch.lower())
        make_upper = not make_upper
    return "".join(out_chars)

@app.route("/bfhl", methods=["POST"])
def bfhl():
    try:
        payload = request.get_json(force=True)
        if payload is None:
            return jsonify({"is_success": False, "error": "Invalid JSON"}), 400

        if "data" not in payload:
            return jsonify({"is_success": False, "error": "Missing 'data' key"}), 400

        raw = payload["data"]
        if not isinstance(raw, list):
            return jsonify({"is_success": False, "error": "'data' must be an array"}), 400

        tokens = [str(x) for x in raw]

        even_numbers = []
        odd_numbers = []
        alphabets = []
        special_characters = []
        sum_total = 0
        flattened_alpha_chars = []

        for tok in tokens:
            s = tok.strip()
            if s == "":
                special_characters.append(s)
                continue
            if is_integer_string(s):
                try:
                    n = int(s)
                except ValueError:
                    special_characters.append(s)
                    continue
                sum_total += n
                if n % 2 == 0:
                    even_numbers.append(s)
                else:
                    odd_numbers.append(s)
            elif is_alpha_string(s):
                alphabets.append(s.upper())
                for ch in s:
                    if ch.isalpha():
                        flattened_alpha_chars.append(ch)
            else:
                special_characters.append(s)
                for ch in s:
                    if ch.isalpha():
                        flattened_alpha_chars.append(ch)

        concat_string = alternating_caps_from_reversed_charlist(flattened_alpha_chars)

        response = {
            "is_success": True,
            "user_id": f"{FULL_NAME}_{DOB_DDMMYYYY}",
            "email": EMAIL,
            "roll_number": ROLL_NUMBER,
            "odd_numbers": odd_numbers,
            "even_numbers": even_numbers,
            "alphabets": alphabets,
            "special_characters": special_characters,
            "sum": str(sum_total),
            "concat_string": concat_string
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"is_success": False, "error": "Server error", "details": str(e)}), 500

if __name__ == "__main__":
    app.run()
