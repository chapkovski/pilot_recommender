# Copilot instructions

## Project overview
- This is an oTree 5 app with a single app module: `main` (see [main/__init__.py](main/__init__.py)).
- Session config is defined in [settings.py](settings.py): session name `recommender_system` runs `app_sequence=['main']`.
- Static assets live under [_static/](./_static/) and templates reference posters via `/static/...` (see movie cards in [main/MovieSurvey.html](main/MovieSurvey.html)).

## Core flow & data model
- The study is round-based: `C.MOVIES` defines the stimuli, and `C.NUM_ROUNDS = len(C.MOVIES)` drives the number of rounds.
- Page order is `Consent → Instructions → MovieSurvey (every round) → ExitQuestionnaire (last round) → Completion` (see `page_sequence` in [main/__init__.py](main/__init__.py)).
- `Player` fields store consent, per-movie answers, and exit questionnaire data (all in [main/__init__.py](main/__init__.py)).

## SurveyJS integration pattern (important)
- `MovieSurvey` and `ExitQuestionnaire` are SurveyJS-driven pages.
- JSON schemas are built in Python via `build_movie_survey_json()` / `build_exit_survey_json()` and exposed via `js_vars`.
- Templates load SurveyJS from CDN and submit a hidden `surveyResults` field; parsing happens in `SurveyJSPage.post()`.
- Always update both the JSON builder **and** `process_survey_data()` when adding/removing survey questions.

## Templates & styling
- Templates are in [main/](main/) and use oTree blocks (`title`, `content`, `styles`, `scripts`).
- SurveyJS styling overrides live in template `<style>` blocks (see [main/MovieSurvey.html](main/MovieSurvey.html)).

## External dependencies & runtime
- Dependencies are minimal and pinned in [requirements.txt](requirements.txt) (`otree>=5.0.0a21`, `psycopg2`).
- Production entry points are defined in [Procfile](Procfile) (`otree prodserver1of2` / `otree prodserver2of2`).
- Admin password is read from `OTREE_ADMIN_PASSWORD` (see [settings.py](settings.py)).

## Common edit points
- Adding/changing movies: update `C.MOVIES` and ensure poster files exist under [_static/images/](./_static/images/).
- Changing survey scales: update `C.*_SCALE` constants and the related SurveyJS JSON builders.
