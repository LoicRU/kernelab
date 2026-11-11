#!/usr/bin/env python3
"""Point d'entrée du linter kernelab : vérifie taille et style du code."""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lintlib.config import load_config
from lintlib.runner import run


def main():
    """Lit les options, lance l'analyse et affiche le résultat."""
    here = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(description="Linter kernelab")
    parser.add_argument("--root", default=os.path.join(here, ".."),
                         help="racine du projet à analyser")
    parser.add_argument("--conf", default=os.path.join(here, "lint.conf"),
                         help="fichier de configuration")
    args = parser.parse_args()

    config = load_config(args.conf)
    issues, nb_files = run(os.path.abspath(args.root), config)

    for issue in issues:
        print(issue.format())

    status = "OK" if not issues else f"{len(issues)} erreur(s)"
    print(f"lint : {nb_files} fichier(s) analysé(s), {status}")
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
