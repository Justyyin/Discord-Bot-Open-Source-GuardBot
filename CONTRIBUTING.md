# Contributing

Bug reports, ideas and pull requests are welcome.

- Open an issue on GitHub or write to Discord: justyyin
- One topic per pull request, small commits with a clear message
- Do not commit tokens, `.env`, `settings.json` or the `data` folder
- Write a docstring for every module, class and function
- Do not ignore errors. Catch the specific exception, log it with `log.warning` or `log.exception`, and tell the user or the staff when the failure matters
- Run `python -m unittest` and `python -m pyflakes guardbot tests scripts main.py` before you open a pull request
- Features that need a live Discord server cannot be covered by the automated tests, so describe how you tried them
- New texts that members see go through `guardbot/i18n.py`: the English text is the key, add the translation to every file in `guardbot/locales/` (a test checks that all files are complete and keep the placeholders)
- New slash commands count against the limit of 100 per bot. Put related commands in a group instead of a new top-level command

## Releases

1. Add the entry at the top of `CHANGELOG.md` under `## <version>`
2. Set `__version__` in `guardbot/__init__.py` to the same version
3. Create and push the tag: `git tag v<version> && git push origin v<version>`

The release workflow checks that tag and version match, runs the tests, takes the notes from the changelog and publishes the release with a zip of the sources.
