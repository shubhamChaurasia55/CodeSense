function Source({ source }) {
  return (
    <div className="border border-gray-200 rounded-xl px-3 py-2 bg-white">

      <div className="text-sm font-medium text-gray-900">
        {source.filename}
      </div>

      <div className="text-xs text-gray-500 mt-1">
        {source.type}

        {source.name && (
          <> · {source.name}</>
        )}
      </div>

      <div className="text-xs text-gray-400 mt-1">
        Lines {source.start_line}–{source.end_line}
      </div>

    </div>
  );
}

export default Source;