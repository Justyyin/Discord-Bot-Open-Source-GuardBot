# Contributing

Bug reports, ideas and pull requests are welcome.

- Open an issue on GitHub or write to Discord: justyyin
- One topic per pull request, small commits with a clear message
- Do not commit tokens, `.env`, `settings.json` or the `data` folder
- Write a docstring for every module, class and function
- Do not ignore errors. Catch the specific exception, log it with `log.warning` or `log.exception`, and tell the user or the staff when the failure matters
- Run `python -m unittest` and `python -m pyflakes guardbot tests scripts main.py` before you open a pull request
- Features that need a live Discord server cannot be covered by the automated tests, so describe how you tried them
