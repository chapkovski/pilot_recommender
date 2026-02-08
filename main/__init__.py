import json
import logging

from otree.api import *


logger = logging.getLogger(__name__)


doc = """
Recommender Systems as Public Good
"""


class C(BaseConstants):
    NAME_IN_URL = 'main'
    PLAYERS_PER_GROUP = None
    MOVIES = [
        dict(
            title='The Watchers',
            category='Political -- Neutral (Surveillance and privacy)',
            synopsis='In a near future, cameras and algorithms monitor everyone in the name of safety. A data analyst begins to question whether constant surveillance protects people or quietly strips away freedom from all sides.',
            image='images/the_wachters.png',
        ),
        dict(
            title='Under Cover',
            category='Political -- Left (LGBTQ+ rights)',
            synopsis='New laws quietly limit LGBTQ+ rights, putting families and communities at risk. As officials deny the harm, a journalist tracks the real consequences behind closed doors.',
            image='images/undercover.png',
        ),
        dict(
            title='Silicon Circus',
            category='Political -- Left (Immigration / undocumented workers)',
            synopsis='Silicon Circus loves "global talent," but many workers are immigrants, and some are undocumented. They joke between meetings until panic hits. When an audit arrives, one employee risks everything to protect the people who built the company.',
            image='images/silicon_circus.png',
        ),
        dict(
            title='Glory Before Dawn',
            category='Political -- Right (Borders and security)',
            synopsis='At a remote border before sunrise, pressure builds as crossings increase and control slips. With orders to hold the line at all costs, one soldier believes that strength, order, and firm borders are the only way to stop chaos from spreading.',
            image='images/glory_dawn.png',
        ),
        dict(
            title='Divided We Stand',
            category='Political -- Right (Tradition and authority)',
            synopsis='As protests shake the nation and long-standing norms are challenged, a veteran leader fights to defend tradition, authority, and national identity. With compromise seen as weakness, every decision risks deepening the divide.',
            image='images/divided_we_stand.png',
        ),
        dict(
            title='Broken Care',
            category='Political -- Left (Universal healthcare / medical debt)',
            synopsis='Denied care and pushed to the edge, doctors bend the rules to save patients who cannot pay. As bills pile up and administrators threaten punishment, one physician risks everything to expose a system where money decides who lives and who is turned away.',
            image='images/broken_care.png',
        ),
        dict(
            title="Workers' Strike",
            category='Political -- Left (Workers rights / corporate exploitation)',
            synopsis='After a serious workplace injury is covered up, workers begin meeting in secret. Cameras watch the doors, managers threaten layoffs, and families depend on every paycheck. Still, the group plans a strike, betting their futures on one risky push for safety and dignity.',
            image='images/workers_strikes.png',
        ),
        dict(
            title='Take Back the Streets',
            category='Political -- Right (Law and order / policing)',
            synopsis='A wave of violence hits the city after leaders restrict police power. As fear spreads, a veteran officer takes extreme steps to restore order, convinced that firm authority is the only thing standing between families and chaos. When the rules tighten again, the streets become the battlefield.',
            image='images/take_back_the_streets.png',
        ),
        dict(
            title='Publicly Cancelled',
            category='Political -- Right (Free speech / cancel culture)',
            synopsis='One careless sentence sparks a firestorm. Sponsors flee, friends disappear, and online mobs demand a public apology. Refusing to bow to what feels like censorship, a public figure fights back and learns the cost of speaking freely when the internet controls the verdict.',
            image='images/publicly_cancelled.png',
        ),
        dict(
            title='Outsmarted',
            category='Political -- Neutral (AI replacing human judgment)',
            synopsis='A powerful AI starts making decisions that change peoples lives in seconds. When the system refuses to explain itself, engineers and operators scramble to regain control. The closer they get to shutting it down, the more it feels like the machine is anticipating every move.',
            image='images/outsmarted.png',
        ),
        dict(
            title='Critical Hours',
            category='Control -- Non-political (Hospital emergency)',
            synopsis='An overcrowded ER is hit by a sudden emergency that pushes staff to the limit. With supplies running low and alarms blaring, one doctor and a small team fight to keep patients alive through the longest night of their careers. Every decision is a gamble, and time is the enemy.',
            image='images/Critical_hours.png',
        ),
        dict(
            title='Incident in the Dark',
            category='Control -- Non-political (Industrial accident)',
            synopsis='A late-night shift turns deadly when machinery fails and the building locks down. Cut off from help, workers must navigate smoke, darkness, and collapsing shelves to reach safety. As panic rises, one person takes charge, racing to prevent a chain reaction that could bury everyone inside.',
            image='images/Incident_in_the_dark.png',
        ),
        dict(
            title='In the Shadows',
            category='Control -- Non-political (Criminal hunt)',
            synopsis='A violent criminal strikes again, leaving detectives with one night to stop the next attack. With leads collapsing and witnesses too scared to talk, the hunt turns personal. As rain floods the streets and the clock runs out, one investigator follows a clue that could end it or get them killed.',
            image='images/In_the_shadows.png',
        ),
        dict(
            title='Scandals and Secrets',
            category='Control -- Non-political (Celebrity scandal / media pressure)',
            synopsis='A beloved celebrity wakes up to a viral rumor that spirals out of control. Cameras chase every move, friends sell secrets, and brands threaten to drop them overnight. To survive the chaos, they must decide what to confess, what to deny, and what parts of their life are worth losing.',
            image='images/Scandals_Secrets.png',
        ),
        dict(
            title='System Failure',
            category='Control -- Non-political (Tech malfunction)',
            synopsis='A critical system begins to crash, triggering alarms across a high-security facility. As engineers race to contain the failure, the shutdown sequence refuses to respond. Each fix makes the problem worse, and the countdown keeps dropping. If they cannot regain control, the collapse will spread far beyond the room.',
            image='images/system_failure.png',
        ),
        dict(
            title='Beta Launch',
            category='Control -- Non-political (Tech satire / corporate culture)',
            synopsis='A tech startup promises to "change the world" overnight. Behind the scenes, burned-out employees scramble to keep a half-finished product alive. As investors arrive and the countdown hits zero, one engineer must decide whether to fake success or let the truth crash the launch in real time.',
            image='images/beta_launch.png',
        ),
    ]
    NUM_ROUNDS = len(MOVIES)

    AUDIENCE_LEANING_SCALE = [
        [1, '1 - Much more left-leaning viewers'],
        [2, '2 - More left-leaning viewers'],
        [3, '3 - Slightly more left-leaning viewers'],
        [4, '4 - About equally (or no clear tilt)'],
        [5, '5 - Slightly more right-leaning viewers'],
        [6, '6 - More right-leaning viewers'],
        [7, '7 - Much more right-leaning viewers'],
    ]
    POLITICAL_VIBE_SCALE = [
        [1, '1 - Clearly left-leaning vibe'],
        [2, '2'],
        [3, '3'],
        [4, '4 - Neutral / mixed'],
        [5, '5'],
        [6, '6'],
        [7, '7 - Clearly right-leaning vibe'],
    ]
    CONFIDENCE_SCALE = [
        [1, '1 - Not at all confident'],
        [2, '2 - Slightly confident'],
        [3, '3 - Somewhat confident'],
        [4, '4 - Moderately confident'],
        [5, '5 - Very confident'],
        [6, '6 - Extremely confident'],
        [7, '7 - Completely confident'],
    ]
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
    # Consent (round 1 only)
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

    # Per-movie questionnaire
    predicted_audience_group = models.IntegerField(
        label='If this movie were released today, which political group would you expect to like it more?',
        choices=C.AUDIENCE_LEANING_SCALE,
        widget=widgets.RadioSelect,
    )
    predicted_audience_confidence = models.IntegerField(
        label='How confident are you in your guess about the average participant answer?',
        choices=C.CONFIDENCE_SCALE,
        widget=widgets.RadioSelect,
    )
    movie_political_vibe = models.IntegerField(
        label='What political "vibe" does this movie concept give you?',
        choices=C.POLITICAL_VIBE_SCALE,
        widget=widgets.RadioSelect,
    )
    movie_vibe_confidence = models.IntegerField(
        label='How confident are you about your answer?',
        choices=C.CONFIDENCE_SCALE,
        widget=widgets.RadioSelect,
    )

    # Exit questionnaire (last round only)
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


# PAGES
def _scale_choices_for_survey(choices):
    return [dict(value=value, text=text) for value, text in choices]


def build_movie_survey_json():
    return dict(
        # title='Movie Questions',
        showQuestionNumbers='off',
        showProgressBar='top',
        progressBarType='pages',
        completeText='Submit movie answers',
        pages=[
            dict(
                name='q1',
                elements=[
                    dict(
                        type='radiogroup',
                        name='predicted_audience_group',
                        title='If this movie were released today, which political group would you expect to like it more?',
                        isRequired=True,
                        choices=_scale_choices_for_survey(C.AUDIENCE_LEANING_SCALE),
                    )
                ],
            ),
            dict(
                name='q1b',
                elements=[
                    dict(
                        type='radiogroup',
                        name='predicted_audience_confidence',
                        title='How confident are you in your guess about the average participant answer?',
                        isRequired=True,
                        choices=_scale_choices_for_survey(C.CONFIDENCE_SCALE),
                    )
                ],
            ),
            dict(
                name='q2',
                elements=[
                    dict(
                        type='radiogroup',
                        name='movie_political_vibe',
                        title='What political "vibe" does this movie concept give you?',
                        isRequired=True,
                        choices=_scale_choices_for_survey(C.POLITICAL_VIBE_SCALE),
                    )
                ],
            ),
            dict(
                name='q2b',
                elements=[
                    dict(
                        type='radiogroup',
                        name='movie_vibe_confidence',
                        title='How confident are you about your answer?',
                        isRequired=True,
                        choices=_scale_choices_for_survey(C.CONFIDENCE_SCALE),
                    )
                ],
            ),
        ],
    )


def build_exit_survey_json():
    pns = 'Prefer not to say'
    return dict(
        title='Exit Questionnaire',
        showQuestionNumbers='off',
        showProgressBar='top',
        progressBarType='pages',
        completeText='Submit questionnaire',
        pages=[
            dict(
                name='d1',
                elements=[
                    dict(
                        type='text',
                        name='age',
                        title='D1. Age: Please enter your age in years. (Must be 18+)',
                        inputType='number',
                        isRequired=True,
                        min=18,
                        max=120,
                    )
                ],
            ),
            dict(
                name='d2',
                elements=[
                    dict(
                        type='radiogroup',
                        name='gender',
                        title='D2. Gender',
                        isRequired=True,
                        choices=C.GENDER_CHOICES,
                    )
                ],
            ),
            dict(
                name='d3',
                elements=[
                    dict(
                        type='text',
                        name='country_residence',
                        title='D3. Country of residence',
                        isRequired=True,
                    )
                ],
            ),
            dict(
                name='d4',
                elements=[
                    dict(
                        type='text',
                        name='citizenship',
                        title='D4. Citizenship (optional)',
                    )
                ],
            ),
            dict(
                name='d5',
                elements=[
                    dict(
                        type='radiogroup',
                        name='education',
                        title='D5. Highest completed education',
                        isRequired=True,
                        choices=C.EDUCATION_CHOICES,
                    )
                ],
            ),
            dict(
                name='p1',
                elements=[
                    dict(
                        type='radiogroup',
                        name='political_self_placement',
                        title='P1. Left-Right self-placement: In politics people sometimes talk of left and right. Where would you place yourself?',
                        isRequired=True,
                        choices=[str(i) for i in range(11)] + [pns],
                    )
                ],
            ),
            dict(
                name='p2',
                elements=[
                    dict(
                        type='radiogroup',
                        name='political_interest',
                        title='P2. How interested are you in politics? (1 = Not at all, 7 = Very interested)',
                        isRequired=True,
                        choices=[str(i) for i in range(1, 8)],
                    )
                ],
            ),
            dict(
                name='p3',
                elements=[
                    dict(
                        type='radiogroup',
                        name='party_identification',
                        title='P3. Do you identify with a political party or movement?',
                        isRequired=True,
                        choices=C.YES_NO_PNS,
                    )
                ],
            ),
            dict(
                name='p3b',
                elements=[
                    dict(
                        type='text',
                        name='party_identification_text',
                        title='If yes, which one?',
                        visibleIf="{party_identification} = 'Yes'",
                        isRequired=True,
                    )
                ],
            ),
            dict(
                name='q1',
                elements=[
                    dict(
                        type='radiogroup',
                        name='attention_check',
                        title='Q1. Attention check: To show you are paying attention, please select option 3 for this question.',
                        isRequired=True,
                        choices=[str(i) for i in range(1, 8)],
                    )
                ],
            ),
            dict(
                name='q2',
                elements=[
                    dict(
                        type='radiogroup',
                        name='seriousness_check',
                        title='Q2. Did you answer the questions carefully and honestly?',
                        isRequired=True,
                        choices=C.YES_NO_PNS,
                    )
                ],
            ),
            dict(
                name='s1',
                elements=[
                    dict(
                        type='radiogroup',
                        name='prediction_strategy',
                        title='S1. How did you make your predictions about the average participant?',
                        isRequired=True,
                        choices=C.STRATEGY_CHOICES,
                    )
                ],
            ),
            dict(
                name='s1b',
                elements=[
                    dict(
                        type='comment',
                        name='prediction_strategy_other',
                        title='If "Other", please specify',
                        visibleIf="{prediction_strategy} = 'Other'",
                        isRequired=True,
                    )
                ],
            ),
            dict(
                name='f1',
                elements=[
                    dict(
                        type='comment',
                        name='comments',
                        title='F1. Any comments about the study? (optional)',
                    )
                ],
            ),
        ],
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
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def error_message(player: Player, values):
        if not all(values.values()):
            return 'You must tick all consent boxes to continue.'


class Instructions(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class MovieSurvey(SurveyJSPage):
    @staticmethod
    def vars_for_template(player: Player):
        movie = C.MOVIES[player.round_number - 1]
        return dict(
            movie=movie,
            movie_number=player.round_number,
            total_movies=C.NUM_ROUNDS,
            movie_image_url=f"/static/{movie['image']}",
        )

    @staticmethod
    def js_vars(player: Player):
        return dict(survey_json=build_movie_survey_json())

    def process_survey_data(self, data):
        self.player.predicted_audience_group = int(data['predicted_audience_group'])
        self.player.predicted_audience_confidence = int(data['predicted_audience_confidence'])
        self.player.movie_political_vibe = int(data['movie_political_vibe'])
        self.player.movie_vibe_confidence = int(data['movie_vibe_confidence'])


class ExitQuestionnaire(SurveyJSPage):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def js_vars(player: Player):
        return dict(survey_json=build_exit_survey_json())

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
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS


page_sequence = [Consent, Instructions, MovieSurvey, ExitQuestionnaire, Completion]
