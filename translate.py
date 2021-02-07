"""
This script is used to for entering translation data,
one entry at a time.
"""

import json
import argparse
import os


def manually_translate(locale, args):
    """
    Manually translate a single file
    """

    MY_DIR = os.path.dirname(os.path.realpath(__file__))
    
    locale_filename = f'app_{locale}.arb'

    locale_file = os.path.join(MY_DIR, locale_filename)

    # Create locale file if it does not exist
    if not os.path.exists(locale_file):
        print(f"Creating new file for locale '{locale}'")
        with open(locale_file, 'w') as f:

            data = {"@@locale": locale}

            f.write(json.dumps(data, indent=2))

    # Load all the keys from the target tile
    with open(locale_file, 'r') as f:

        locale_data = json.loads(f.read())

    keyboard_exited = False
    first_message = True

    total_keys = len(translation_keys)
    translated_keys = 0
    untranslated_keys = 0
    new_messages = 0

    # First extract total number of "untranslated" strings
    for key in translation_keys:
        if key not in locale_data.keys():
            untranslated_keys += 1
        else:
            translated_keys += 1

    if args.stats:
        if total_keys > 0:
                completion_percent = int(translated_keys / total_keys * 100)
        else:
            completion_percent = 0

        print(f"'{locale}' translations: {translated_keys} / {total_keys} ({completion_percent}%)")

        return

    # First, remove any extra keys in the target file, which do not exist in the template file
    keys = [k for k in locale_data.keys()]

    for key in keys:

        key = key.strip()

        if key.startswith('@'):
            continue

        if key not in translation_keys:
            print(f"Removing extra key '{key}'")
            del locale_data[key]

    print(f"Entering translations for '{locale_filename}'")

    for key in translation_keys:
        if key not in locale_data.keys():

            if first_message:
                first_message = False
                print("")
                print(f"Enter '{locale}' translation for each string,")
                print("or leave empty (press enter) to skip.")
                print("Press Ctrl-C to exit")
                print()

            message = arb_data[key]

            try:
                translation = str(input(f"@{key} - '{message}' > ")).strip()
            except KeyboardInterrupt:
                keyboard_exited = True
                break

            if len(translation) == 0:
                continue

            locale_data[key] = translation
            new_messages += 1
            translated_keys += 1

    print()

    if new_messages > 0:
        print(f"Added {new_messages} new translation strings")

    if not args.fake:
        with open(locale_file, 'w') as output:
            print(f"Writing results to '{locale_file}'")
            output.write(json.dumps(locale_data, indent=2))


if __name__ == '__main__':

    MY_DIR = os.path.dirname(os.path.realpath(__file__))
    
    parser = argparse.ArgumentParser(description="InvenTree app translation helper")

    parser.add_argument('locale', help='Language code', action='store')

    parser.add_argument('--stats', help='Show stats for specified locale', action='store_true')
    parser.add_argument('--fake', help='Do not store updated translations', action='store_true')

    args = parser.parse_args()

    base_locale_file = 'app_en.arb'

    if not os.path.exists(os.path.join(MY_DIR, base_locale_file)):
        print(f"Base locale file '{base_locale_file}' missing")
        sys.exit(1)

    base_locale_file = os.path.join(MY_DIR, base_locale_file)

    with open(base_locale_file, 'r') as arb_data_file:
        arb_data = json.loads(arb_data_file.read())

    translation_keys = []

    for key in arb_data.keys():

        key = key.strip()

        if len(key) == 0:
            continue

        if key.startswith('@'):
            continue

        translation_keys.append(key)

    # Sort alphabetically
    translation_keys = sorted(translation_keys)

    manually_translate(args.locale, args)
