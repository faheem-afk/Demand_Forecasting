from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    file_path: Path
    artifact_path: Path
    

