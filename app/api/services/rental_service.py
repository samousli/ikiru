import math
from datetime import datetime

from flask import g, current_app
from sqlalchemy.exc import SQLAlchemyError

from app.models import db, Movie, Rental
from app.common.responses import IkiruJsonResponse, Status

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
        payload=rental,
        message=f'Movie `{movie.title}` rented successfully.'
    )


def _tiered_cost(days_past, costs, tiers):
    total_cost, current_tier, days_so_far = .0, 0, 0
    # ToDo: Perhaps assert config constraints during init/update of config
    assert len(costs) == len(tiers) + 1
    while days_so_far < days_past and current_tier < len(tiers):
        days_in_current_tier = min(days_past, tiers[current_tier]) - days_so_far
        total_cost += costs[current_tier] * days_in_current_tier
        days_so_far += days_in_current_tier
        current_tier += 1
    total_cost += max(0, days_past - days_so_far) * costs[current_tier]
    return total_cost


def calculate_cost(date_rented):
    # always bill at least a day (by rounding up even if only a second passed)
    total_secs = (datetime.utcnow() - date_rented).total_seconds()
    days_past = math.ceil(total_secs * SECONDS_TO_DAYS)

    costs = current_app.config['RENTAL_COST_BRACKETS']
    tiers = current_app.config['RENTAL_PRICING_TIER_BRACKETS']
    return _tiered_cost(days_past, costs, tiers)


def formatted_cost(rental_date):
    cost = calculate_cost(rental_date)
    currency_symbol = current_app.config['PAYMENT_CURRENCY'][2]
    return f'{currency_symbol}{cost:.2f}'


def return_rental(parser):
    # This shouldn't happen
    if not g.user:
        return IkiruJsonResponse(message='Unable to validate user.', status_code=401)

    args = parser.parse_args()
    rental = Rental.get_by_uuid(args['rental_uuid'])

    if not rental or rental.user.uuid != g.user.uuid:
        return IkiruJsonResponse(message='Invalid rental identifier.', status_code=404)

    if rental.was_returned():
        return IkiruJsonResponse(message='Rental already returned.', status_code=Status.UNPROCESSABLE_ENTITY)

    # Faulty logic but should work as a proof of concept
    try:
        rental.date_returned = datetime.utcnow()
        db.session.commit()
    except SQLAlchemyError as e:
        return IkiruJsonResponse(message=e._message(), status_code=500)

    return IkiruJsonResponse({"cost": formatted_cost(rental.date_rented)}, 'Rental returned successfully.')


def get_cost(rental_uuid):
    rental = Rental.get_by_uuid(rental_uuid)
    if not rental or rental.user.uuid != g.user.uuid:
        return IkiruJsonResponse(message='Invalid rental identifier.', status_code=404)
    return IkiruJsonResponse({"cost": formatted_cost(rental.date_rented)})
