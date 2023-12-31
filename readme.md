# PDFRAILSESBUILD & LANGCHAIN_ASKPDF

## Project Description

This project combines the power of Artificial Intelligence, Rails, and Flask to provide an intuitive way to extract information from PDF documents. Users can upload a PDF file and ask a question related to the content of the PDF. The system utilizes a state-of-the-art machine learning model to read the PDF and answer the question in real-time.

![Screenshot](/RAILS_ESBUILD/app/assets/images/Screenshot.png)


## Technologies Used

- **Python**: 3.9.12
- **Rails**: 7.0.8
- **React**: 18.2.0

## Dependencies

- **Flask**: 2.1.0
- **langchain**
- **faiss-cpu**:1.7.4
- **tiktoken**:0.5.1
- **httparty**: Ruby Gem

## Installation & Setup

### Cloning the Repository

First, clone the repository to your local machine by opening up a new terminal window:

```
git clone https://github.com/colin-thornburg/React-Rails-Langchain.git
```

### Setting Up OpenAI API Key

1. Navigate to the Flask application folder:
    ```
    cd React-Rails-Langchain/flask_ai

    ```


2. You need to set up an OpenAI API key for the Flask application to function correctly.  Visit [OpenAI](https://platform.openai.com/account/api-keys)
3. Add an environment variable `OPENAI_API_KEY` with your OpenAI API key.
    - On Mac/Linux: `export OPENAI_API_KEY=your-api-key-here`
    - On Windows: `set OPENAI_API_KEY=your-api-key-here`


### Setting Up the Flask App (flask_ai)

1. Navigate to the Flask application folder (if you aren't already there):

    ```
    cd flask_ai
    ```

2. Create a virtual environment:

    ```
    python3 -m venv venv
    ```

3. Activate the virtual environment:

    - **Mac/Linux**:

        ```
        source venv/bin/activate
        ```

    - **Windows**:

        ```
        .\\venv\\Scripts\\activate
        ```

4. Install the required packages:

    ```
    pip install -r requirements.txt
    ```

5. Start the Flask app:

    ```
    python flask_app.py
    ```

### Setting Up the Rails App (RAILS_ESBUILD)

1. Open a new terminal and navigate to the Rails application folder:

    ```
    cd React-Rails-Langchain/RAILS_ESBUILD
    ```

2. Install the Ruby Gem dependencies:

    ```
    bundle install
    ```

3. Start the Rails app:

    ```
    bin/dev
    ```

For more information on using React with ESBuild and Rails, you can watch this [YouTube tutorial](https://youtu.be/yoLJXjEV2nM?si=2dqvMXGe2-ElU4US).


## How to Use

1. Open the web application.
2. Upload a PDF document using the "Choose File" button.
3. Enter your question in the text area.
4. Click "Submit" to get your answer.
