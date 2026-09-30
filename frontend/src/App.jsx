import { useState } from "react";

import Header from "./components/Header";
import Chat from "./components/Chat";
import InputBox from "./components/InputBox";

import {
  indexCode,
  askCode,
  debugCode,
  analyzeCode,
} from "./services/api";

function App() {
  const [messages, setMessages] = useState([]);
  const [question, setQuestion] = useState("");

  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);

  const [mode, setMode] = useState("ask");

  const getErrorMessage = (error) => {
    if (error.response?.data?.detail) {
      return error.response.data.detail;
    }

    if (error.code === "ERR_NETWORK") {
      return "Cannot connect to CodeSense backend. Make sure the FastAPI server is running.";
    }

    return "Something went wrong. Please try again.";
  };

  const handleFileSelect = async (event) => {
    const file = event.target.files[0];

    if (!file) return;

    setUploading(true);

    try {
      /*
       * Analyze mode does not index the file.
       * It directly sends the file to the AST analyzer.
       */
      if (mode === "analyze") {
        const result = await analyzeCode(file);

        setMessages((previous) => [
          ...previous,
          {
            role: "assistant",
            content: result,
            type: "analysis",
          },
        ]);
      } else {
        /*
         * Ask and Debug both require the code
         * to be indexed in FAISS first.
         */
        const result = await indexCode(file);

        setMessages((previous) => [
          ...previous,
          {
            role: "assistant",
            content: `✓ ${result.filename} indexed successfully.`,
            type: "text",
          },
        ]);
      }
    } catch (error) {
      console.error("FILE PROCESSING ERROR:", error);

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: getErrorMessage(error),
          type: "error",
        },
      ]);
    } finally {
      setUploading(false);

      // Allows the same file to be selected again.
      event.target.value = "";
    }
  };

  const handleSubmit = async () => {
    /*
     * Analyze works through file upload,
     * so the Ask/Debug submit button should
     * not make an API request in Analyze mode.
     */
    if (mode === "analyze") {
      return;
    }

    if (!question.trim() || loading) {
      return;
    }

    const userQuestion = question.trim();

    // Add user's message immediately.
    setMessages((previous) => [
      ...previous,
      {
        role: "user",
        content: userQuestion,
        type: "text",
      },
    ]);

    setQuestion("");
    setLoading(true);

    try {
      if (mode === "ask") {
        const result = await askCode(userQuestion);

        setMessages((previous) => [
          ...previous,
          {
            role: "assistant",
            content: result.answer,
            sources: result.sources || [],
            type: "text",
          },
        ]);
      } else if (mode === "debug") {
        const result = await debugCode(userQuestion);

        setMessages((previous) => [
          ...previous,
          {
            role: "assistant",
            content: result.answer,
            sources: result.sources || [],
            type: "debug",
          },
        ]);
      }
    } catch (error) {
      console.error("REQUEST ERROR:", error);

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: getErrorMessage(error),
          type: "error",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="h-screen flex flex-col bg-white">
      <Header />

      <Chat
        messages={messages}
        loading={loading}
      />

      <InputBox
        question={question}
        setQuestion={setQuestion}
        onSubmit={handleSubmit}
        onFileSelect={handleFileSelect}
        loading={loading}
        uploading={uploading}
        mode={mode}
        setMode={setMode}
      />
    </div>
  );
}

export default App;