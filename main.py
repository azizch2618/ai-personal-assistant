import os

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI


# FLASK APP

app = Flask(__name__)


# LOAD ENVIRONMENT VARIABLES

load_dotenv()

api_key = os.getenv("OPEN_API_KEY")

if not api_key:
    raise ValueError(
        "OPEN_API_KEY was not found. "
        "Check your .env file."
    )


# OPENAI CLIENT

client = OpenAI(api_key=api_key)


# HOME PAGE


@app.route("/")
def hello_world():
    return render_template("index.html")



# ASK ANYTHING


@app.route("/ask", methods=["POST"])
def ask():

    try:

        question = request.form.get("question")

        if not question:
            return jsonify({
                "error": "Please enter a question."
            }), 400

        response = client.responses.create(
            model="gpt-5-nano",
            input=[
                {
                    "role": "system",
                    "content": "Act like a helpful personal assistant."
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            max_output_tokens=3000
        )

        answer = response.output_text.strip()

        return jsonify({
            "response": answer
        }), 200

    except Exception as e:

        print("ASK ERROR:", e)

        return jsonify({
            "error": str(e)
        }), 500


# SUMMARIZE EMAIL


@app.route("/summarize", methods=["POST"])
def summarize():

    try:

        email_text = request.form.get("email")

        if not email_text:
            return jsonify({
                "error": "Please enter an email to summarize."
            }), 400

        prompt = (
            "Summarize the following email in 2-3 sentences:\n\n"
            f"{email_text}"
        )

        response = client.responses.create(
            model="gpt-5-nano",
            input=[
                {
                    "role": "system",
                    "content": "Act like an expert email assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_output_tokens=2000
        )

        summary = response.output_text.strip()

        return jsonify({
            "response": summary
        }), 200

    except Exception as e:

        print("SUMMARIZE ERROR:", e)

        return jsonify({
            "error": str(e)
        }), 500



# RUN FLASK


if __name__ == "__main__":
    app.run(debug=True)