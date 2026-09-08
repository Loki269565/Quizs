#!/usr/bin/env python3
"""
Scans the data/ directory (up to 2 levels: category, and category/subfolder)
and writes data/manifest.json describing every test file found.

The site (index.html) fetches this manifest.json as a plain static file
instead of calling the GitHub API, so there is no rate limit and no
"403 / entries.filter is not a function" errors for visitors.
"""
import json
import os

DATA_DIR = "data"
OUTPUT_PATH = os.path.join(DATA_DIR, "manifest.json")


def is_json_file(name):
    return name.endswith(".json") and name != "manifest.json"


def list_json_files(dir_path):
    if not os.path.isdir(dir_path):
        return []
    return sorted(f for f in os.listdir(dir_path) if is_json_file(f) and os.path.isfile(os.path.join(dir_path, f)))


def main():
    manifest = {"uncategorized": [], "categories": []}

    if not os.path.isdir(DATA_DIR):
        write_manifest(manifest)
        return

    top_entries = sorted(os.listdir(DATA_DIR))

    # Files sitting directly in data/ (not in any category folder)
    manifest["uncategorized"] = list_json_files(DATA_DIR)

    for name in top_entries:
        cat_path = os.path.join(DATA_DIR, name)
        if not os.path.isdir(cat_path):
            continue

        category = {
            "name": name,
            "files": list_json_files(cat_path),
            "subfolders": [],
        }

        for sub_name in sorted(os.listdir(cat_path)):
            sub_path = os.path.join(cat_path, sub_name)
            if not os.path.isdir(sub_path):
                continue
            category["subfolders"].append({
                "name": sub_name,
                "files": list_json_files(sub_path),
            })

        manifest["categories"].append(category)

    write_manifest(manifest)


def write_manifest(manifest):
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
