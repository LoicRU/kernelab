"""Détection des définitions de fonctions C par comptage d'accolades."""

import re

_SIG_RE = re.compile(
    r"(?P<static>\bstatic\s+)?[A-Za-z_][\w\s\*]*?\b(?P<name>[A-Za-z_]\w*)\s*"
    r"\(([^;{}]*)\)\s*\{"
)


class Func:
    """Une fonction C détectée : nom, lignes de début/fin, visibilité."""

    def __init__(self, name, start_line, end_line, is_static):
        self.name = name
        self.start_line = start_line
        self.end_line = end_line
        self.is_static = is_static


def find_functions(stripped_text):
    """Trouve les fonctions définies au niveau 0 dans un texte C nettoyé."""
    funcs = []
    pos = 0
    while True:
        match = _SIG_RE.search(stripped_text, pos)
        if not match:
            break
        open_idx = match.end() - 1
        end_idx = _match_brace(stripped_text, open_idx)
        if end_idx is None:
            break
        funcs.append(
            Func(
                name=match.group("name"),
                start_line=stripped_text.count("\n", 0, match.start()) + 1,
                end_line=stripped_text.count("\n", 0, end_idx) + 1,
                is_static=bool(match.group("static")),
            )
        )
        pos = end_idx + 1
    return funcs


def _match_brace(text, open_idx):
    """Retourne l'index de l'accolade fermante correspondant à open_idx."""
    depth = 1
    i = open_idx + 1
    n = len(text)
    while i < n and depth > 0:
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
        i += 1
    return i - 1 if depth == 0 else None
