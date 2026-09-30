import Source from "./Source";

function DebugResponse({
  answer,
  sources = [],
}) {
  return (
    <div className="max-w-3xl bg-gray-100 rounded-2xl px-5 py-4 space-y-5">

      {/* Problem */}
      <section>
        <h3 className="text-sm font-semibold text-gray-900">
          Problem
        </h3>

        <p className="mt-2 text-sm leading-6 text-gray-700 whitespace-pre-wrap">
          {answer.problem}
        </p>
      </section>

      {/* Why */}
      <section>
        <h3 className="text-sm font-semibold text-gray-900">
          Why
        </h3>

        <p className="mt-2 text-sm leading-6 text-gray-700 whitespace-pre-wrap">
          {answer.why}
        </p>
      </section>

      {/* Fix */}
      <section>
        <h3 className="text-sm font-semibold text-gray-900">
          Fix
        </h3>

        <pre className="mt-2 bg-gray-900 text-gray-100 rounded-xl p-4 text-sm overflow-x-auto">
          <code>
            {answer.fix}
          </code>
        </pre>
      </section>

      {/* Explanation */}
      <section>
        <h3 className="text-sm font-semibold text-gray-900">
          Explanation
        </h3>

        <p className="mt-2 text-sm leading-6 text-gray-700 whitespace-pre-wrap">
          {answer.explanation}
        </p>
      </section>

      {/* Sources */}
      {sources.length > 0 && (
        <section>
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
        </section>
      )}

    </div>
  );
}

export default DebugResponse;