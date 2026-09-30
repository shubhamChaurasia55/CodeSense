function InputBox({
  question,
  setQuestion,
  onSubmit,
  onFileSelect,
  loading,
  uploading,
  mode,
  setMode,
}) {
  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();

      if (mode !== "analyze") {
        onSubmit();
      }
    }
  };

  const getPlaceholder = () => {
    if (mode === "ask") {
      return "Ask about your code...";
    }

    if (mode === "debug") {
      return "Describe the bug...";
    }

    return "Select a Python file to analyze...";
  };

  const getButtonText = () => {
    if (loading) {
      return "...";
    }

    if (mode === "ask") {
      return "Ask";
    }

    if (mode === "debug") {
      return "Debug";
    }

    return "Analyze via upload";
  };

  return (
    <div className="max-w-3xl mx-auto w-full px-4 pb-6">
      <div className="border border-gray-300 rounded-2xl p-2 shadow-sm">

        <textarea
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={getPlaceholder()}
          rows={1}
          disabled={uploading}
          className="w-full resize-none outline-none px-3 py-2 text-sm disabled:opacity-50"
        />

        <div className="flex items-center justify-between mt-2 px-1">

          <div className="flex items-center gap-2">

            {/* File upload */}
            <label
              className={`text-sm ${
                uploading
                  ? "text-gray-400 cursor-not-allowed"
                  : "text-gray-500 hover:text-gray-900 cursor-pointer"
              }`}
            >
              {uploading
                ? "Processing..."
                : mode === "analyze"
                  ? "📎 Analyze Python"
                  : "📎 Upload Python"}

              <input
                type="file"
                accept=".py"
                onChange={onFileSelect}
                disabled={uploading || loading}
                className="hidden"
              />
            </label>

            <div className="h-5 w-px bg-gray-200" />

            {/* Ask */}
            <button
              onClick={() => setMode("ask")}
              disabled={loading || uploading}
              className={`text-xs px-3 py-1.5 rounded-lg ${
                mode === "ask"
                  ? "bg-gray-900 text-white"
                  : "text-gray-500 hover:bg-gray-100"
              } disabled:opacity-40`}
            >
              Ask
            </button>

            {/* Debug */}
            <button
              onClick={() => setMode("debug")}
              disabled={loading || uploading}
              className={`text-xs px-3 py-1.5 rounded-lg ${
                mode === "debug"
                  ? "bg-gray-900 text-white"
                  : "text-gray-500 hover:bg-gray-100"
              } disabled:opacity-40`}
            >
              Debug
            </button>

            {/* Analyze */}
            <button
              onClick={() => setMode("analyze")}
              disabled={loading || uploading}
              className={`text-xs px-3 py-1.5 rounded-lg ${
                mode === "analyze"
                  ? "bg-gray-900 text-white"
                  : "text-gray-500 hover:bg-gray-100"
              } disabled:opacity-40`}
            >
              Analyze
            </button>

          </div>

          {/* Main action */}
          <button
            onClick={onSubmit}
            disabled={
              loading ||
              uploading ||
              mode === "analyze" ||
              !question.trim()
            }
            className="px-4 py-2 rounded-xl bg-gray-900 text-white text-sm disabled:opacity-40"
          >
            {getButtonText()}
          </button>

        </div>
      </div>
    </div>
  );
}

export default InputBox;