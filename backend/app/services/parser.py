import ast


def parse_python_code(code: str, filename: str = "unknown.py"):
    """
    Parse Python source code and extract:
    - imports
    - top-level functions
    - classes
    - methods inside classes
    """

    tree = ast.parse(code)
    lines = code.splitlines()
    chunks = []

    for node in tree.body:
        # Imports
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            start = node.lineno
            end = node.end_lineno

            source = "\n".join(
                lines[start - 1:end]
            )

            chunks.append({
                "filename": filename,
                "type": "import",
                "name": None,
                "start_line": start,
                "end_line": end,
                "code": source
            })

        # Top-level functions
        elif isinstance(
            node,
            (ast.FunctionDef, ast.AsyncFunctionDef)
        ):
            start = node.lineno
            end = node.end_lineno

            source = "\n".join(
                lines[start - 1:end]
            )

            chunks.append({
                "filename": filename,
                "type": "function",
                "name": node.name,
                "class_name": None,
                "start_line": start,
                "end_line": end,
                "code": source
            })

        # Classes
        elif isinstance(node, ast.ClassDef):

            class_start = node.lineno
            class_end = node.end_lineno

            class_source = "\n".join(
                lines[class_start - 1:class_end]
            )

            chunks.append({
                "filename": filename,
                "type": "class",
                "name": node.name,
                "class_name": None,
                "start_line": class_start,
                "end_line": class_end,
                "code": class_source
            })

            # Methods inside class
            for child in node.body:

                if isinstance(
                    child,
                    (ast.FunctionDef, ast.AsyncFunctionDef)
                ):
                    start = child.lineno
                    end = child.end_lineno

                    source = "\n".join(
                        lines[start - 1:end]
                    )

                    chunks.append({
                        "filename": filename,
                        "type": "method",
                        "name": child.name,
                        "class_name": node.name,
                        "start_line": start,
                        "end_line": end,
                        "code": source
                    })

    return chunks