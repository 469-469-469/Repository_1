from pathlib import Path
from datetime import datetime, timezone
from typing import Optional


class Tools:

    """Класс для ."""

    _project_dir: Optional[Path] = None

    @staticmethod
    def project_dir(_project_dir=None) -> Path:
        if _project_dir is None:
            _project_dir = Path(__file__).resolve().parents[1]
        return _project_dir

    @staticmethod
    def files_dir(nested_directory: Optional[str] = None, filename: Optional[str] = None) -> Path:
        """
        Возвращает путь к директории `files` (или её поддиректории).
        Если директория не существует, она создается.
        Если указан `filename`, возвращает полный путь к файлу.
        """
        files_path = Tools.project_dir() / "files"

        if nested_directory:
            files_path = files_path / nested_directory

        files_path.mkdir(parents=True, exist_ok=True)

        if filename:
            return files_path / filename

        return files_path

    @staticmethod
    def get_timestamp() -> str:
        """
        Возвращает текущую временную метку в формате YYYY-MM-DD_HH-MM-SS.
        """
        return datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S_UTC")