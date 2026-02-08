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

        return dict(num_movies=MainC.NUM_ROUNDS)


page_sequence = [Consent, Instructions]
