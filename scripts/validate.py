#!/usr/bin/env python3
"""KnowFlow Nexus Schema Validator

Usage:
    python3 scripts/validate.py registry/data-sources.json
    python3 scripts/validate.py registry/parser-recipes.json
    python3 scripts/validate.py registry/meta-parameters.json

Returns exit code 0 if valid, 1 if invalid.
"""
import json
import sys
import os
from pathlib import Path

SCHEMA_MAP = {
    "data-sources.json": "../schema/data-source.schema.json",
    "parser-recipes.json": "../schema/parser-recipe.schema.json",
    "meta-parameters.json": "../schema/meta-parameter.schema.json",
}

def validate(data_file: str) -> bool:
    """Validate a data file against its schema using basic structural checks."""
    data_path = Path(data_file)
    if not data_path.exists():
        print(f"❌ File not found: {data_file}")
        return False

    try:
        with open(data_path, encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in {data_file}: {e}")
        return False

    if not isinstance(data, list):
        print(f"❌ {data_file}: Root element must be an array (list of records)")
        return False

    if len(data) == 0:
        print(f"⚠️  {data_file}: Array is empty (no records)")
        return True

    # Basic structural validation
    all_valid = True
    for i, record in enumerate(data):
        record_num = i + 1
        if not isinstance(record, dict):
            print(f"❌ Record #{record_num}: Must be a JSON object")
            all_valid = False
            continue

        # Check required fields (varies by file type)
        filename = os.path.basename(data_file)
        if filename == "data-sources.json":
            required = ["id", "name", "url", "type", "accessibility", "method", "domains"]
        elif filename == "parser-recipes.json":
            required = ["id", "name", "source_type", "parser_language", "extraction_rules", "output_schema"]
        elif filename == "meta-parameters.json":
            required = ["id", "name", "pattern", "description", "example_domains"]
        else:
            required = ["id", "name"]

        for field in required:
            if field not in record:
                print(f"❌ Record #{record_num} ({record.get('name', 'unknown')}): Missing required field '{field}'")
                all_valid = False

        # Validate accessibility for data sources
        if "accessibility" in record and isinstance(record["accessibility"], dict):
            acc = record["accessibility"]
            if "status" not in acc:
                print(f"❌ Record #{record_num}: accessibility must have 'status' field")
                all_valid = False
            elif acc["status"] not in ["verified-working", "verified-broken", "needs-test", "partial"]:
                print(f"⚠️  Record #{record_num}: accessibility.status '{acc['status']}' is non-standard")

            if "last_verified" not in acc:
                print(f"⚠️  Record #{record_num}: Missing accessibility.last_verified")
            if "verified_by" not in acc:
                print(f"⚠️  Record #{record_num}: Missing accessibility.verified_by")

    if all_valid:
        print(f"✅ {data_file}: {len(data)} records, all valid")
    return all_valid


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/validate.py <data-file>")
        sys.exit(1)

    script_dir = Path(__file__).parent
    all_ok = True

    for data_file in sys.argv[1:]:
        # Resolve relative paths
        if not Path(data_file).is_absolute():
            data_file = str((script_dir / ".." / data_file).resolve())
        if not validate(data_file):
            all_ok = False

    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
