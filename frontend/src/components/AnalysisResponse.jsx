function AnalysisResponse({ data }) {
  if (!data) {
    return (
      <div className="max-w-3xl bg-red-50 border border-red-200 rounded-2xl px-5 py-4">
        <p className="text-sm text-red-700">
          No analysis result received.
        </p>
      </div>
    );
  }

  return (
    <div className="max-w-3xl bg-gray-100 rounded-2xl px-5 py-4">

      <div className="flex items-center justify-between mb-5">

        <div>
          <h3 className="font-semibold text-gray-900">
            Code Quality Analysis
          </h3>

          <p className="text-xs text-gray-500 mt-1">
            {data.filename}
          </p>
        </div>

        <div className="text-sm text-gray-500">
          {data.function_count} functions
        </div>

      </div>

      <div className="space-y-3">

        {data.functions.map((func, index) => (
          <div
            key={index}
            className="bg-white border border-gray-200 rounded-xl p-4"
          >

            <div className="flex items-center justify-between">

              <h4 className="font-medium text-gray-900">
                {func.name}()
              </h4>

              <span className="text-xs text-gray-500">
                Lines {func.start_line}–{func.end_line}
              </span>

            </div>

            <div className="flex gap-6 mt-3 text-sm">

              <div>
                <span className="text-gray-400">
                  Lines
                </span>

                <p className="font-medium text-gray-800">
                  {func.lines}
                </p>
              </div>

              <div>
                <span className="text-gray-400">
                  Complexity
                </span>

                <p className="font-medium text-gray-800">
                  {func.complexity}
                </p>
              </div>

            </div>

          </div>
        ))}

      </div>

      {data.functions.length === 0 && (
        <p className="text-sm text-gray-500">
          No functions were found in this file.
        </p>
      )}

    </div>
  );
}

export default AnalysisResponse;