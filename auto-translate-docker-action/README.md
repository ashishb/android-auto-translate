# Auto Translator Action

This GitHub Action auto-translates Android's strings.xml and 
fills in the missing translations in all other languages.

To use this for a new language, say "hi", first create "values-hi/strings.xml" empty file
and then run this action

```yaml
  - name: Translate strings.xml to supported languages
    uses: ashishb/auto-translate-docker-action
```