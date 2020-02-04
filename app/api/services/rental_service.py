import math
from datetime import datetime

from flask import g, current_app
from sqlalchemy.exc import SQLAlchemyError

from app import IkiruJsonResponse
from app.models import db, Movie, Rental

# resolution loss is negligible
SECONDS_TO_DAYS = 1 / (24*60*60)


def rent_movie(parser):
    args = parser.parse_args()

    movie = Movie.get_by_uuid(args['movie_uuid'])
    if movie is None:
        return IkiruJsonResponse(message='Invalid movie identifier', status_code=404)

    rental = Rental(user_id=g.user.id, movie_id=movie.id)
    db.session.add(rental)
    db.session.commit()
    db.session.refresh(rental)
    return IkiruJsonResponse(
        payload={'date_rented': rental.date_rented},
        message=f'Movie `{movie.title}` rented successfully.'
    )


def _tiered_cost(days_past, costs, tiers):
    # total_cost, current_tier, days_so_far
    tc, ct, dsf = .0, 0, 0
    assert len(costs) == len(tiers) + 1
    while dsf < days_past and ct < len(tiers):
        d = min(days_past, tiers[ct]) - dsf
        tc += costs[ct] * d
        dsf += d
        ct += 1
    tc += max(0, days_past - dsf) * costs[ct]
    return tc


def calculate_cost(date_rented):
    # always bill at least a day (by rounding up even if only a second passed)
    total_secs = (datetime.utcnow() - date_rented).total_seconds()
    days_past = math.ceil(total_secs * SECONDS_TO_DAYS)

    costs = current_app.config['RENTAL_COST_BRACKETS']
    tiers = current_app.config['RENTAL_PRICING_TIER_BRACKETS']
    return _tiered_cost(days_past, costs, tiers)


def return_rental(parser):
    # This shouldn't happen
    if not g.user:
        return IkiruJsonResponse(message='Unable to validate user.', status_code=401)

    args = parser.parse_args()
    rental = Rental.get_by_uuid(args['rental_uuid'])

    if not rental or rental.user.uuid != g.user.uuid:
        return IkiruJsonResponse(message='Invalid rental identifier.', status_code=404)

    # Faulty logic but should work as a proof of concept
    cost = calculate_cost(rental.date_rented)
    try:
        rental.date_returned = datetime.utcnow()
        db.session.commit()
    except SQLAlchemyError as e:
        return IkiruJsonResponse(message=e._message(), status_code=500)

    currency_symbol = current_app.config['PAYMENT_CURRENCY'][2]
    return IkiruJsonResponse({"cost": f'{currency_symbol} {cost}'}, 'Rental returned successfully.')


def get_cost(rental_uuid):
    rental = Rental.get_by_uuid(rental_uuid)
    if not rental or rental.user.uuid != g.user.uuid:
        return IkiruJsonResponse(message='Invalid rental identifier.', status_code=404)

    cost = calculate_cost(rental.date_rented)
    currency_symbol = current_app.config['PAYMENT_CURRENCY'][2]
    return IkiruJsonResponse({"cost": f'{currency_symbol} {cost}'})
