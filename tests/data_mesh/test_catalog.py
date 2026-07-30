from tradiba.data_mesh.catalog.inventory import CatalogInventory

def test_catalog():
    cat = CatalogInventory()
    assert cat.list_products() == []
