# Contributing to EMA References

Thanks for taking the time to look at this project. The app is a single-file Streamlit tool for organising the bibliography behind an HTW Berlin M8 course presentation. Contributions are welcome — within the scope set out below.

## What we welcome

- Bug fixes anywhere in the Streamlit flow
- Accessibility improvements (focus order, keyboard navigation, contrast)
- Better search (e.g. tokenised matching across `title`, `description`, `type`, `url`)
- Roadmap items: pytest smoke suite, citation export (BibTeX / RIS), tag-based filtering, admin role beyond a single shared password
- Documentation improvements

## What we won't merge

- A real admin password committed to source. **The previous `admin123` literal is permanently considered compromised** — see [security](#security) below.
- New runtime dependencies without a clear rationale (`requirements.txt` is intentionally tight)
- Tracking, telemetry, or any third-party network call that isn't disclosed to the user

## Workflow

1. **Open an issue first** for anything larger than a typo or a one-line fix, so we can confirm scope.
2. Fork the repository and create a topic branch:
   ```bash
   git checkout -b fix/short-description
   ```
3. Install and run locally:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate              # Windows
   # source .venv/bin/activate         # macOS / Linux
   pip install -r requirements.txt
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   # set ADMIN_PASSWORD inside .streamlit/secrets.toml
   streamlit run app.py
   ```
4. Walk through the flow:
   - Browse references → confirm search filter
   - Admin login → add a reference → edit it → delete it
   - Backup → download JSON → restore from JSON
5. Commit with a clear message (imperative mood, e.g. `Add tag filter to references list`).
6. Open a pull request against `main` describing **what changed and why**, with screenshots if the change is visual.

## Coding style

- Python 3.10+
- One file for now (`app.py`). If we split, the helpers go in `lib/`, the Streamlit views stay in `app.py`. Discuss in an issue first.
- No global mutable state outside `st.session_state`.
- Use `st.secrets` for credentials and external API keys — never inline.

## Security

This is a public repository. Treat anything you commit as published.

- **Never** put a real `ADMIN_PASSWORD`, API key, or token in source, in an issue, or in a PR description.
- `.streamlit/secrets.toml` is gitignored. The `.streamlit/secrets.toml.example` template ships with a `change-me-...` placeholder and is the only safe file to commit.
- If you accidentally commit a credential, **rotate it immediately** on Streamlit Cloud (App settings → Secrets) — pushing a force-push to remove the file from history does NOT undo the leak; assume any committed value is permanently compromised.

## Reporting issues

Please include:

- Streamlit version
- Python version
- Steps to reproduce
- Expected vs. actual behaviour
- Screenshot if the issue is visual
- Console / browser-console errors (strip any secrets)

## Code of conduct

Be kind, be specific, assume good faith. Disagreement on technical decisions is welcome; personal attacks are not.

## License

By contributing, you agree that your contributions are licensed under the [MIT License](LICENSE) covering this repository.
