from flask import Flask, request, jsonify, abort, current_app
from PyPDF2 import PdfReader
from io import BytesIO
import base64
import logging
from datetime import datetime
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object('configmodule.ProductionConfig')
CORS(app, resources={r"/*": {"origins": "*"}})

logging.basicConfig(level=logging.INFO)

@app.errorhandler(400)
def bad_request_error(error):
    return jsonify({"error": "Bad Request", "message": str(error)}), 400

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal Server Error", "message": "An error occurred. Try again later."}), 500

def initialize_app(pdf_data):
    # Read data from the pdf_data and put them into a variable called raw_text
    reader = PdfReader(pdf_data)
    raw_text = ''
    for page in reader.pages:
        text = page.extract_text()
        if text:
            raw_text += text

    # Split the text into smaller chunks
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    texts = text_splitter.split_text(raw_text)

    embedding = OpenAIEmbeddings()
    docsearch = FAISS.from_texts(texts, embedding)

    # Use the current date and time in the prompt template
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    prompt_template = f"""The current date and time is {current_datetime}. Always remember the current date and time and use it to perform date calculations.  Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

    {{context}}

    Question: {{question}}
    Answer in a professional tone:"""

    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )
    chain = load_qa_chain(OpenAI(temperature=0), chain_type="stuff", prompt=PROMPT)

    return chain, docsearch

@app.route('/test_query', methods=['POST'])
def test_query():
    try:
        json_data = request.get_json(silent=True)

        if not json_data:
            abort(400, "No JSON input received")

        try:
            pdf_data_base64 = json_data['pdf_data']
            question = json_data['question']
            pdf_data = base64.b64decode(pdf_data_base64)
            pdf_data_file = BytesIO(pdf_data)
            current_app.logger.info("Received base64 encoded input")
        except KeyError:
            abort(400, "Invalid JSON input")

        if not pdf_data_file or not question:
            abort(400, "Invalid input")

        current_app.logger.info("PDF successfully uploaded")
        chain, docsearch = initialize_app(pdf_data_file)
        docs = docsearch.similarity_search(question)
        result = chain.run(input_documents=docs, question=question)

        return jsonify({"question": question, "answer": result})

    except Exception as e:
        current_app.logger.error(f"An error occurred: {e}")
        abort(500)


if __name__ == "__main__":
    app.run(debug=True)