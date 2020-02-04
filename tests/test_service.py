import time
from datetime import datetime, timedelta

from app.api.services.rental_service import _tiered_cost, calculate_cost


def test_tiered_costs():
    costs = [_tiered_cost(x, [5, 4, 3, 2, 1], [2, 5, 8, 10]) for x in range(13)]
    expected_costs = [0, 5, 10, 14, 18, 22, 25, 28, 31, 33, 35, 36, 37, 38]
    for x, y in zip(costs, expected_costs):
        assert abs(x - y) < 1e-8


def test_calculate_costs(app):
    now = datetime.utcnow()
    time.sleep(1)

    # 12h diff
    h12 = timedelta(seconds=17*3600)

    inputs = [now - n*h12 for n in range(12)]
    costs = [calculate_cost(d) for d in inputs]
    # hours: [0, 17, 34, 51, 68, 85, 102, 119, 136, 153, 170, 187]
    # days:          [1, 1, 2, 3, 3, 4, 5, 5, 6, 7, 8, 8]
    expected_costs = [1, 1, 2, 3, 3, 3.5, 4, 4, 4.5, 5, 5.5, 5.5]

    for x, y in zip(costs, expected_costs):
        assert abs(x - y) < 1e-8
