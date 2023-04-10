#!/usr/bin/env python3
import copy
import logging
import os
import pathlib
import re
import sys
import typing
import time

import xml.etree.ElementTree as ET
import googletrans

_XML_ATTR_TRANSLATABLE = "translatable"
_XML_ATTR_NAME = "name"


def _get_english_string_files(base_dir: str) -> [str]:
    return list(pathlib.Path(base_dir).glob("**/src/*/res/values/strings.xml"))


def _get_strings_to_translate(source_path: str) -> typing.Dict[str, ET.Element]:
    source_strings = dict()
    logging.debug("Input string file is %s", source_path)
    source_tree = ET.parse(source_path)
    for child in source_tree.getroot():
        # Respect translatable attribute
        if child.attrib.get(_XML_ATTR_TRANSLATABLE) == "false":
            continue
        # Add this child to our dict where key is the name attribute
        source_strings[child.attrib.get(_XML_ATTR_NAME)] = child
    return source_strings


def _get_target_languages(res_dir: str) -> typing.Dict[str, str]:
    # Map of language code -> strings.xml file
    result: typing.Dict[str, str] = {}
    for path in pathlib.Path(res_dir).glob("**/values-*"):
        strings_path = os.path.join(path, "strings.xml")
        if not os.path.exists(strings_path):
            continue
        lang_code = path.name.replace("values-", "")
        result[lang_code] = strings_path
        logging.debug('Target language is "%s" -> "%s"', lang_code, strings_path)
    return result


def _normalize_response(text: str) -> str:
    text = text.replace("$、d", "$d")
    text = text.replace("$、s", "$s")
    # Replace Chinese % sign with standard English one or "%d" and "%s" won't work
    text = text.replace("％", "%")
    # Replace Arabic % sign with standard English one or "%d" and "%s" won't work
    text = text.replace("٪", "%")
    # Fix responses like \ "%1 $ S \" -> \"%1$s\"
    pattern = r'%\s*([\d*])\s*\$(,?)\s*([sdfSDF])'
    text = re.sub(pattern, r'%\1$\2\3', text)
    # Fix responses like %4 $ .1f -> %4$.1f
    pattern = r'%\s*([\d*])\s*\$(,?)\s*(\d*\.\d+)([fF])'
    text = re.sub(pattern, r'%\1$\2\3\4', text)
    # Remove extraneous spaces just before or after double-quotes
    # TODO(ashishb): If there are multiple pair of quotes then this
    # regex won't handle that properly and might remove more whitespace
    # than necessary
    text = re.sub(r'\"\s*(.*?)\s*\"', r'"\1"', text)
    text = re.sub(r'\(\s*(.*?)\s*\)', r'(\1)', text)
    # Replace unescaped quotes
    text = re.sub(r"([^\\])'", r"\1\'", text)

    text = text.replace('" ', '"')
    # text = text.replace(" \"", "\"")
    # text = text.replace(" \\\"", "\\\"")
    text = text.replace(r'\ "', r'\"')

    text = text.replace("%D", "%d")
    text = text.replace("%S", "%s")
    text = text.replace("$D", "$d")
    text = text.replace("$S", "$s")
    text = text.replace("d/ %", "d/%")
    text = text.replace("$,S", "$,s")
    text = text.replace("$,D", "$,d")
    text = text.replace("f/ %", "f/%")
    text = text.replace("...", "…")
    text = text.replace(" …", "…")
    text = text.replace("“", "\"")
    text = text.replace("”", "\"")
    # TODO: escape apostrophe as well
    return text


def _translate(
    src_strings: typing.Dict[str, ET.Element],
    target_lang: str,
    translated_string_xml_file: str,
):
    # See the full list of language codes here
    # https://py-googletrans.readthedocs.io/en/latest/#googletrans-languages
    if target_lang == "zh-rTW":
        target_lang = "zh-TW"
    # Use "Portuguese for "pt-rBR"
    if target_lang == "pt-rBR":
        target_lang = "pt"
    logging.info("Translating into '%s'...", translated_string_xml_file)
    translated_strings = _get_strings_to_translate(translated_string_xml_file)
    translations_to_add: typing.Dict[str, ET.Element] = dict()
    num_translated = 0
    translator = googletrans.Translator()

    # Strings that have been translated but are no longer part of the main
    # file
    translations_to_remove = list(
        filter(lambda x: x not in src_strings, translated_strings)
    )
    logging.info(
        '%d strings will be removed from %s',
        len(translations_to_remove),
        translated_string_xml_file,
    )

    for k in src_strings:
        if translated_strings.get(k, None) is not None:
            continue
        logging.debug("Requires translation in '%s' -> '%s'", target_lang, k)
        num_translated += 1
        try:
            translation = translator.translate(src_strings[k].text, dest=target_lang)
            if num_translated > 1:
                time.sleep(0.7)
        except Exception as e:
            logging.error(
                "Failed to translate '%s' to '%s': %s"
                % (src_strings[k].text, target_lang, e)
            )
            continue
        element = copy.deepcopy(src_strings[k])
        element.text = _normalize_response(translation.text)
        translations_to_add[k] = element
        if num_translated % 10 == 0:
            logging.info("Num translated: %d/%d", num_translated, len(src_strings))

    logging.info(
        "Translated %d strings to (%s, %s)",
        num_translated,
        target_lang,
        translated_string_xml_file,
    )
    if num_translated == 0 and len(translations_to_remove) == 0:
        return

    xml_tree = ET.parse(translated_string_xml_file)
    qualified_strings_root = xml_tree.getroot()
    for k in translations_to_remove:
        for qualified_string in qualified_strings_root:
            if qualified_string.attrib.get(_XML_ATTR_NAME) == k:
                qualified_strings_root.remove(qualified_string)
    for k in translations_to_add:
        qualified_strings_root.append(translations_to_add[k])
    logging.info("Writing changes to '%s'", translated_string_xml_file)
    xml_tree.write(
        translated_string_xml_file, encoding="utf-8", xml_declaration=True, method="xml"
    )


# Note: some of the code in this file is inspired from a similar work referenced below that uses ChatGPT
# Ref: https://proandroiddev.com/using-openais-text-completion-api-for-android-translations-80846e03b9cb


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    base_dir = os.getenv("GITHUB_WORKSPACE", ".")

    files = _get_english_string_files(base_dir=base_dir)
    if len(files) == 0:
        logging.error("No strings.xml found")
        exit(1)
    for file in files:
        strings_to_translate = _get_strings_to_translate(file)
        # for k in strings_to_translate:
        #     logging.debug("%s -> \"%s\"", k, strings_to_translate[k].text)

        target_lang_and_files = _get_target_languages(file.parent.parent)
        for target_lang in target_lang_and_files:
            _translate(
                strings_to_translate, target_lang, target_lang_and_files[target_lang]
            )


if __name__ == "__main__":
    main()
