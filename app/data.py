from flask import url_for

from .utils.money import Money, USD, GBP

customers = {
    'Holmes': {
        'first_name': 'Sherlock',
        'last_name': 'Holmes',
        'address': '221B Baker Street',
        'zip_code': 'NW1 6XE',
        'city': 'London',
        'country': 'United Kingdom',
        'email': 'sherlock54@home.ok'
    }
}


items = {
    'pipe': {
        'name': 'Tobacco Pipe',
        'code': 'TB89-MB',
        'image_filename': 'images/items/pipe.jpg',
        'price': Money(currency=GBP, amount=1599)
    },
    'hat': {
        'name': 'Mustang Cowboy Hat',
        'code': 'CH56-LB',
        'image_filename': 'images/items/hat.jpeg',
        'price': Money(currency=USD, amount=18000)
    },
    'glass': {
        'name': 'Whiskey Glass',
        'code': 'WG88-M240',
        'image_filename': 'images/items/glass.jpeg',
        'price': Money(currency=USD, amount=9)
    }
}