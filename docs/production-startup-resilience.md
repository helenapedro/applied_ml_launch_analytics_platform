# Production Startup Resilience

## Incident Summary

On 2026-06-29, the Heroku web dyno crashed during Gunicorn startup because the app called the live SpaceX API while importing modules. The SpaceX API returned HTTP 525 responses from Heroku. The fetch helper returned `None`, and startup crashed when `fetch_and_process_data()` tried to iterate over that `None` value.

The visible symptom was:

```text
Reason: Worker failed to boot.
TypeError: 'NoneType' object is not iterable
```

## Prevention Rules

1. Keep imports side-effect free.
   Modules should define functions, classes, constants, and callbacks. They should not call external APIs, databases, scrapers, or long-running processing during import.

2. Never require third-party services for worker boot.
   Gunicorn must be able to import `app:server` even if external APIs are down, slow, or returning invalid responses.

3. Add timeouts to every network call.
   All `requests.get()` calls should include an explicit timeout so workers cannot hang indefinitely.

4. Fail soft for optional data.
   External data helpers should return cached data, empty schema-compatible DataFrames, or a visible "data unavailable" state instead of raising during startup.

5. Prefer cached snapshots for portfolio/demo data.
   For datasets that do not need real-time freshness, commit a known-good snapshot and refresh it through a separate script or scheduled job.

6. Run a startup smoke test before deploy.
   A deploy should fail if `app:server` cannot be imported.

7. Pin the Python major version.
   Heroku uses `.python-version`. Keep this file committed so runtime changes do not surprise production.

## Local Checks

After installing dependencies, run:

```bash
python scripts/smoke_import.py
python -m unittest discover -s tests
```

The smoke script verifies that the WSGI entrypoint imports successfully. The regression test verifies that failed SpaceX API calls return empty DataFrames with the columns the UI expects.

## Deployment Check

After a Heroku deploy, confirm the app boots and responds:

```bash
heroku logs --app rocket-launch-analysis --num 100
curl https://rocket-launch-analysis-5c3ea0d2902d.herokuapp.com/
```

Look for `State changed from starting to up` and an HTTP 200 response.
