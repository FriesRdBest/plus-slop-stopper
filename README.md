# Plus AI Enterprise ROI & Deployment Simulator

A public Streamlit prototype for modeling the enterprise capacity and productivity value created when teams reduce manual presentation-formatting work through governed AI workflows.

The simulator turns a few operating assumptions—creator count, deck volume, manual formatting time, and labor rate—into a clear executive view of annual value, reclaimed capacity, deployment readiness, and a practical 30/60/90-day rollout path.

## What it demonstrates

- **Executive ROI modeling** — Estimate annual reclaimed hours and productivity value from current workflow assumptions.
- **Scenario presets** — Start from a Pilot, Department rollout, or Enterprise rollout model, then tune assumptions live.
- **Client-ready context** — Optionally add a client or company name to personalize the working scenario and export.
- **Interactive value ramp** — Explore cumulative financial value and reclaimed-capacity curves over 12 months.
- **Deployment planning** — See a tier-responsive 30/60/90-day rollout journey based on brand and template complexity.
- **Slide Slop Linter** — Compare uncontrolled presentation output with governed layout, typography, and safe-margin rules.
- **Executive PDF export** — Download a one-page summary of the active scenario, milestones, rollout posture, and calculation method.
- **Glossary** — Search the operational, financial, and presentation-governance terminology used by the simulator.

## Public demo guidance

This is a public demonstration application. Use sanitized, fictional, or representative assumptions only. Do not enter client-confidential information, personal information, credentials, API keys, or sensitive production financial data.

## Run locally

### Requirements

- Python 3.10 or later
- `pip`

### Setup

```bash
git clone https://github.com/FriesRdBest/plus-slop-stopper.git
cd plus-slop-stopper
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Streamlit will provide a local URL, normally `http://localhost:8501`.

## Core calculation model

The simulator applies a modeled 65% reduction in manual formatting time:

```text
Monthly deck volume = active slide creators × average decks per user per month
Monthly hours reclaimed = monthly deck volume × manual formatting hours per deck × 65%
Annual hours reclaimed = monthly hours reclaimed × 12
Annual value delivered = annual hours reclaimed × average worker hourly rate
```

The model is intended for strategic scenario planning. It is not a substitute for a validated financial forecast, implementation estimate, or client-specific benefits case.

## Repository structure

```text
.
├── app.py                 # Streamlit application
├── requirements.txt       # Runtime dependencies
├── .github/               # Issue, pull-request, and Dependabot configuration
├── CONTRIBUTING.md        # Contribution guidance
├── CODE_OF_CONDUCT.md     # Community standards
├── SECURITY.md            # Security reporting and public-demo policy
└── LICENSE                # Apache License 2.0
```

## Contributing

Contributions and focused feedback are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) and follow the [Code of Conduct](CODE_OF_CONDUCT.md) before opening an issue or pull request.

For security concerns, do not open a public issue; follow [SECURITY.md](SECURITY.md).

## License

Copyright 2026 Robin Sylvester.

Licensed under the [Apache License, Version 2.0](LICENSE).
