import logging

from otree.api import *

try:
    from user_agents import parse as parse_user_agent
except ImportError:  # pragma: no cover - dependency installed in runtime
    parse_user_agent = None


logger = logging.getLogger(__name__)


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

    # User agent info
    user_agent_browser = models.StringField(blank=True)
    user_agent_browser_version = models.StringField(blank=True)
    user_agent_os = models.StringField(blank=True)
    user_agent_os_version = models.StringField(blank=True)
    user_agent_device = models.StringField(blank=True)
    user_agent_is_bot = models.BooleanField(initial=False)
    user_agent_is_mobile = models.BooleanField(initial=False)
    user_agent_is_tablet = models.BooleanField(initial=False)
    user_agent_is_pc = models.BooleanField(initial=False)


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

    def get(self, *args, **kwargs):
        user_agent_string = self.request.headers.get('User-Agent', '')
        if parse_user_agent:
            user_agent = parse_user_agent(user_agent_string)
            self.player.user_agent_browser = user_agent.browser.family or ''
            self.player.user_agent_browser_version = user_agent.browser.version_string or ''
            self.player.user_agent_os = user_agent.os.family or ''
            self.player.user_agent_os_version = user_agent.os.version_string or ''
            self.player.user_agent_device = user_agent.device.family or ''
            self.player.user_agent_is_mobile = bool(user_agent.is_mobile)
            self.player.user_agent_is_tablet = bool(user_agent.is_tablet)
            self.player.user_agent_is_pc = bool(user_agent.is_pc)
            self.player.user_agent_is_bot = bool(user_agent.is_bot)
        else:
            logger.warning('user-agents package not installed; User-Agent details were not parsed.')
            self.player.user_agent_device = user_agent_string[:255]
        return super().get(*args, **kwargs)

    @staticmethod
    def error_message(player: Player, values):
        if not all(values.values()):
            return "You must answer 'Yes' to each consent item to continue."


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
