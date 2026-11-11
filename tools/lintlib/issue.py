"""Représente une erreur de lint détectée dans un fichier."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Issue:
    """Une erreur de lint : fichier, ligne, règle et message."""

    path: str
    line: int
    rule: str
    msg: str

    def format(self) -> str:
        """Formate l'erreur au format chemin:ligne: [règle] message."""
        return f"{self.path}:{self.line}: [{self.rule}] {self.msg}"
