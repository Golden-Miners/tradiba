from tradiba.alternative_data.geospatial.intelligence import GeospatialIntelligence

def test_geospatial():
    geo = GeospatialIntelligence()
    assert geo.index_data("g1")
