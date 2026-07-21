import json

from publish import publish_json_entries


def test_publish_json_entries_preserves_section_summaries(tmp_path):
    source_dir = tmp_path / "entries"
    source_dir.mkdir()
    entry = {
        "id": "sample-entry",
        "what_changed": "Agency repealed the rule.",
        "section_summaries": {
            "what_changed": "Agency repealed the rule outright.",
            "confidence_note": "High confidence, agency-sourced figures.",
        },
    }
    (source_dir / "sample-entry.json").write_text(json.dumps(entry))

    dest_file = tmp_path / "output" / "deregulation.json"
    included, excluded_count = publish_json_entries(source_dir, dest_file, excluded_ids=set())

    assert excluded_count == 0
    assert included[0]["section_summaries"] == entry["section_summaries"]

    published = json.loads(dest_file.read_text())
    assert published[0]["section_summaries"] == entry["section_summaries"]


def test_publish_json_entries_excludes_entries_without_touching_others(tmp_path):
    source_dir = tmp_path / "entries"
    source_dir.mkdir()
    kept = {"id": "kept-entry", "section_summaries": {"what_changed": "Kept."}}
    excluded = {"id": "excluded-entry", "section_summaries": {"what_changed": "Excluded."}}
    (source_dir / "kept-entry.json").write_text(json.dumps(kept))
    (source_dir / "excluded-entry.json").write_text(json.dumps(excluded))

    dest_file = tmp_path / "output" / "deregulation.json"
    included, excluded_count = publish_json_entries(
        source_dir, dest_file, excluded_ids={"excluded-entry"}
    )

    assert excluded_count == 1
    assert len(included) == 1
    assert included[0]["id"] == "kept-entry"
