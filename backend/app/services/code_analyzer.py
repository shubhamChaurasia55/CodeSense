import ast


def analyze_python_code(code: str):
    tree = ast.parse(code)

    results = []

    for node in ast.walk(tree):

        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue

        complexity = 1

        for child in ast.walk(node):

            if isinstance(
                child,
                (
                    ast.If,
                    ast.For,
                    ast.While,
                    ast.Try,
                    ast.ExceptHandler,
                    ast.With,
                    ast.AsyncWith,
                    ast.IfExp,
                )
            ):
                complexity += 1

            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1

        results.append({
            "name": node.name,
            "start_line": node.lineno,
            "end_line": node.end_lineno,
            "lines": node.end_lineno - node.lineno + 1,
            "complexity": complexity,
        })

    return results