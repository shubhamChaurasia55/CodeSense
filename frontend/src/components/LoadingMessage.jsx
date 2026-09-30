function LoadingMessage() {
  return (
    <div className="flex justify-start">

      <div className="bg-gray-100 rounded-2xl px-4 py-3">

        <div className="flex items-center gap-2">

          <span className="text-sm text-gray-500">
            CodeSense is thinking
          </span>

          <div className="flex gap-1">

            <span className="w-1.5 h-1.5 rounded-full bg-gray-400 animate-bounce" />

            <span className="w-1.5 h-1.5 rounded-full bg-gray-400 animate-bounce [animation-delay:150ms]" />

            <span className="w-1.5 h-1.5 rounded-full bg-gray-400 animate-bounce [animation-delay:300ms]" />

          </div>

        </div>

      </div>

    </div>
  );
}

export default LoadingMessage;