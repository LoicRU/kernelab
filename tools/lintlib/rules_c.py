"""Règles de lint spécifiques aux fichiers C (.c/.h)."""

import os
import re

from .cfuncs import find_functions
from .cstrip import strip_c
from .issue import Issue

_NAME_RE = re.compile(r"^[a-z_][a-z0-9_]*$")
_IFNDEF_RE = re.compile(r"#ifndef\s+(\w+)")
_DEFINE_RE = re.compile(r"#define\s+(\w+)")


def check_functions(path, text, config):
    """Vérifie la longueur des fonctions et leur nom (snake_case)."""
    issues = []
    for func in find_functions(strip_c(text)):
        length = func.end_line - func.start_line + 1
        if length > config.max_function_lines:
            issues.append(Issue(path, func.start_line, "function-length",
                                 f"fonction '{func.name}' de {length} lignes "
                                 f"(max {config.max_function_lines})"))
        if not _NAME_RE.match(func.name):
            issues.append(Issue(path, func.start_line, "function-name",
                                 f"fonction '{func.name}' non snake_case"))
    return issues


def check_public_functions(path, text, config):
    """Vérifie le nombre de fonctions publiques (non static) dans un .c."""
    if not path.endswith(".c"):
        return []
    public = [f for f in find_functions(strip_c(text)) if not f.is_static]
    if len(public) > config.max_public_functions:
        return [Issue(path, 1, "public-functions",
                       f"{len(public)} fonctions publiques "
                       f"(max {config.max_public_functions})")]
    return []


def check_header_guard(path, text):
    """Vérifie la présence d'un garde #ifndef/#define/#endif dans un .h."""
    if not path.endswith(".h"):
        return []
    ifndef = _IFNDEF_RE.search(text)
    define = _DEFINE_RE.search(text)
    ok = ifndef and define and ifndef.group(1) == define.group(1) and "#endif" in text
    if not ok:
        return [Issue(path, 1, "header-guard",
                       "garde #ifndef/#define/#endif manquant ou incorrect")]
    return []


def check_header_pair(path, rel, config):
    """Vérifie qu'un .c a un .h du même nom (sauf exemptions)."""
    base = os.path.basename(path)
    if not base.endswith(".c") or base in config.header_exempt:
        return []
    header = path[:-len(".c")] + ".h"
    if not os.path.exists(header):
        return [Issue(rel, 1, "header-pair", f"pas de {os.path.basename(header)} associé")]
    return []
