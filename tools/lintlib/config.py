"""Chargement de la configuration du linter (tools/lint.conf)."""

from dataclasses import dataclass, field


@dataclass
class Config:
    """Paramètres du linter lus depuis le fichier de configuration."""

    max_file_lines: int = 200
    max_function_lines: int = 40
    max_public_functions: int = 8
    max_line_length: int = 100
    header_exempt: set = field(default_factory=lambda: {"kernel.c"})
    exclude_dirs: set = field(default_factory=lambda: {".git", "build", "__pycache__", "iso"})
    extensions: set = field(default_factory=lambda: {".c", ".h", ".asm", ".S", ".py", ".ld"})


_INT_KEYS = {"max_file_lines", "max_function_lines", "max_public_functions", "max_line_length"}
_LIST_KEYS = {"header_exempt", "exclude_dirs", "extensions"}


def load_config(path: str) -> Config:
    """Charge la configuration depuis un fichier clé = valeur."""
    config = Config()
    with open(path, "r", encoding="utf-8") as handle:
        for raw_line in handle:
            _apply_line(config, raw_line)
    return config


def _apply_line(config: Config, raw_line: str) -> None:
    """Applique une ligne de configuration (clé = valeur) à config."""
    line = raw_line.split("#", 1)[0].strip()
    if not line or "=" not in line:
        return
    key, value = (part.strip() for part in line.split("=", 1))
    if key in _INT_KEYS:
        setattr(config, key, int(value))
    elif key in _LIST_KEYS:
        setattr(config, key, {item.strip() for item in value.split(",") if item.strip()})
