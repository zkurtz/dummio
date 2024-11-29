from datetime import datetime, timezone
from pathlib import Path
from uuid import UUID, uuid4

from pydantic import BaseModel

import dummio.pydantic


# make a pydantic model equivalent to the dataclass above
class Data(BaseModel):
    id: UUID
    documentation: str
    config: dict
    rmse: float
    trained_at: datetime


def test_pydantic_io(tmp_path: Path) -> None:
    data = Data(
        id=uuid4(),
        documentation="This is a test data instance.",
        config={"n_estimators": 100, "learning_rate": 0.01},
        rmse=0.1,
        trained_at=datetime.now(timezone.utc),
    )
    filepath = tmp_path / "data.json"
    dummio.pydantic.save(data, filepath=filepath)
    loaded_data = dummio.pydantic.load(filepath=filepath, model=Data)
    assert data == loaded_data
