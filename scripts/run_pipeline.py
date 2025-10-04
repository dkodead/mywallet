#!/usr/bin/env python
"""Run the news pipeline on sample data and print the results as JSON.

This script is intended for demonstration and testing.  It loads the built‑in
sample articles, runs the full pipeline and outputs the top topics per
category.  You can run it with `python scripts/run_pipeline.py` from the
repository root.
"""

import json
import sys
from pathlib import Path

# Ensure the root of the repository (containing the `packages` directory) is
# on the Python path.  This allows the script to import `packages.news` when
# executed from the repository root without installing the package.  We add
# the parent directory of this file's parent (i.e. wallet_dkoded) to sys.path.
repo_root = Path(__file__).resolve().parents[1]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from packages.news.pipeline import run_pipeline


def main() -> None:
    results = run_pipeline(use_sample=True)
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
