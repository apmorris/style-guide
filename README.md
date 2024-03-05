# The Guardian's style guide in Markdown

Python code to convert the [Guardian and Observer style guide](https://www.theguardian.com/guardian-observer-style-guide-a) to a Markdown file.

The code uses the Content API to download all style guide articles, converts the HTML to Markdown and creates a file called `style_guide.md`.

## How to run

You will need a Python environment. Set up using the Pipfile provided by running:
```bash
pipenv install
```

You will also need to have your [Content API](https://open-platform.theguardian.com/access/) key stored in an environment variable called `CAPI_KEY`. You can set this directly, or (if you are using pipenv) by creating a `.env` file with a line as follows
```bash
CAPI_KEY=your_key_here
```
which will be auto-loaded into the environment when pipenv is run.

To run the script, simply do:
```bash
pipenv run python style_guide.py
```
