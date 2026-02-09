from os import environ

SESSION_CONFIGS = [
    dict(
        name='full_study',
        display_name='Full Study (intro + main + post_experimental)',
        app_sequence=['intro', 'main', 'post_experimental'],
        num_demo_participants=1,
    ),
    dict(
        name='intro_only',
        display_name='Intro Only',
        app_sequence=['intro'],
        num_demo_participants=1,
    ),
    dict(
        name='main_only',
        display_name='Main Only',
        app_sequence=['main'],
        num_demo_participants=1,
    ),
    dict(
        name='post_experimental_only',
        display_name='Post-Experimental Only',
        app_sequence=['post_experimental'],
        num_demo_participants=1,
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00,
    participation_fee=0.00,
    doc="",
    estimated_duration_minutes=30,
    payment_currency_symbol="€",
    base_payment_amount=1.50,
    accuracy_bonus_max_amount=1.50,
    bonus_per_movie_amount=0.10,
    bonus_tolerance_points=1,
    scale_min=1,
    scale_max=7,
    no_bonus_amount=0.00,
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '2899852870928'
