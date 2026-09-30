function ErrorMessage({ message }) {
  return (
    <div className="flex justify-start">

      <div className="max-w-3xl bg-red-50 border border-red-200 rounded-2xl px-4 py-3">

        <p className="text-sm text-red-700">
          {message}
        </p>

      </div>

    </div>
  );
}

export default ErrorMessage;