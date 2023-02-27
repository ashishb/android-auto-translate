# android-auto-translate

[![Lint YAML](https://github.com/ashishb/android-auto-translate/actions/workflows/lint-yaml.yaml/badge.svg)](https://github.com/ashishb/android-auto-translate/actions/workflows/lint-yaml.yaml)
[![Lint Markdown](https://github.com/ashishb/android-auto-translate/actions/workflows/lint-markdown.yaml/badge.svg)](https://github.com/ashishb/android-auto-translate/actions/workflows/lint-markdown.yaml)
[![Lint Dockerfiles](https://github.com/ashishb/android-auto-translate/actions/workflows/lint-docker.yaml/badge.svg)](https://github.com/ashishb/android-auto-translate/actions/workflows/lint-docker.yaml)
[![Lint Python Code](https://github.com/ashishb/android-auto-translate/actions/workflows/lint-python.yaml/badge.svg)](https://github.com/ashishb/android-auto-translate/actions/workflows/lint-python.yaml)

[![Build Docker image](https://github.com/ashishb/android-auto-translate/actions/workflows/build-docker.yaml/badge.svg)](https://github.com/ashishb/android-auto-translate/actions/workflows/build-docker.yaml)

This GitHub Action auto-translates Android's strings.xml and
fills in the missing translations in all other languages.

To use this for a new language, say "es", first create "values-es/strings.xml" file with
the following placeholder content

```xml
<resources>
</resources>
```

and save the following to `.github/workflows/translate-android.yaml` in the repository.

```yaml
---
name: Automatically Translate Android App

on:  # yamllint disable-line rule:truthy
  pull_request:
    branches: ["master", "main"]
    paths:
      - "**/strings.xml"

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:

  # Run locally with "act -j translateAndroid"
  translateAndroid:

    runs-on: ubuntu-latest
    timeout-minutes: 15

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v3

      - name: Translate strings.xml to supported languages
        uses: ashishb/android-auto-translate@v0.5

      - uses: stefanzweifel/git-auto-commit-action@v4
        with:
          commit_message: Add automatically generated translations
          commit_user_name: "ashishb's Translation Bot"
```
