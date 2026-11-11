"""Blanchit commentaires, chaînes et préprocesseur en gardant les lignes."""


def strip_c(text):
    """Remplace commentaires, chaînes et lignes de préprocesseur par des espaces.

    Les retours à la ligne sont conservés pour ne pas fausser les numéros
    de ligne calculés ensuite (détection de fonctions).
    """
    out = []
    i, n = 0, len(text)
    while i < n:
        two = text[i:i + 2]
        if two == "//":
            i = _skip_line_comment(text, i, out)
        elif two == "/*":
            i = _skip_block_comment(text, i, out)
        elif text[i] in "\"'":
            i = _skip_literal(text, i, out)
        else:
            out.append(text[i])
            i += 1
    return _strip_preprocessor("".join(out))


def _skip_line_comment(text, i, out):
    """Avance jusqu'à la fin de la ligne en remplaçant par des espaces."""
    n = len(text)
    while i < n and text[i] != "\n":
        out.append(" ")
        i += 1
    return i


def _skip_block_comment(text, i, out):
    """Avance jusqu'à la fin du commentaire /* ... */ en le blanchissant."""
    n = len(text)
    out.append("  ")
    i += 2
    while i < n and text[i:i + 2] != "*/":
        out.append("\n" if text[i] == "\n" else " ")
        i += 1
    out.append("  ")
    return i + 2


def _skip_literal(text, i, out):
    """Avance jusqu'à la fin d'une chaîne ou d'un caractère littéral."""
    n = len(text)
    quote = text[i]
    out.append(quote)
    i += 1
    while i < n and text[i] != quote:
        if text[i] == "\\" and i + 1 < n:
            out.append("  ")
            i += 2
            continue
        out.append("\n" if text[i] == "\n" else " ")
        i += 1
    if i < n:
        out.append(quote)
        i += 1
    return i


def _strip_preprocessor(text):
    """Remplace les lignes de préprocesseur (#define, #include...) par des espaces."""
    lines = text.split("\n")
    for idx, line in enumerate(lines):
        if line.lstrip().startswith("#"):
            lines[idx] = " " * len(line)
    return "\n".join(lines)
