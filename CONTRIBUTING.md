# Contributing to Plus AI ROI Simulator

Thank you for your interest in improving the Plus AI Enterprise ROI & Deployment Simulator. This repository is a public Streamlit prototype focused on clear enterprise value modeling, deployment planning, and presentation-governance demonstrations.

## Before you contribute

- Review the [README](README.md) for the product scope and local setup.
- Search existing issues before opening a new one.
- Keep proposals focused on clear user value, accuracy, accessibility, or maintainability.
- Do not include client data, confidential business information, credentials, API keys, or personal information in issues, pull requests, screenshots, or exported files.

## Local setup

```bash
git clone https://github.com/FriesRdBest/plus-slop-stopper.git
cd plus-slop-stopper
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

On Windows PowerShell, activate the virtual environment with:

```powershell
.venv\Scripts\Activate.ps1
```

## Contribution guidelines

1. Create a branch from `main`.
2. Make one focused change at a time.
3. Preserve the ROI formulas unless the issue explicitly concerns model methodology.
4. Run the app locally and exercise the affected workflow.
5. Check formatting and syntax before opening a pull request:

```bash
python -m py_compile app.py
git diff --check
```

6. In your pull request, explain the problem, the change, validation performed, and any user-facing impact.

## Design principles

- Keep the simulator understandable for non-technical stakeholders.
- Prefer clear decision support over decorative complexity.
- Preserve responsive behavior across desktop, tablet, and mobile widths.
- Maintain the light executive glass visual language.
- Treat exported summaries as stakeholder-facing documents.

## Reporting issues

Use the repository issue templates for bugs and feature requests. For security concerns, follow [SECURITY.md](SECURITY.md) instead of opening a public issue.

## License

By contributing, you agree that your contributions will be licensed under the [Apache License 2.0](LICENSE).
