from __future__ import annotations

import ast
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Symbol:
    name: str
    kind: str
    line: int


class CodeAnalyzer:
    def analyze(self, path: str | Path) -> list[Symbol]:
        file_path = Path(path)
        if file_path.suffix in {".py"}:
            return self._analyze_python(file_path)
        if file_path.suffix in {".ts", ".tsx", ".js", ".jsx"}:
            return self._analyze_typescript(file_path)
        return []

    def _analyze_python(self, path: Path) -> list[Symbol]:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)
        symbols: list[Symbol] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                symbols.append(Symbol(name=node.name, kind="function", line=node.lineno))
            elif isinstance(node, ast.ClassDef):
                symbols.append(Symbol(name=node.name, kind="class", line=node.lineno))
        return symbols

    def _analyze_typescript(self, path: Path) -> list[Symbol]:
        source = path.read_text(encoding="utf-8")
        symbols: list[Symbol] = []
        function_pattern = re.compile(r"function\s+(\w+)")
        class_pattern = re.compile(r"class\s+(\w+)")
        interface_pattern = re.compile(r"interface\s+(\w+)")
        for index, line in enumerate(source.splitlines(), start=1):
            for match in function_pattern.finditer(line):
                symbols.append(Symbol(name=match.group(1), kind="function", line=index))
            for match in class_pattern.finditer(line):
                symbols.append(Symbol(name=match.group(1), kind="class", line=index))
            for match in interface_pattern.finditer(line):
                symbols.append(Symbol(name=match.group(1), kind="interface", line=index))
        return symbols
