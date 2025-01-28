from datetime import datetime
from pathlib import Path
from uuid import UUID

from pydantic import BaseModel

import dummio.pydantic


class Data(BaseModel):
    id: UUID
    documentation: str
    config: dict
    rmse: float
    trained_at: datetime


def test_pydantic_io(tmp_path: Path) -> None:
    _ = dummio.pydantic.example(filepath=tmp_path / "data.json")
