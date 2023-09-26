import React, { useState, useEffect } from "react";

function useTypewriter(text = '') {
    if (typeof text !== 'string') {
      console.error('Invalid text:', text);
      return;
    }
    const [displayedText, setDisplayedText] = useState("");

    useEffect(() => {
      let index = 0;
      let currentText = "";
      const intervalId = setInterval(() => {
        currentText += text.charAt(index);
        setDisplayedText(currentText);
        index += 1;
        if (index === text.length) {
          clearInterval(intervalId);
        }
      }, 30);

      return () => clearInterval(intervalId);
    }, [text]);

    return displayedText;
  }

function App() {
  const [file, setFile] = useState(null);
  const [fileUploaded, setFileUploaded] = useState(false);
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleLuckyClick = () => {
    const options = [
      "What is the current date and time?",
      "Can you summarize this document?",
      "What is the overall sentiment of this document?",
    ];
    const randomQuestion = options[Math.floor(Math.random() * options.length)];
    setQuestion(randomQuestion);
  };

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setFileUploaded(true);
  };

  const handleQuestionChange = (e) => {
    setQuestion(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    const formData = new FormData();
    formData.append('pdf_data', file);
    formData.append('question', question);

    try {
      const res = await fetch("/test_query", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        throw new Error("Network response was not ok");
      }

      const data = await res.json();
      setResponse(data);
    } catch (error) {
      setError("An error occurred. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const displayedResponse = useTypewriter(response ? response.flask_response.answer : "");

  return (
    <div>
      <h1>Ask Your Document</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label
            className={`custom-file-upload ${fileUploaded ? "file-uploaded" : ""}`}>
            {fileUploaded ? "PDF uploaded! Choose another file?" : "Choose File"}
            <input type="file" id="file-upload" onChange={handleFileChange} />
          </label>
        </div>
        <div>
          <textarea
            className="question-textarea"
            value={question}
            onChange={handleQuestionChange}
            placeholder="Your question..."
          />
        </div>
        <div className="button-container">
          {/* Disable the button if no file is uploaded */}
          <button type="submit" className="button-submit" disabled={!fileUploaded}>
            {loading ? "Asking..." : "Submit"}
          </button>
          <button type="button" onClick={handleLuckyClick}>I'm feeling lucky</button>
        </div>
      </form>
      {response && <div>Response: {displayedResponse}</div>}
    </div>
  );

  }

export default App;
