"""Règles de lint applicables à tous les fichiers texte."""

import os
import re

from .issue import Issue

_TODO_RE = re.compile(r"TODO(\([A-Za-z0-9_]+\))?")
_NAME_RE = re.compile(r"^[a-z][a-z0-9_]*$")
_COMMENT_MARKERS = ("//", "#", ";")


def check_file_length(path, lines, config):
    """Vérifie que le fichier ne dépasse pas max_file_lines lignes."""
    if len(lines) > config.max_file_lines:
        return [Issue(path, len(lines), "file-length",
                       f"fichier de {len(lines)} lignes (max {config.max_file_lines})")]
    return []


def check_line_length(path, lines, config):
    """Vérifie qu'aucune ligne ne dépasse max_line_length caractères."""
    issues = []
    for num, line in enumerate(lines, start=1):
        if len(line) > config.max_line_length:
            issues.append(Issue(path, num, "line-length",
                                 f"ligne de {len(line)} caractères "
                                 f"(max {config.max_line_length})"))
    return issues


def check_trailing_ws(path, lines):
    """Vérifie l'absence d'espaces en fin de ligne."""
    issues = []
    for num, line in enumerate(lines, start=1):
        if line != line.rstrip():
            issues.append(Issue(path, num, "trailing-ws", "espaces en fin de ligne"))
    return issues


def check_todo_tag(path, lines):
    """Vérifie que les marqueurs todo, dans les commentaires, sont étiquetés."""
    issues = []
    for num, line in enumerate(lines, start=1):
        comment = _comment_part(line)
        if comment is None:
            continue
        for match in _TODO_RE.finditer(comment):
            if not match.group(1):
                issues.append(Issue(path, num, "todo-tag",
                                     "TODO non étiqueté, attendu TODO(nom)"))
    return issues


def _comment_part(line):
    """Retourne la partie commentaire d'une ligne, ou None si absente."""
    indices = [line.find(marker) for marker in _COMMENT_MARKERS if marker in line]
    if not indices:
        return None
    return line[min(indices):]


def check_file_name(path):
    """Vérifie que le nom de fichier est en snake_case."""
    base = os.path.splitext(os.path.basename(path))[0]
    if base == "__init__":
        return []
    if not _NAME_RE.match(base):
        return [Issue(path, 1, "file-name", f"nom de fichier non snake_case : {base}")]
    return []
