# inventree-app-i18n

Translation files for the InvenTree mobile app.

This repository contains translation files for the InvenTree mobile app (Android / iOS)

## Translating

To enter new translation strings, use the included python script:

e.g. the following command:

```
python translate.py de
```

will allow you to enter translation strings step-by-step.

### Editing Translations

To update / edit / overrite an existing translation, the corresponding `.arb` file needs to be manually edited.

### Stats

To see translation statistics for a particular locale:

```
python translate.py fr --stats
```