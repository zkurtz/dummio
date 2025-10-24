"""Performance comparison between Parquet and Vortex formats for pandas DataFrames.

This demo creates a ~300MB DataFrame and compares the IO cycle round trip time
for .parquet vs .vortex formats.

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
from pathlib import Path

import numpy as np
import pandas as pd

from dummio.pandas import df_parquet, df_vortex


def create_large_dataframe(target_size_mb: float = 300) -> pd.DataFrame:
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
    df: pd.DataFrame, filepath: Path, save_func: callable, load_func: callable, format_name: str
) -> dict[str, float]:
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
    loaded_df = load_func(filepath)
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
    print("Parquet vs Vortex Performance Comparison")
    print("=" * 60)

    # Create test data
    df = create_large_dataframe(target_size_mb=300)

    # Create temporary directory for test files
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)

        # Benchmark Parquet
        parquet_results = benchmark_format(
            df, tmpdir_path / "test.parquet", df_parquet.save, df_parquet.load, "Parquet"
        )

        # Benchmark Vortex
        vortex_results = benchmark_format(df, tmpdir_path / "test.vortex", df_vortex.save, df_vortex.load, "Vortex")

    # Print comparison summary
    print(f"\n{'=' * 60}")
    print("SUMMARY")
    print(f"{'=' * 60}")
    print(f"\n{'Metric':<25} {'Parquet':<15} {'Vortex':<15} {'Winner':<10}")
    print("-" * 65)

    metrics = [
        ("Save time (s)", "save_time"),
        ("Load time (s)", "load_time"),
        ("Round-trip time (s)", "round_trip_time"),
        ("File size (MB)", "file_size_mb"),
    ]

    for metric_name, metric_key in metrics:
        parquet_val = parquet_results[metric_key]
        vortex_val = vortex_results[metric_key]

        # Determine winner (lower is better)
        if parquet_val < vortex_val:
            winner = "Parquet"
            speedup = vortex_val / parquet_val
        else:
            winner = "Vortex"
            speedup = parquet_val / vortex_val

        print(f"{metric_name:<25} {parquet_val:<15.3f} {vortex_val:<15.3f} {winner:<10} ({speedup:.2f}x)")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
