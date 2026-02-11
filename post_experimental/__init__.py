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
    SECS_ITEM_SPECS = [
        ('secs_religion', 'S', False),
        ('secs_trad_marriage', 'S', False),
        ('secs_business', 'E', False),
        ('secs_welfare', 'E', True),
        ('secs_abortion', 'S', False),
        ('secs_family', 'S', False),
        ('secs_limited_gov', 'E', False),
        ('secs_military', 'S', False),
        ('secs_patriotism', 'S', False),
        ('secs_trad_values', 'S', False),
        ('secs_guns', 'S', False),
        ('secs_fiscal', 'E', False),
    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    age = models.IntegerField(
        label='Age (in years)',
        min=18,
        max=120,
    )
    gender = models.StringField(
        label='Gender',
        choices=C.GENDER_CHOICES,
    )
    country_residence = models.StringField(label='Country of residence')
    education = models.StringField(
        label='Highest completed education',
        choices=C.EDUCATION_CHOICES,
    )
    political_self_placement = models.StringField(
        label='Left-Right self-placement',
        choices=[[str(i), str(i)] for i in range(1, 11)]
        + [['Prefer not to say', 'Prefer not to say']],
    )
    allbus_left_right_numeric = models.IntegerField(
        label='Left-Right self-placement (numeric 1-10)',
        min=1,
        max=10,
        blank=True,
    )
    secs_religion = models.IntegerField(label='SECS: Religion', min=0, max=100, blank=True)
    secs_trad_marriage = models.IntegerField(label='SECS: Traditional marriage', min=0, max=100, blank=True)
    secs_business = models.IntegerField(label='SECS: Business', min=0, max=100, blank=True)
    secs_welfare = models.IntegerField(label='SECS: Welfare benefits', min=0, max=100, blank=True)
    secs_abortion = models.IntegerField(label='SECS: Abortion', min=0, max=100, blank=True)
    secs_family = models.IntegerField(label='SECS: The family unit', min=0, max=100, blank=True)
    secs_limited_gov = models.IntegerField(label='SECS: Limited government', min=0, max=100, blank=True)
    secs_military = models.IntegerField(label='SECS: Military and national security', min=0, max=100, blank=True)
    secs_patriotism = models.IntegerField(label='SECS: Patriotism', min=0, max=100, blank=True)
    secs_trad_values = models.IntegerField(label='SECS: Traditional values', min=0, max=100, blank=True)
    secs_guns = models.IntegerField(label='SECS: Gun ownership', min=0, max=100, blank=True)
    secs_fiscal = models.IntegerField(label='SECS: Fiscal responsibility', min=0, max=100, blank=True)
    secs_economic_score = models.FloatField(
        label='SECS economic conservatism score (0-100; higher=more conservative)',
        blank=True,
    )
    secs_cultural_score = models.FloatField(
        label='SECS cultural conservatism score (0-100; higher=more conservative)',
        blank=True,
    )
    secs_left_right_reconstructed = models.FloatField(
        label='SECS reconstructed left-right position (1-10)',
        blank=True,
    )
    secs_allbus_diff = models.FloatField(
        label='ALLBUS declared minus SECS reconstructed left-right (1-10)',
        blank=True,
    )
    political_interest = models.IntegerField(
        label='How interested are you in politics?',
        choices=[[i, str(i)] for i in range(1, 8)],
        widget=widgets.RadioSelect,
    )
    party_identification = models.StringField(
        label='Do you identify with a political party or movement?',
        choices=C.YES_NO_PNS,
    )
    party_identification_text = models.StringField(
        label='If yes, which one?',
        blank=True,
    )
    attention_check = models.IntegerField(
        label='Attention check: To show you are paying attention, please select option 3 for this question.',
        choices=[[i, str(i)] for i in range(1, 8)],
        widget=widgets.RadioSelect,
    )
    seriousness_check = models.StringField(
        label='Did you answer the questions carefully and honestly?',
        choices=C.YES_NO_PNS,
    )
    prediction_strategy = models.StringField(
        label='How did you make your predictions about the average participant?',
        choices=C.STRATEGY_CHOICES,
    )
    prediction_strategy_other = models.StringField(
        label='If "Other", please specify',
        blank=True,
    )
    comments = models.LongStringField(
        label='Any comments about the study? (optional)',
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
        self.player.country_residence = str(data['country_residence']).strip()
        self.player.education = data['education']
        self.player.political_self_placement = str(data['political_self_placement'])
        self.player.allbus_left_right_numeric = (
            int(self.player.political_self_placement)
            if self.player.political_self_placement.isdigit()
            else None
        )

        secs_scores = {'E': [], 'S': []}
        for field_name, dim, reverse in C.SECS_ITEM_SPECS:
            value = int(data[field_name])
            setattr(self.player, field_name, value)
            scored = 100 - value if reverse else value
            secs_scores[dim].append(scored)

        self.player.secs_economic_score = sum(secs_scores['E']) / len(secs_scores['E'])
        self.player.secs_cultural_score = sum(secs_scores['S']) / len(secs_scores['S'])
        secs_combined_0_to_100 = (self.player.secs_economic_score + self.player.secs_cultural_score) / 2
        self.player.secs_left_right_reconstructed = 1 + 9 * (secs_combined_0_to_100 / 100)
        self.player.secs_allbus_diff = (
            self.player.allbus_left_right_numeric - self.player.secs_left_right_reconstructed
            if self.player.allbus_left_right_numeric is not None
            else None
        )

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
