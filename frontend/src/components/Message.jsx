import ReactMarkdown from "react-markdown";

import Source from "./Source";
import DebugResponse from "./DebugResponse";
import AnalysisResponse from "./AnalysisResponse";
import ErrorMessage from "./ErrorMessage";

function Message({
  role,
  content,
  sources = [],
  type = "text",
}) {
  const isUser = role === "user";

  /*
   * Debug response
   */
  if (!isUser && type === "debug") {
    return (
      <DebugResponse
        answer={content}
        sources={sources}
      />
    );
  }

  /*
   * Static analysis response
   */
  if (!isUser && type === "analysis") {
    return (
      <AnalysisResponse
        data={content}
      />
    );
  }

  /*
   * Error response
   */
  if (!isUser && type === "error") {
    return (
      <ErrorMessage
        message={content}
      />
    );
  }

  /*
   * Normal user / Ask message
   */
  return (
    <div
      className={`flex w-full ${
        isUser
          ? "justify-end"
          : "justify-start"
      }`}
    >
      <div className="max-w-3xl">

        <div
          className={`px-4 py-3 rounded-2xl text-sm leading-6 ${
            isUser
              ? "bg-gray-900 text-white"
              : "bg-gray-100 text-gray-900"
          }`}
        >
          {isUser ? (
            <p className="whitespace-pre-wrap">
              {content}
            </p>
          ) : (
            <div className="ai-markdown">
              <ReactMarkdown>
                {content}
              </ReactMarkdown>
            </div>
          )}
        </div>

        {/* RAG sources */}
        {!isUser && sources.length > 0 && (
          <div className="mt-3">

            <p className="text-xs font-medium text-gray-500 mb-2">
              Sources
            </p>

            <div className="flex flex-wrap gap-2">
              {sources.map((source, index) => (
                <Source
                  key={index}
                  source={source}
                />
              ))}
            </div>

          </div>
        )}

      </div>
    </div>
  );
}

export default Message;