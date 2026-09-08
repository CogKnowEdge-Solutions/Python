"""Tests for Lab 7 — File Handling (Text, JSON & CSV).

Covers:
- Plain text read/write with file modes 'w', 'r', 'a'
- JSON serialization with json.dump/json.load
- CSV with csv.reader and csv.DictReader
- CSV writing with csv.DictWriter
- Safe file modes and missing-file error handling
- Combined shop inventory export/reload pipeline

All tests use the pytest tmp_path fixture so no real files pollute the repo.
"""
import csv
import json
import os
import shutil
from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# Module-level helpers (matching the notebook's functions)
# ---------------------------------------------------------------------------

def write_text_file(path, content, mode="w", encoding="utf-8"):
    """Write text to a file. Mode defaults to 'w' (overwrite)."""
    with open(path, mode, encoding=encoding) as f:
        f.write(content)


def read_text_file(path, encoding="utf-8"):
    """Read full text from a file, raising FileNotFoundError if missing."""
    with open(path, "r", encoding=encoding) as f:
        return f.read()


def save_json_data(path, data, encoding="utf-8"):
    """Serialize data (list/dict) to a JSON file with utf-8 encoding."""
    with open(path, "w", encoding=encoding) as f:
        json.dump(data, f, indent=2)


def load_json_data(path, encoding="utf-8"):
    """Load and parse a JSON file, raising FileNotFoundError if missing."""
    with open(path, "r", encoding=encoding) as f:
        return json.load(f)


CSV_FIELDS = ["product", "qty", "price"]


def write_csv_orders(path, orders, fieldnames=CSV_FIELDS, encoding="utf-8"):
    """Write a header plus order rows using csv.DictWriter."""
    with open(path, "w", newline="", encoding=encoding) as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(orders)


def read_csv_orders(path, encoding="utf-8"):
    """Read orders back as a list of dicts using csv.DictReader."""
    with open(path, "r", encoding=encoding) as f:
        return list(csv.DictReader(f))


def run_inventory_pipeline(path_stem):
    """Full shop inventory export/reload pipeline.

    Writes orders to .txt, .json, and .csv alongside path_stem, re-reads
    all three, and returns a summary dict with counts and revenue.
    """
    orders = [
        {"product": "Widget", "qty": 3, "price": 9.99},
        {"product": "Gadget", "qty": 1, "price": 14.50},
        {"product": "Shirt",  "qty": 2, "price": 25.00},
    ]

    txt_path = f"{path_stem}.txt"
    json_path = f"{path_stem}.json"
    csv_path = f"{path_stem}.csv"

    lines = "".join(
        f"{o['product']},{o['qty']},{o['price']:.2f}\n" for o in orders
    )
    write_text_file(txt_path, lines)
    save_json_data(json_path, orders)
    write_csv_orders(csv_path, orders)

    txt_orders = [
        dict(zip(["product", "qty", "price"], line.strip().split(",")))
        for line in read_text_file(txt_path).splitlines()
    ]
    json_orders = load_json_data(json_path)
    csv_orders = read_csv_orders(csv_path)

    total_qty = sum(int(r["qty"]) for r in txt_orders)
    revenue = sum(float(r["price"]) * int(r["qty"]) for r in json_orders)

    return {
        "txt_count": len(txt_orders),
        "json_count": len(json_orders),
        "csv_count": len(csv_orders),
        "total_qty": total_qty,
        "revenue": round(revenue, 2),
        "orders": json_orders,
    }


def delete_file_safely(path):
    """Delete a single file only if it exists (mirrors the notebook)."""
    if path.exists():
        path.unlink()


def delete_folder_safely(path):
    """Delete a folder and its contents only if it exists."""
    if path.exists():
        shutil.rmtree(path)


# ---------------------------------------------------------------------------
# Test Classes
# ---------------------------------------------------------------------------

class TestTextFile:
    """Tests for plain-text write/read round-trips."""

    def test_write_then_read_round_trip(self, tmp_path):
        p = tmp_path / "orders.txt"
        write_text_file(p, "Widget,3,9.99\n")
        assert read_text_file(p) == "Widget,3,9.99\n"

    def test_append_mode_adds_to_existing(self, tmp_path):
        p = tmp_path / "log.txt"
        write_text_file(p, "first line\n")
        write_text_file(p, "second line\n", mode="a")
        assert read_text_file(p) == "first line\nsecond line\n"

    def test_write_mode_replaces_existing(self, tmp_path):
        p = tmp_path / "order.txt"
        write_text_file(p, "old content")
        write_text_file(p, "new content")
        assert read_text_file(p) == "new content"

    def test_reading_missing_file_raises(self, tmp_path):
        p = tmp_path / "nope.txt"
        with pytest.raises(FileNotFoundError):
            read_text_file(p)


class TestJSONFile:
    """Tests for json.dump / json.load round-trips."""

    def test_dump_then_load_round_trip(self, tmp_path):
        p = tmp_path / "data.json"
        data = [{"product": "Widget", "qty": 3, "price": 9.99}]
        save_json_data(p, data)
        assert load_json_data(p) == data

    def test_preserves_list_of_dicts(self, tmp_path):
        p = tmp_path / "orders.json"
        orders = [
            {"product": "Widget", "qty": 3, "price": 9.99},
            {"product": "Gadget", "qty": 1, "price": 14.50},
        ]
        save_json_data(p, orders)
        loaded = load_json_data(p)
        assert isinstance(loaded, list)
        assert len(loaded) == 2
        assert all(isinstance(o, dict) for o in loaded)

    def test_type_is_preserved(self, tmp_path):
        p = tmp_path / "typed.json"
        original = {"count": 5, "price": 9.99, "active": True, "none": None}
        save_json_data(p, original)
        loaded = load_json_data(p)
        assert loaded["count"] == 5
        assert isinstance(loaded["count"], int)
        assert isinstance(loaded["price"], float)
        assert loaded["active"] is True
        assert loaded["none"] is None

    def test_utf8_encoding_round_trip(self, tmp_path):
        p = tmp_path / "emoji.json"
        data = [{"product": "Café ☕", "qty": 2}]
        save_json_data(p, data)
        assert load_json_data(p) == data


class TestCSVReader:
    """Tests for csv.reader raw rows and csv.DictReader."""

    def test_reader_returns_raw_rows(self, tmp_path):
        p = tmp_path / "orders.csv"
        p.write_text("product,qty,price\nWidget,3,9.99\nGadget,1,14.50\n",
                     encoding="utf-8")
        with open(p, "r", encoding="utf-8") as f:
            rows = list(csv.reader(f))
        assert rows == [
            ["product", "qty", "price"],
            ["Widget", "3", "9.99"],
            ["Gadget", "1", "14.50"],
        ]

    def test_dictreader_maps_fieldnames_to_dicts(self, tmp_path):
        p = tmp_path / "orders.csv"
        p.write_text("product,qty,price\nWidget,3,9.99\nGadget,1,14.50\n",
                     encoding="utf-8")
        with open(p, "r", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        assert rows[0] == {"product": "Widget", "qty": "3", "price": "9.99"}
        assert rows[1]["product"] == "Gadget"

    def test_dictreader_uses_first_row_as_header(self, tmp_path):
        p = tmp_path / "orders.csv"
        p.write_text("product,qty,price\nWidget,3,9.99\n", encoding="utf-8")
        with open(p, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            assert reader.fieldnames == ["product", "qty", "price"]


class TestDictWriter:
    """Tests for csv.DictWriter header and round-trip."""

    def test_writeheader_writes_header_first(self, tmp_path):
        p = tmp_path / "out.csv"
        with open(p, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
            writer.writeheader()
        assert read_text_file(p) == "product,qty,price\n"

    def test_rows_come_back_identical(self, tmp_path):
        p = tmp_path / "out.csv"
        with open(p, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
            writer.writeheader()
            writer.writerow({"product": "Widget", "qty": 3, "price": 9.99})
        with open(p, "r", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        assert rows == [{"product": "Widget", "qty": "3", "price": "9.99"}]

    def test_round_trip_via_helpers(self, tmp_path):
        p = tmp_path / "orders.csv"
        orders = [
            {"product": "Widget", "qty": 3, "price": 9.99},
            {"product": "Shirt", "qty": 2, "price": 25.00},
        ]
        write_csv_orders(p, orders)
        loaded = read_csv_orders(p)
        assert [o["product"] for o in loaded] == ["Widget", "Shirt"]
        assert loaded[0]["qty"] == "3"


class TestMissingFile:
    """Tests for safe missing-file error handling."""

    def test_reading_missing_file_raises(self, tmp_path):
        p = tmp_path / "absent.txt"
        with pytest.raises(FileNotFoundError):
            read_text_file(p)

    def test_loading_missing_json_raises(self, tmp_path):
        p = tmp_path / "absent.json"
        with pytest.raises(FileNotFoundError):
            load_json_data(p)

    def test_catching_missing_file_gracefully(self, tmp_path):
        p = tmp_path / "absent.txt"
        try:
            read_text_file(p)
            caught = False
        except FileNotFoundError:
            caught = True
        assert caught

    def test_with_open_context_closes_file(self, tmp_path):
        p = tmp_path / "ctx.txt"
        write_text_file(p, "hello")
        handle = open(p, "r", encoding="utf-8")
        content = None
        with handle as f:
            content = f.read()
        assert content == "hello"
        assert handle.closed


class TestInventoryPipeline:
    """Tests for the combined export/reload/summarize pipeline."""

    def test_pipeline_reports_correct_counts(self, tmp_path):
        result = run_inventory_pipeline(str(tmp_path / "inventory"))
        assert result["txt_count"] == 3
        assert result["json_count"] == 3
        assert result["csv_count"] == 3

    def test_pipeline_reports_correct_quantity_total(self, tmp_path):
        result = run_inventory_pipeline(str(tmp_path / "inventory"))
        assert result["total_qty"] == 6

    def test_pipeline_reports_correct_revenue(self, tmp_path):
        result = run_inventory_pipeline(str(tmp_path / "inventory"))
        assert result["revenue"] == 9.99 * 3 + 14.50 * 1 + 25.00 * 2

    def test_pipeline_preserves_order_list(self, tmp_path):
        result = run_inventory_pipeline(str(tmp_path / "inventory"))
        assert len(result["orders"]) == 3
        assert result["orders"][0]["product"] == "Widget"
        assert result["orders"][2]["product"] == "Shirt"


class TestSafeDeletion:
    """Tests for deleting files and folders safely."""

    def test_unlink_deletes_file(self, tmp_path):
        p = tmp_path / "temp.txt"
        p.write_text("data", encoding="utf-8")
        assert p.exists()
        delete_file_safely(p)
        assert not p.exists()

    def test_unlink_missing_file_no_error(self, tmp_path):
        p = tmp_path / "never_existed.txt"
        delete_file_safely(p)
        assert not p.exists()

    def test_unlink_would_raise_without_guard(self, tmp_path):
        p = tmp_path / "missing.txt"
        with pytest.raises(FileNotFoundError):
            p.unlink()

    def test_rmtree_deletes_folder_contents(self, tmp_path):
        d = tmp_path / "folder"
        d.mkdir()
        (d / "inside.txt").write_text("nested", encoding="utf-8")
        assert d.exists()
        delete_folder_safely(d)
        assert not d.exists()

    def test_rmtree_missing_folder_no_error(self, tmp_path):
        d = tmp_path / "absent_folder"
        delete_folder_safely(d)
        assert not d.exists()

    def test_rmtree_would_raise_without_guard(self, tmp_path):
        d = tmp_path / "no_such_folder"
        with pytest.raises(FileNotFoundError):
            shutil.rmtree(d)

    def test_delete_then_recreate(self, tmp_path):
        p = tmp_path / "cycle.txt"
        write_text_file(p, "first")
        delete_file_safely(p)
        write_text_file(p, "second")
        assert read_text_file(p) == "second"
