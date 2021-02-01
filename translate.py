"""
This script is used to for entering translation data,
one entry at a time.
"""

import json
import argparse
import os


if __name__ == '__main__':

    MY_DIR = os.path.dirname(os.path.realpath(__file__))
    
    parser = argparse.ArgumentParser(description="InvenTree app translation helper")

    parser.add_argument('locale', help='Language code', action='store')

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

    locale = args.locale

    filename = f'app_{locale}.arb'

    locale_file = os.path.join(MY_DIR, filename)

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

    new_messages = 0

    for key in translation_keys:
        if key not in locale_data.keys():

            if first_message:
                first_message = False
                print("")
                print(f"Enter '{locale}' translation for each string,")
                print("or leave empty (press enter) to skip.")
                print("")
                print("Press Ctrl-C to exit")

            message = arb_data[key]

            try:
                translation = str(input(f"'{message}' > ")).strip()
            except KeyboardInterrupt:
                keyboard_exited = True
                break

            if len(translation) == 0:
                continue

            locale_data[key] = translation
            new_messages += 1

    if new_messages > 0:
        print(f"Added {new_messages} new translation strings")

        if not args.fake:
            with open(locale_file, 'w') as output:
                output.write(json.dumps(locale_data, indent=2))

    print("Done!")