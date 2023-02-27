#!/usr/bin/env python3
import copy
import logging
import os
import pathlib
import sys
import typing

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


# Fix responses like \ "%1 $ S \" -> \"%1$s\"
# TODO(ashishb): Eventually replace this with RegEx
def _normalize_response(text: str) -> str:
    for i in range(1, 9):
        for ch in ["d", "D", "s", "S"]:
            text = text.replace(f"%{i} $ {ch}", f"%{i}${ch.lower()}")
            text = text.replace(f"% {i} $ {ch}", f"%{i}${ch.lower()}")
    text = text.replace('" ', '"')
    # text = text.replace(" \"", "\"")
    # text = text.replace(" \\\"", "\\\"")
    text = text.replace('\\ "', '\\"')
    text = text.replace("%D", "%d")
    text = text.replace("%S", "%s")
    # Replace Chinese % sign with standard English one or "%d" and "%s" won't work
    text = text.replace("％", "%")
    text = text.replace("...", "…")
    text = text.replace(" …", "…")
    return text


def _translate(
    strings: typing.Dict[str, ET.Element],
    target_lang: str,
    translated_string_xml_file: str,
):
    if target_lang == "zh-rTW":
        target_lang = "zh-TW"
    # Not supported
    if target_lang == "pt-rBR":
        logging.warning("Not supported: '%s'", target_lang)
        return
    logging.info("Translating into '%s'...", translated_string_xml_file)
    translated_str = _get_strings_to_translate(translated_string_xml_file)
    translations_to_add: typing.Dict[str, ET.Element] = dict()
    num_translated = 0
    translate = googletrans.Translator()

    for k in strings:
        if translated_str.get(k, None) is not None:
            continue
        logging.debug("Requires translation in '%s' -> '%s'", target_lang, k)
        num_translated += 1
        try:
            translation = translate.translate(strings[k].text, dest=target_lang)
        except:
            logging.error("Failed to translate")
            continue
        element = copy.deepcopy(strings[k])
        element.text = _normalize_response(translation.text)
        translations_to_add[k] = element

    logging.info(
        "Translated %d strings to (%s, %s)",
        num_translated,
        target_lang,
        translated_string_xml_file,
    )
    if num_translated == 0:
        return

    xml_tree = ET.parse(translated_string_xml_file)
    qualified_strings_root = xml_tree.getroot()
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
