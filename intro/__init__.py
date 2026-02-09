from otree.api import *


doc = """
Study introduction (consent + instructions)
"""


class C(BaseConstants):
    NAME_IN_URL = 'intro'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    consent_age_18 = models.BooleanField(label='I confirm I am 18 years or older.')
    consent_read_notice = models.BooleanField(
        label='I have read and understood the Participant Information and Privacy Notice.'
    )
    consent_voluntary = models.BooleanField(
        label='I agree to participate voluntarily and understand I can stop at any time.'
    )
    consent_gdpr6 = models.BooleanField(
        label='I consent to processing of my data for research purposes (GDPR Art. 6(1)(a)).'
    )
    consent_gdpr9 = models.BooleanField(
        label='I explicitly consent to processing data that may reveal my political opinions (GDPR Art. 9(2)(a)).'
    )
    consent_anonymized = models.BooleanField(
        label='I understand anonymized data may be used for scientific publication and sharing.'
    )


class Consent(Page):
    form_model = 'player'
    form_fields = [
        'consent_age_18',
        'consent_read_notice',
        'consent_voluntary',
        'consent_gdpr6',
        'consent_gdpr9',
        'consent_anonymized',
    ]

    @staticmethod
    def error_message(player: Player, values):
        if not all(values.values()):
            return 'You must tick all consent boxes to continue.'


class Instructions(Page):
    @staticmethod
    def vars_for_template(player: Player):
        from main import C as MainC

        cfg = player.session.config
        currency = cfg['payment_currency_symbol']
        tolerance = int(cfg['bonus_tolerance_points'])
        return dict(
            num_movies=MainC.NUM_ROUNDS,
            duration_minutes=int(cfg['estimated_duration_minutes']),
            base_payment_display=f"{currency}{float(cfg['base_payment_amount']):.2f}",
            accuracy_bonus_max_display=f"{currency}{float(cfg['accuracy_bonus_max_amount']):.2f}",
            bonus_per_movie_display=f"{currency}{float(cfg['bonus_per_movie_amount']):.2f}",
            no_bonus_display=f"{currency}{float(cfg['no_bonus_amount']):.2f}",
            bonus_tolerance_points=tolerance,
            bonus_tolerance_label='point' if tolerance == 1 else 'points',
            scale_min=int(cfg['scale_min']),
            scale_max=int(cfg['scale_max']),
        )


page_sequence = [Consent, Instructions]
