import ast


def parse_python_code(code: str):
    """
    Parse Python source code and extract top-level
    functions, classes, and imports.
    """

    tree = ast.parse(code)

    lines = code.splitlines()

    chunks = []

    for node in tree.body:

        # Function
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):

            start = node.lineno
            end = node.end_lineno

            source = "\n".join(lines[start - 1:end])

            chunks.append({
                "type": "function",
                "name": node.name,
                "start_line": start,
                "end_line": end,
                "code": source
            })

        # Class
        elif isinstance(node, ast.ClassDef):

            start = node.lineno
            end = node.end_lineno

            source = "\n".join(lines[start - 1:end])

            chunks.append({
                "type": "class",
                "name": node.name,
                "start_line": start,
                "end_line": end,
                "code": source
            })

        # Import
        elif isinstance(node, (ast.Import, ast.ImportFrom)):

            start = node.lineno
            end = node.end_lineno

            source = "\n".join(lines[start - 1:end])

            chunks.append({
                "type": "import",
                "name": None,
                "start_line": start,
                "end_line": end,
                "code": source
            })

    return chunks