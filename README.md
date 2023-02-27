# android-auto-translate

[![Lint YAML](https://github.com/ashishb/android-auto-translate/actions/workflows/lint-yaml.yaml/badge.svg)](https://github.com/ashishb/android-auto-translate/actions/workflows/lint-yaml.yaml)
[![Lint Markdown](https://github.com/ashishb/android-auto-translate/actions/workflows/lint-markdown.yaml/badge.svg)](https://github.com/ashishb/android-auto-translate/actions/workflows/lint-markdown.yaml)
[![Lint Dockerfiles](https://github.com/ashishb/android-auto-translate/actions/workflows/lint-docker.yaml/badge.svg)](https://github.com/ashishb/android-auto-translate/actions/workflows/lint-docker.yaml)
[![Lint Python Code](https://github.com/ashishb/android-auto-translate/actions/workflows/lint-python.yaml/badge.svg)](https://github.com/ashishb/android-auto-translate/actions/workflows/lint-python.yaml)

This GitHub Action auto-translates Android's strings.xml and
fills in the missing translations in all other languages.

To use this for a new language, say "hi", first create "values-hi/strings.xml" empty file
and then run this action.

```yaml
  - name: Translate strings.xml to supported languages
    uses: ashishb/android-auto-translate@v0.1

  - uses: stefanzweifel/git-auto-commit-action@v4
    with:
      commit_message: Adds Translations
      commit_user_name: "ashishb's Translation Bot"
```
