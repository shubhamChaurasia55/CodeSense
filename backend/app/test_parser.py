from app.services.parser import parse_python_code


code = """
import jwt


class UserService:

    def login(self, username, password):
        return authenticate(username, password)

    def logout(self, user_id):
        return delete_session(user_id)


def calculate_average(numbers):
    return sum(numbers) / len(numbers)
"""


chunks = parse_python_code(
    code,
    "user_service.py"
)


for chunk in chunks:
    print(
        chunk["type"],
        "|",
        chunk["name"],
        "|",
        chunk.get("class_name"),
        "|",
        chunk["start_line"],
        "-",
        chunk["end_line"]
    )