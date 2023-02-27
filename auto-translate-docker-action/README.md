# Auto Translator Action

This GitHub Action auto-translates Android's strings.xml and
fills in the missing translations in all other languages.

To use this for a new language, say "hi", first create "values-hi/strings.xml" empty file
and then run this action

```yaml
  - name: Translate strings.xml to supported languages
    uses: ashishb/android-auto-translate@v0.1

  - uses: stefanzweifel/git-auto-commit-action@v4
    with:
      commit_message: Adds Translations
      commit_user_name: "ashishb's Translation Bot"
```
