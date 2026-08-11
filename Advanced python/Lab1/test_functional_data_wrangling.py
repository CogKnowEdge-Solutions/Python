"""End-to-end tests for lab-functional-data-wrangling.ipynb.

The notebook is executed top-to-bottom in a fresh kernel via testbook; tests
then assert on real kernel state and cell output. The pip-install cell
(`!{sys.executable} -m pip install ...`) is stripped so the run is hermetic and
offline.

Run from the lab folder::

    pip install pytest testbook ipykernel
    pytest test_functional_data_wrangling.py -q
"""

import asyncio
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import pytest
from testbook import testbook

NOTEBOOK = "lab-functional-data-wrangling.ipynb"


@pytest.fixture(scope="module")
def executed_nb():
    with testbook(NOTEBOOK, execute=False) as tb:
        tb.nb.cells = [
            cell for cell in tb.nb.cells
            if not (cell.cell_type == "code" and "pip install" in cell.source)
        ]
        tb.execute()
        yield tb


class TestDataIntegrity:
    def test_notebook_loads_37_records(self, executed_nb):
        assert len(executed_nb.ref("catalog")) == 37

    def test_catalog_has_five_categories(self, executed_nb):
        catalog = executed_nb.ref("catalog")
        assert {p["category"] for p in catalog} == {
            "Electronics", "Home & Kitchen", "Apparel", "Sports & Outdoors", "Books"}

    def test_catalog_discontinued_ids(self, executed_nb):
        catalog = executed_nb.ref("catalog")
        assert {p["id"] for p in catalog if p["discontinued"]} == {105, 205, 305, 404, 504}

    def test_catalog_zero_stock_ids(self, executed_nb):
        catalog = executed_nb.ref("catalog")
        assert {p["id"] for p in catalog if p.get("stock") == 0} == {102, 203, 302, 403, 503}

    def test_catalog_no_stock_field_ids(self, executed_nb):
        catalog = executed_nb.ref("catalog")
        assert {p["id"] for p in catalog if "stock" not in p and "qty" not in p} == {109, 207, 406}

    def test_catalog_qty_fallback_ids(self, executed_nb):
        catalog = executed_nb.ref("catalog")
        assert {p["id"] for p in catalog if "stock" not in p and "qty" in p} == {106, 505}

    def test_catalog_string_price_ids(self, executed_nb):
        catalog = executed_nb.ref("catalog")
        assert {p["id"] for p in catalog if isinstance(p.get("price"), str)} == {103, 202, 208, 405, 502}

    def test_catalog_null_price_ids(self, executed_nb):
        catalog = executed_nb.ref("catalog")
        assert {p["id"] for p in catalog if "price" in p and p["price"] is None} == {108, 306, 506}

    def test_catalog_nested_pricing_two_non_usd(self, executed_nb):
        catalog = executed_nb.ref("catalog")
        nested = [p for p in catalog if "pricing" in p]
        assert len(nested) == 5
        non_usd = {p["pricing"]["currency"] for p in nested if p["pricing"]["currency"] != "USD"}
        assert non_usd == {"EUR", "GBP"}


class TestPipeline:
    def test_notebook_selects_21_active_products(self, executed_nb):
        assert len(executed_nb.ref("active")) == 21

    @pytest.mark.parametrize("name,price,sale", [
        ("Wireless Mouse", 23.91, 21.52),
        ("Running Shoes", 59.79, 53.81),
        ("Gaming Monitor 27in", 229.99, 206.99),
        ("Cotton T-Shirt", 9.19, 8.27),
        ("Wool Beanie", 11.95, 10.76),
        ("Self-Help Bestseller", 15.63, 14.07),
    ])
    def test_known_conversion_values(self, name, price, sale, executed_nb):
        priced = executed_nb.ref("priced")
        product = next(p for p in priced if p["name"] == name)
        assert product["price_eur"] == price
        assert product["sale_eur"] == sale

    def test_map_agrees_with_comprehension(self, executed_nb):
        assert executed_nb.ref("priced_alt") == executed_nb.ref("priced")

    def test_named_and_lambda_predicates_agree(self, executed_nb):
        assert executed_nb.ref("via_function") == executed_nb.ref("via_lambda")
        assert len(executed_nb.ref("via_function")) == 21

    def test_final_ranking_order_matches_section_5(self, executed_nb):
        final = executed_nb.ref("final")
        assert [p["name"] for p in final] == [
            "Running Shoes", "Leather Belt", "Wool Beanie", "Cotton T-Shirt",
            "Cookbook: World Cuisines", "Self-Help Bestseller", "Bestselling Novel",
            "Gaming Monitor 27in", "Portable SSD 1TB", "Bluetooth Earbuds",
            "USB-C Hub", "Wireless Mouse", "Vacuum Sealer", "Ceramic Dinner Set",
            "Non-Stick Frying Pan", "Coffee Grinder", "Stainless Steel Water Bottle",
            "Adjustable Dumbbells", "Yoga Mat", "Insulated Water Bottle",
            "Resistance Bands Set",
        ]

    def test_table_cell_prints_full_21_row_grid(self, executed_nb):
        index = next(i for i, cell in enumerate(executed_nb.cells)
                     if cell.cell_type == "code" and "tabulate(rows" in cell.source)
        text = executed_nb.cell_output_text(index)
        assert "Price (EUR)" in text and "Sale (EUR)" in text
        assert text.count("| Apparel") == 4
        assert text.count("| Books") == 3
        assert text.count("| Electronics") == 5
        assert text.count("| Home & Kitchen") == 5
        assert text.count("| Sports & Outdoors") == 4


class TestOptionalExercise:
    def test_gbp_swap_preserves_ranking_order(self, executed_nb):
        executed_nb.inject(
            "usd_to_gbp = 0.79\n"
            "final_gbp = sorted(\n"
            "    map(lambda product: {\n"
            "        'name': product['name'],\n"
            "        'category': product['category'],\n"
            "        'price_gbp': round(to_usd(product) * usd_to_gbp, 2),\n"
            "    }, active),\n"
            "    key=lambda product: (product['category'], -product['price_gbp']),\n"
            ")\n"
        )
        eur_names = [p["name"] for p in executed_nb.ref("final")]
        gbp_names = [p["name"] for p in executed_nb.ref("final_gbp")]
        assert eur_names == gbp_names


class TestEnvironmentAndConfig:
    def test_tabulate_pinned_version(self):
        import tabulate
        assert tabulate.__version__ == "0.10.0"

    def test_no_credential_patterns_in_shipped_files(self):
        from pathlib import Path

        notebook_text = Path(NOTEBOOK).read_text(encoding="utf-8")
        data_text = (Path("data") / "product_catalog.json").read_text(encoding="utf-8")
        for pattern in ("sk-", "api_key", "apiKey", "password", "secret", "Bearer "):
            assert pattern not in notebook_text
            assert pattern not in data_text
