import os

import openai
from flask import Flask, redirect, render_template, request, url_for
from gpt_index import GPTKeywordTableIndex, GPTSimpleVectorIndex, SimpleDirectoryReader


app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    print(request.data)
    logs = "test"
    if request.method == "POST":
        question = request.form["animal"]
        documents = SimpleDirectoryReader('data').load_data()
        index = GPTSimpleVectorIndex(documents)
        index.save_to_disk('index.json')
        print(question)
        response = index.query(generate_prompt(question))
        print(response)
        # index = GPTSimpleVectorIndex.load_from_disk("index.json")

        # response = openai.Completion.create(
        #     model="text-davinci-003",
        #     prompt=generate_prompt(question),
        #     temperature=0.6,
        #     max_tokens=2048,
        # )

        return redirect(url_for("index", result=response))

    result = request.args.get("result")
    return render_template("index.html", result=result, logs=logs)


def generate_prompt(question):
    return question + "日本語で応えて下さい。また、読み込んだファイルに書いてあることから応えてください。"
    