"""Performance comparison between different file formats for pandas DataFrames.

This demo creates a ~500MB DataFrame and compares the IO cycle round trip time
for different formats supported by dummio: .csv, .parquet, .feather, and .vortex.

Run this script from the repo root:
    python demo/vortex_vs_parquet.py

Example results (2025-10-24 on a macbook):

Metric                    Parquet         Vortex          Winner
-----------------------------------------------------------------
Save time (s)             2.315           1.731           Vortex     (1.34x)
Load time (s)             1.599           0.458           Vortex     (3.49x)
Round-trip time (s)       3.914           2.189           Vortex     (1.79x)
File size (MB)            296.845         296.380         Vortex     (1.00x)
"""

import tempfile
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from dummio.pandas import df_csv, df_parquet

# Try to import optional formats
try:
    from dummio.pandas import df_feather

    HAS_FEATHER = True
except ImportError:
    HAS_FEATHER = False

try:
    from dummio.pandas import df_vortex

    HAS_VORTEX = True
except ImportError:
    HAS_VORTEX = False


def create_large_dataframe(target_size_mb: float = 500) -> pd.DataFrame:
    """Create a DataFrame of approximately the target size in MB.

    Args:
        target_size_mb: Target size in megabytes (default: 300)

    Returns:
        A pandas DataFrame of approximately the target size
    """
    # Estimate rows needed
    # Each row has: int64 (8 bytes) + float64 (8 bytes) + 10-char string (~10 bytes) ≈ 26 bytes
    # Plus overhead, let's estimate 30 bytes per row
    rows_needed = int((target_size_mb * 1024 * 1024) / 30)

    print(f"Creating DataFrame with {rows_needed:,} rows...")
    np.random.seed(42)

    data = {
        "id": np.arange(rows_needed),
        "value1": np.random.randn(rows_needed),
        "value2": np.random.randn(rows_needed),
        "value3": np.random.randn(rows_needed),
        "category": np.random.choice(["A", "B", "C", "D", "E"], rows_needed),
        "text": [f"text_{i % 1000}" for i in range(rows_needed)],
        "flag": np.random.choice([True, False], rows_needed),
    }

    df = pd.DataFrame(data)

    # Calculate actual memory usage
    memory_mb = df.memory_usage(deep=True).sum() / (1024 * 1024)
    print(f"DataFrame created: {len(df):,} rows, {memory_mb:.2f} MB in memory")

    return df


def benchmark_format(
    df: pd.DataFrame,
    filepath: Path,
    save_func: Callable[..., None],
    load_func: Callable[..., pd.DataFrame],
    format_name: str,
) -> dict[str, Any]:
    """Benchmark save and load operations for a given format.

    Args:
        df: DataFrame to save and load
        filepath: Path to save the file
        save_func: Function to save the DataFrame
        load_func: Function to load the DataFrame
        format_name: Name of the format for display

    Returns:
        Dictionary with timing results
    """
    print(f"\n{'=' * 60}")
    print(f"Testing {format_name} format")
    print(f"{'=' * 60}")

    # Save
    print(f"Saving to {filepath}...")
    start_time = time.time()
    save_func(df, filepath=filepath)
    save_time = time.time() - start_time
    file_size_mb = filepath.stat().st_size / (1024 * 1024)
    print(f"  Save time: {save_time:.3f} seconds")
    print(f"  File size: {file_size_mb:.2f} MB")

    # Load
    print(f"Loading from {filepath}...")
    start_time = time.time()
    loaded_df = load_func(filepath=filepath)
    load_time = time.time() - start_time
    print(f"  Load time: {load_time:.3f} seconds")

    # Verify
    if not df.equals(loaded_df):
        # For float columns, check if they're close enough
        print("  Warning: DataFrames not exactly equal, checking numeric columns...")
        for col in df.select_dtypes(include=[np.number]).columns:
            if not np.allclose(df[col].fillna(0), loaded_df[col].fillna(0), rtol=1e-10):
                print(f"    Column '{col}' differs!")
        for col in df.select_dtypes(exclude=[np.number]).columns:
            if not df[col].equals(loaded_df[col]):
                print(f"    Column '{col}' differs!")
    else:
        print("  ✓ Data integrity verified")

    # Cleanup
    filepath.unlink()

    return {
        "format": format_name,
        "save_time": save_time,
        "load_time": load_time,
        "round_trip_time": save_time + load_time,
        "file_size_mb": file_size_mb,
    }


def main() -> None:
    """Run the benchmark comparison."""
    print("DataFrame IO Format Performance Comparison")
    print("=" * 60)

    # Create test data
    df = create_large_dataframe(target_size_mb=500)

    # Create temporary directory for test files
    results = []
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)

        # Benchmark CSV
        results.append(benchmark_format(df, tmpdir_path / "test.csv", df_csv.save, df_csv.load, "CSV"))

        # Benchmark Parquet
        results.append(benchmark_format(df, tmpdir_path / "test.parquet", df_parquet.save, df_parquet.load, "Parquet"))

        # Benchmark Feather (if available)
        if HAS_FEATHER:
            results.append(
                benchmark_format(
                    df,
                    tmpdir_path / "test.feather",
                    df_feather.save,
                    df_feather.load,
                    "Feather",  # type: ignore[possibly-undefined]
                )
            )
        else:
            print("\n⚠ Feather format skipped (pyarrow not available)")

        # Benchmark Vortex (if available)
        if HAS_VORTEX:
            results.append(
                benchmark_format(
                    df,
                    tmpdir_path / "test.vortex",
                    df_vortex.save,
                    df_vortex.load,
                    "Vortex",  # type: ignore[possibly-undefined]
                )
            )
        else:
            print("\n⚠ Vortex format skipped (vortex-data not available)")

    # Print comparison summary
    print(f"\n{'=' * 80}")
    print("SUMMARY")
    print(f"{'=' * 80}")

    # Print header
    format_names = [r["format"] for r in results]
    header = f"\n{'Metric':<25}"
    for name in format_names:
        header += f" {name:<15}"
    header += " Winner"
    print(header)
    print("-" * 80)

    metrics = [
        ("Save time (s)", "save_time"),
        ("Load time (s)", "load_time"),
        ("Round-trip time (s)", "round_trip_time"),
        ("File size (MB)", "file_size_mb"),
    ]

    for metric_name, metric_key in metrics:
        line = f"{metric_name:<25}"
        values = [r[metric_key] for r in results]

        # Find winner (lowest value)
        min_val = min(values)
        winner_idx = values.index(min_val)
        winner_name = format_names[winner_idx]

        # Print all values
        for val in values:
            line += f" {val:<15.3f}"

        # Add winner and speedup
        max_val = max(values)
        speedup = max_val / min_val if min_val > 0 else 1.0
        line += f" {winner_name} ({speedup:.2f}x)"

        print(line)

    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
