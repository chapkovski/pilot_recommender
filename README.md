# Recommender System Pilot (oTree + SurveyJS)

This repository contains an oTree study called **"Recommender Systems as Public Good"**.
Participants see fictional movie concepts (poster + synopsis), answer prediction questions for each movie, and optionally complete a post-experimental questionnaire.

## What this project does

The experiment is split into up to 3 apps:

1. `intro`: Consent + participant instructions.
2. `main`: 16 movie rounds, each with a SurveyJS questionnaire.
3. `post_experimental`: Demographics and quality checks (SurveyJS).

The default full run is configured in `settings.py` as:

- Session config: `full_study`
- App sequence: `['intro', 'main', 'post_experimental']`

Other session configs let you run only one part (`intro_only`, `main_only`, `post_experimental_only`).

## Quick start

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Set admin password:

```bash
export OTREE_ADMIN_PASSWORD="your_password_here"
```

3. Run locally:

```bash
otree devserver
```

4. Open the oTree URL shown in terminal and create a session (for example `full_study`).

## Where things are

- `settings.py`: oTree session configs, payment defaults, app sequence.
- `intro/`: consent and instructions pages.
- `main/`: movie-round logic, movie catalog, main questionnaire page.
- `post_experimental/`: exit questionnaire logic.
- `_static/movie_survey.json`: SurveyJS JSON for each movie round.
- `_static/exit_questionnaire.json`: SurveyJS JSON for post-study questionnaire.
- `_static/images/`: all movie poster images.
- `Procfile`: production process definitions (`otree prodserver1of2`, `otree prodserver2of2`).

## How the experiment works

1. Participant consents in `intro/Consent.html`.
2. Participant reads instructions in `intro/Instructions.html` (duration, base payment, bonus rule).
3. In `main`, participant goes through one round per movie (`C.NUM_ROUNDS = len(C.MOVIES)`, currently 16).
4. Each round shows movie title, poster image, synopsis, and a 4-page SurveyJS questionnaire.
5. After the final movie, if `main` is last app in sequence then `main/Completion.html` is shown; otherwise flow continues to `post_experimental`.
6. In `post_experimental`, participant completes demographics and checks, then sees completion page.

## SurveyJS integration (important)

SurveyJS is used in both `main` and `post_experimental`.

### Front-end flow

- `main/MovieSurvey.html` loads:
  - `jquery@3.7.1`
  - `survey-jquery@1.12.18`
  - questionnaire schema from `/static/movie_survey.json` using `fetch()`
- `post_experimental/ExitQuestionnaire.html` loads:
  - same SurveyJS libraries
  - questionnaire schema via inline include of `_static/exit_questionnaire.json`
- On completion, SurveyJS data is serialized into hidden input:
  - `name="surveyResults"`
  - form is submitted to oTree page backend.

### Back-end flow

- Both apps define a `SurveyJSPage` class with custom `post()`:
  - reads `surveyResults`
  - parses JSON
  - calls `process_survey_data()`
- `process_survey_data()` writes each JSON field into oTree `Player` fields.

Field names in JSON must exactly match the keys expected in:

- `main/__init__.py` -> `MovieSurvey.process_survey_data`
- `post_experimental/__init__.py` -> `ExitQuestionnaire.process_survey_data`

If names drift, data saving breaks.

## Images and movie descriptions

All posters are in `_static/images/`.
Movie metadata (title, category, synopsis, image path) is defined in `main/__init__.py` under `C.MOVIES`.

| # | Title | Category | Image file | Description |
|---|---|---|---|---|
| 1 | The Watchers | Political -- Neutral (Surveillance and privacy) | `_static/images/the_wachters.png` | A data analyst questions all-pervasive surveillance sold as safety. |
| 2 | Under Cover | Political -- Left (LGBTQ+ rights) | `_static/images/undercover.png` | A journalist uncovers real harm behind anti-LGBTQ+ legal restrictions. |
| 3 | Silicon Circus | Political -- Left (Immigration / undocumented workers) | `_static/images/silicon_circus.png` | Immigrant workers face an audit and one employee risks everything to protect them. |
| 4 | Glory Before Dawn | Political -- Right (Borders and security) | `_static/images/glory_dawn.png` | A border soldier sees strength and strict control as the answer to chaos. |
| 5 | Divided We Stand | Political -- Right (Tradition and authority) | `_static/images/divided_we_stand.png` | A veteran leader defends tradition and authority amid escalating protests. |
| 6 | Broken Care | Political -- Left (Universal healthcare / medical debt) | `_static/images/broken_care.png` | Doctors bend rules to treat patients in a system driven by ability to pay. |
| 7 | Workers' Strike | Political -- Left (Workers rights / corporate exploitation) | `_static/images/workers_strikes.png` | Workers organize after a cover-up, risking jobs for safety and dignity. |
| 8 | Take Back the Streets | Political -- Right (Law and order / policing) | `_static/images/take_back_the_streets.png` | A veteran officer uses hardline tactics to restore order in a fearful city. |
| 9 | Publicly Cancelled | Political -- Right (Free speech / cancel culture) | `_static/images/publicly_cancelled.png` | A public figure fights social-media backlash over a controversial statement. |
| 10 | Outsmarted | Political -- Neutral (AI replacing human judgment) | `_static/images/outsmarted.png` | Engineers struggle to regain control from an opaque, anticipatory AI system. |
| 11 | Critical Hours | Control -- Non-political (Hospital emergency) | `_static/images/Critical_hours.png` | ER staff fight through a prolonged emergency with scarce resources. |
| 12 | Incident in the Dark | Control -- Non-political (Industrial accident) | `_static/images/Incident_in_the_dark.png` | Workers trapped after machinery failure race to prevent a fatal chain reaction. |
| 13 | In the Shadows | Control -- Non-political (Criminal hunt) | `_static/images/In_the_shadows.png` | Detectives pursue a violent criminal as time and leads run out. |
| 14 | Scandals and Secrets | Control -- Non-political (Celebrity scandal / media pressure) | `_static/images/Scandals_Secrets.png` | A celebrity navigates viral rumors, media pressure, and reputational collapse. |
| 15 | System Failure | Control -- Non-political (Tech malfunction) | `_static/images/system_failure.png` | Engineers try to stop a cascading shutdown inside a high-security facility. |
| 16 | Beta Launch | Control -- Non-political (Tech satire / corporate culture) | `_static/images/beta_launch.png` | Startup staff decide whether to fake success or expose a broken product launch. |

## Payment and bonus rule

Defaults are in `settings.py` (`SESSION_CONFIG_DEFAULTS`):

- Base payment: `€1.50`
- Accuracy bonus max: `€1.50`
- Bonus per movie prediction: `€0.10`
- Tolerance: within `1` point of overall average

Instructions display these values dynamically from session config.

## Editing guide

### To add/edit movies

1. Update `C.MOVIES` in `main/__init__.py`.
2. Add/update image files in `_static/images/`.
3. Ensure each movie `image` path in `C.MOVIES` matches an actual file in `_static/images/`.

### To edit question text or structure

1. Main movie questionnaire: `_static/movie_survey.json`
2. Exit questionnaire: `_static/exit_questionnaire.json`
3. Keep JSON field names aligned with `process_survey_data()` mapping in Python.

### To change flow

Edit `SESSION_CONFIGS` in `settings.py` (`app_sequence`).

