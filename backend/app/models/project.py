from dataclasses import dataclass, field


@dataclass
class Project:
    name: str
    files: set[str] = field(default_factory=set)

    def add_file(self, filename: str):
        self.files.add(filename)