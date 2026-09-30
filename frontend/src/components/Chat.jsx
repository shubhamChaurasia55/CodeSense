import { useEffect, useRef } from "react";

import Message from "./Message";
import LoadingMessage from "./LoadingMessage";

function Chat({ messages, loading }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  return (
    <main className="flex-1 overflow-y-auto">
      <div className="max-w-3xl mx-auto px-4 py-8 space-y-6">

        {messages.length === 0 && !loading ? (
          <div className="flex items-center justify-center min-h-[60vh]">
            <div className="text-center">

              <h2 className="text-3xl font-semibold">
                Ask your code anything
              </h2>

              <p className="mt-3 text-gray-500">
                Upload Python code and ask questions,
                debug problems, or analyze your code.
              </p>

            </div>
          </div>
        ) : (
          <>
            {messages.map((message, index) => (
              <Message
                key={index}
                role={message.role}
                content={message.content}
                sources={message.sources}
                type={message.type}
              />
            ))}

            {loading && <LoadingMessage />}

            <div ref={bottomRef} />
          </>
        )}

      </div>
    </main>
  );
}

export default Chat;