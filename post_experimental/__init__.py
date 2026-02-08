import json
import logging

from otree.api import *


logger = logging.getLogger(__name__)


doc = """
Post-experimental questionnaire
"""


class C(BaseConstants):
    NAME_IN_URL = 'post_experimental'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    GENDER_CHOICES = [
        'Woman',
        'Man',
        'Non-binary / another identity',
        'Prefer not to say',
    ]
    EDUCATION_CHOICES = [
        'Less than high school',
        'High school / secondary school',
        'Some college / vocational training',
        'Bachelor degree',
        'Master degree',
        'Doctorate',
        'Other',
        'Prefer not to say',
    ]
    YES_NO_PNS = ['Yes', 'No', 'Prefer not to say']
    STRATEGY_CHOICES = [
        'I mostly reported my own impression',
        'I mostly tried to guess what most people would think',
        'I used both / it varied by movie',
        'Other',
    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    age = models.IntegerField(
        label='D1. Age (in years)',
        min=18,
        max=120,
    )
    gender = models.StringField(
        label='D2. Gender',
        choices=C.GENDER_CHOICES,
    )
    country_residence = models.StringField(label='D3. Country of residence')
    citizenship = models.StringField(
        label='D4. Citizenship (optional)',
        blank=True,
    )
    education = models.StringField(
        label='D5. Highest completed education',
        choices=C.EDUCATION_CHOICES,
    )
    political_self_placement = models.StringField(
        label='P1. Left-Right self-placement',
        choices=[[str(i), str(i)] for i in range(11)]
        + [['Prefer not to say', 'Prefer not to say']],
    )
    political_interest = models.IntegerField(
        label='P2. How interested are you in politics?',
        choices=[[i, str(i)] for i in range(1, 8)],
        widget=widgets.RadioSelect,
    )
    party_identification = models.StringField(
        label='P3. Do you identify with a political party or movement?',
        choices=C.YES_NO_PNS,
    )
    party_identification_text = models.StringField(
        label='If yes, which one?',
        blank=True,
    )
    attention_check = models.IntegerField(
        label='Q1. Attention check: To show you are paying attention, please select option 3 for this question.',
        choices=[[i, str(i)] for i in range(1, 8)],
        widget=widgets.RadioSelect,
    )
    seriousness_check = models.StringField(
        label='Q2. Did you answer the questions carefully and honestly?',
        choices=C.YES_NO_PNS,
    )
    prediction_strategy = models.StringField(
        label='S1. How did you make your predictions about the average participant?',
        choices=C.STRATEGY_CHOICES,
    )
    prediction_strategy_other = models.StringField(
        label='If "Other", please specify',
        blank=True,
    )
    comments = models.LongStringField(
        label='F1. Any comments about the study? (optional)',
        blank=True,
    )


class SurveyJSPage(Page):
    def process_survey_data(self, data):
        raise NotImplementedError

    def post(self):
        if not self.participant.is_browser_bot:
            try:
                raw = self._form_data.get('surveyResults')
                if not raw:
                    raise ValueError('Missing surveyResults payload')
                survey_results = json.loads(raw)
                self.process_survey_data(survey_results)
            except json.JSONDecodeError as exc:
                logger.error('Invalid SurveyJS JSON on %s: %s', self.__class__.__name__, exc)
                raise
            except Exception as exc:
                logger.error('Survey processing failed on %s: %s', self.__class__.__name__, exc)
                raise
        return super().post()


class ExitQuestionnaire(SurveyJSPage):
    def process_survey_data(self, data):
        self.player.age = int(data['age'])
        self.player.gender = data['gender']
        self.player.country_residence = data['country_residence'].strip()
        self.player.citizenship = data.get('citizenship', '').strip()
        self.player.education = data['education']
        self.player.political_self_placement = str(data['political_self_placement'])
        self.player.political_interest = int(data['political_interest'])
        self.player.party_identification = data['party_identification']
        self.player.party_identification_text = data.get('party_identification_text', '').strip()
        self.player.attention_check = int(data['attention_check'])
        self.player.seriousness_check = data['seriousness_check']
        self.player.prediction_strategy = data['prediction_strategy']
        self.player.prediction_strategy_other = data.get('prediction_strategy_other', '').strip()
        self.player.comments = data.get('comments', '').strip()


class Completion(Page):
    pass


page_sequence = [ExitQuestionnaire, Completion]
