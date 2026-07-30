from tradiba.alternative_data.news.intelligence import NewsIntelligence

def test_news():
    news = NewsIntelligence()
    assert news.process_news("a1")["sentiment"] == 0.8
