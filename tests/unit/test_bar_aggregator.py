from datetime import datetime
from datetime import timezone

from tradiba.market.aggregator import BarAggregator
from tradiba.market.models import Tick
from tradiba.market.models import Timeframe


def tick(second, price):

    return Tick(
        symbol="EURUSD",
        bid=price,
        ask=price,
        volume=1,
        time=datetime(
            2025,
            1,
            1,
            12,
            0,
            second,
            tzinfo=timezone.utc,
        ),
    )


def test_single_bar():

    agg = BarAggregator(Timeframe.M1)

    assert agg.update(tick(0, 1.1000)) is None
    assert agg.update(tick(10, 1.1005)) is None
    assert agg.update(tick(20, 1.0995)) is None

    candle = agg.current()

    assert candle.open == 1.1000
    assert candle.high == 1.1005
    assert candle.low == 1.0995
    assert candle.close == 1.0995
    assert candle.volume == 3


def test_bar_close():

    agg = BarAggregator(Timeframe.M1)

    agg.update(tick(0, 1.1000))
    agg.update(tick(10, 1.1010))

    event = agg.update(
        Tick(
            symbol="EURUSD",
            bid=1.1020,
            ask=1.1020,
            volume=1,
            time=datetime(
                2025,
                1,
                1,
                12,
                1,
                0,
                tzinfo=timezone.utc,
            ),
        )
    )

    assert event is not None

    candle = event.candle

    assert candle.open == 1.1000
    assert candle.high == 1.1010
    assert candle.low == 1.1000
    assert candle.close == 1.1010
