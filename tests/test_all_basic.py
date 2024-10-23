"""Main tests of ezio."""

import ezio


def test_json(tmp_path):
    """Test the packio package."""
    data = {"a": 1, "b": 2}
    filepath = tmp_path / "data.json"
    ezio.json.save(data, filepath)
    loaded_data = ezio.json.load(filepath)
    assert data == loaded_data
