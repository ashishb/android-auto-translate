# android-auto-translate

[![Lint YAML](https://github.com/ashishb/android-auto-translate/actions/workflows/lint-yaml.yaml/badge.svg)](https://github.com/ashishb/android-auto-translate/actions/workflows/lint-yaml.yaml)
[![Lint Markdown](https://github.com/ashishb/android-auto-translate/actions/workflows/lint-markdown.yaml/badge.svg)](https://github.com/ashishb/android-auto-translate/actions/workflows/lint-markdown.yaml)
[![Lint Dockerfiles](https://github.com/ashishb/android-auto-translate/actions/workflows/lint-docker.yaml/badge.svg)](https://github.com/ashishb/android-auto-translate/actions/workflows/lint-docker.yaml)
[![Lint Python Code](https://github.com/ashishb/android-auto-translate/actions/workflows/lint-python.yaml/badge.svg)](https://github.com/ashishb/android-auto-translate/actions/workflows/lint-python.yaml)

[![Test Python Code](https://github.com/ashishb/android-auto-translate/actions/workflows/test-python.yaml/badge.svg)](https://github.com/ashishb/android-auto-translate/actions/workflows/test-python.yaml)

[![Build Docker image](https://github.com/ashishb/android-auto-translate/actions/workflows/build-docker.yaml/badge.svg)](https://github.com/ashishb/android-auto-translate/actions/workflows/build-docker.yaml)

This GitHub Action auto-translates Android's `strings.xml` and
fills in the missing translations in all other languages.

It also deletes any translations that is no longer defined in default `strings.xml`.

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
  push:
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
        uses: ashishb/android-auto-translate@master

      - name: Create Pull Request
        uses: peter-evans/create-pull-request@v4
        with:
          committer: "ashishb's Translation Bot <ashishb+android-auto-translate@ashishb.net>"
          title: "[Bot]Auto-generated translations for non-English languages"
          body: "Auto-generated translations by [Android Auto Translate](https://github.com/ashishb/android-auto-translate) bot"
```

## How to run this locally

```bash
$ git clone https://github.com/ashishb/android-auto-translate
...
$ cd android-auto-translate
...
# Do note that this will modify strings.xml files in the specified
# Android dir, so, don't forget to back them up first
$ GITHUB_WORKSPACE=<path-to-android-base-dir> ./src/translations.py
```
