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


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Per-movie questionnaire
    predicted_audience_group = models.IntegerField(
        label='If this movie were released today, which political group would you expect to like it more?',
        choices=C.AUDIENCE_LEANING_SCALE,
        widget=widgets.RadioSelect,
    )
    average_predicted_audience = models.IntegerField(
        label='How do you think an average participant would answer this question (the correct answer would increase your bonus): If this movie were released today, which political group would you expect to like it more?',
        choices=C.AUDIENCE_LEANING_SCALE,
        widget=widgets.RadioSelect,
    )
    movie_political_vibe = models.IntegerField(
        label='What political "vibe" does this movie concept give you?',
        choices=C.POLITICAL_VIBE_SCALE,
        widget=widgets.RadioSelect,
    )
    average_movie_vibe = models.IntegerField(
        label='How do you think an average participant would answer this question (the correct answer would increase your bonus): What political "vibe" does this movie concept give you?',
        choices=C.POLITICAL_VIBE_SCALE,
        widget=widgets.RadioSelect,
    )

# PAGES


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

    def process_survey_data(self, data):
        self.player.predicted_audience_group = int(data['predicted_audience_group'])
        self.player.average_predicted_audience = int(data['average_predicted_audience'])
        self.player.movie_political_vibe = int(data['movie_political_vibe'])
        self.player.average_movie_vibe = int(data['average_movie_vibe'])


class Completion(Page):
    @staticmethod
    def is_displayed(player: Player):
        return (
            player.round_number == C.NUM_ROUNDS
            and player.session.config['app_sequence'][-1] == C.NAME_IN_URL
        )


page_sequence = [MovieSurvey, Completion]
