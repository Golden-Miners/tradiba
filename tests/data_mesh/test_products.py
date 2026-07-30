from tradiba.data_mesh.products.manager import DataProductManager

def test_products():
    manager = DataProductManager()
    assert manager.publish_product("p1", {})
