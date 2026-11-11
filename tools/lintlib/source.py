"""Utilitaires pour parcourir et lire les fichiers sources."""

import os


def discover_files(root, extensions, exclude_dirs):
    """Liste les fichiers sous root dont l'extension est dans extensions."""
    found = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in exclude_dirs]
        for name in filenames:
            if os.path.splitext(name)[1] in extensions:
                found.append(os.path.join(dirpath, name))
    return sorted(found)


def read_lines(path):
    """Lit un fichier et retourne ses lignes sans le terminateur de fin."""
    with open(path, "r", encoding="utf-8", errors="replace") as handle:
        return handle.read().splitlines()


def read_text(path):
    """Lit le contenu complet d'un fichier en texte brut."""
    with open(path, "r", encoding="utf-8", errors="replace") as handle:
        return handle.read()


def relpath(path, root):
    """Retourne le chemin relatif à root, avec des séparateurs '/'."""
    return os.path.relpath(path, root).replace(os.sep, "/")
