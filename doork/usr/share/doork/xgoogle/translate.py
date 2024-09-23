#!/usr/bin/python
#
# Peteris Krumins (peter@catonmat.net)
# http://www.catonmat.net  --  good coders code, great reuse
#
# http://www.catonmat.net/blog/python-library-for-google-translate/
#
# Code is licensed under MIT license.
#

from browser import Browser, BrowserError
from urllib import quote_plus

try:    import json
except: import simplejson as json


class TranslationError(Exception):
    pass

class Translator(object):
    translate_url = "http://ajax.googleapis.com/ajax/services/language/translate?v=1.0&q=%(message)s&langpair=%(from)s%%7C%(to)s"

    def __init__(self):
        self.browser = Browser()

    def translate(self, message, lang_to='en', lang_from=''):
        """
        Given a 'message' translate it from 'lang_from' to 'lang_to'.
        If 'lang_from' is empty, auto-detects the language.
        Returns the translated message.
        """

        if lang_to not in _languages:
            raise TranslationError, "Language %s is not supported as lang_to." % lang_to
        if lang_from not in _languages and lang_from != '':
            raise TranslationError, "Language %s is not supported as lang_from." % lang_from

        message = quote_plus(message)
        real_url = Translator.translate_url % { 'message': message,
                                                'from':    lang_from,
                                                'to':      lang_to }

        try:
            translation = self.browser.get_page(real_url)
            data = json.loads(translation)

            if data['responseStatus'] != 200:
                raise TranslationError, "Failed translating: %s" % data['responseDetails']

            return data['responseData']['translatedText']
        except BrowserError, e:
            raise TranslationError, "Failed translating (getting %s failed): %s" % (e.url, e.error)
        except ValueError, e:
            raise TranslationError, "Failed translating (json failed): %s" % e.message
        except KeyError, e:
            raise TranslationError, "Failed translating, response didn't contain the translation"

        return None

class DetectionError(Exception):
    pass

class Language(object):
    def __init__(self, lang, confidence, is_reliable):
        self.lang_code = lang
        self.lang = _languages[lang]
        self.confidence = confidence
        self.is_reliable = is_reliable

    def __repr__(self):
        return '<Language: %s (%s)>' % (self.lang_code, self.lang)

class LanguageDetector(object):
    detect_url = "http://ajax.googleapis.com/ajax/services/language/detect?v=1.0&q=%(message)s"

    def __init__(self):
        self.browser = Browser()

    def detect(self, message):
        """
        Given a 'message' detects its language.
        Returns Language object.
        """

        message = quote_plus(message)
        real_url = LanguageDetector.detect_url % { 'message': message }

        try:
            detection = self.browser.get_page(real_url)
            data = json.loads(detection)

            if data['responseStatus'] != 200:
                raise DetectionError, "Failed detecting language: %s" % data['responseDetails']

            rd = data['responseData']
            return Language(rd['language'], rd['confidence'], rd['isReliable'])

        except BrowserError, e:
            raise DetectionError, "Failed detecting language (getting %s failed): %s" % (e.url, e.error)
        except ValueError, e:
            raise DetectionErrro, "Failed detecting language (json failed): %s" % e.message
        except KeyError, e:
            raise DetectionError, "Failed detecting language, response didn't contain the necessary data"

        return None


_languages = {
  'af': 'Afrikaans',
  'sq': 'Albanian',
  'am': 'Amharic',
  'ar': 'Arabic',
  'hy': 'Armenian',
  'az': 'Azerbaijani',
  'eu': 'Basque',
  'be': 'Belarusian',
  'bn': 'Bengali',
  'bh': 'Bihari',
  'bg': 'Bulgarian',
  'my': 'Burmese',
  'ca': 'Catalan',
  'chr': 'Cherokee',
  'zh': 'Chinese',
  'zh-CN': 'Chinese_simplified',
  'zh-TW': 'Chinese_traditional',
  'hr': 'Croatian',
  'cs': 'Czech',
  'da': 'Danish',
  'dv': 'Dhivehi',
  'nl': 'Dutch',
  'en': 'English',
  'eo': 'Esperanto',
  'et': 'Estonian',
  'tl': 'Filipino',
  'fi': 'Finnish',
  'fr': 'French',
  'gl': 'Galician',
  'ka': 'Georgian',
  'de': 'German',
  'el': 'Greek',
  'gn': 'Guarani',
  'gu': 'Gujarati',
  'iw': 'Hebrew',
  'hi': 'Hindi',
  'hu': 'Hungarian',
  'is': 'Icelandic',
  'id': 'Indonesian',
  'iu': 'Inuktitut',
  'ga': 'Irish',
  'it': 'Italian',
  'ja': 'Japanese',
  'kn': 'Kannada',
  'kk': 'Kazakh',
  'km': 'Khmer',
  'ko': 'Korean',
  'ku': 'Kurdish',
  'ky': 'Kyrgyz',
  'lo': 'Laothian',
  'lv': 'Latvian',
  'lt': 'Lithuanian',
  'mk': 'Macedonian',
  'ms': 'Malay',
  'ml': 'Malayalam',
  'mt': 'Maltese',
  'mr': 'Marathi',
  'mn': 'Mongolian',
  'ne': 'Nepali',
  'no': 'Norwegian',
  'or': 'Oriya',
  'ps': 'Pashto',
  'fa': 'Persian',
  'pl': 'Polish',
  'pt-PT': 'Portuguese',
  'pa': 'Punjabi',
  'ro': 'Romanian',
  'ru': 'Russian',
  'sa': 'Sanskrit',
  'sr': 'Serbian',
  'sd': 'Sindhi',
  'si': 'Sinhalese',
  'sk': 'Slovak',
  'sl': 'Slovenian',
  'es': 'Spanish',
  'sw': 'Swahili',
  'sv': 'Swedish',
  'tg': 'Tajik',
  'ta': 'Tamil',
  'tl': 'Tagalog',
  'te': 'Telugu',
  'th': 'Thai',
  'bo': 'Tibetan',
  'tr': 'Turkish',
  'uk': 'Ukrainian',
  'ur': 'Urdu',
  'uz': 'Uzbek',
  'ug': 'Uighur',
  'vi': 'Vietnamese',
  'cy': 'Welsh',
  'yi': 'Yiddish'
};

