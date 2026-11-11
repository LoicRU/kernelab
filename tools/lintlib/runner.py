"""Orchestration du linter : parcourt les fichiers et applique les règles."""

from . import rules_c, rules_text
from .source import discover_files, read_lines, read_text, relpath


def run(root, config):
    """Analyse tous les fichiers sous root et retourne (issues, nb_fichiers)."""
    paths = discover_files(root, config.extensions, config.exclude_dirs)
    issues = []
    for path in paths:
        issues.extend(_check_file(path, root, config))
    return issues, len(paths)


def _check_file(path, root, config):
    """Applique toutes les règles pertinentes à un fichier."""
    rel = relpath(path, root)
    lines = read_lines(path)
    issues = []
    issues += rules_text.check_file_length(rel, lines, config)
    issues += rules_text.check_line_length(rel, lines, config)
    issues += rules_text.check_trailing_ws(rel, lines)
    issues += rules_text.check_todo_tag(rel, lines)
    issues += rules_text.check_file_name(rel)
    if path.endswith((".c", ".h")):
        issues += _check_c_file(path, rel, config)
    return issues


def _check_c_file(path, rel, config):
    """Applique les règles spécifiques au C (fonctions, gardes, pairage)."""
    text = read_text(path)
    issues = []
    issues += rules_c.check_functions(rel, text, config)
    issues += rules_c.check_public_functions(rel, text, config)
    issues += rules_c.check_header_guard(rel, text)
    issues += rules_c.check_header_pair(path, rel, config)
    return issues
