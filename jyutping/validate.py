import re

class Validator:
    def __init__(self, groups):
        self.groups = groups

    def test(self, test_set):
        return max(self.test_rule(rule_set) for rule_set in test_set.values())

    def test_rule(self, rule_set):
        for level, matchers in rule_set:
            if all(Validator.match(matcher, group) for matcher, group in zip(matchers, self.groups)):
                return level
        return ValidationStatus.VALID

    @staticmethod
    def match(matcher, group):
        return matcher is None or group in ['' if part == '-' else part for part in matcher.split(' ')]

class ValidationStatus:
    VALID = 0
    UNCOMMON = 1
    INVALID = 2

def validate(jyutping):
    '''
    >>> validate('jyut6')
    0  # ValidationStatus.VALID
    >>> validate('gwek6')
    1  # ValidationStatus.UNCOMMON
    >>> validate('nguk1')
    2  # ValidationStatus.INVALID
    '''
    match = re.match('^([gk]w?|ng|[bpmfdtnlhwzcsj]?)(?![1-6]$)(aa?|oe?|eo?|y?u|i?)(ng|[iumnptk]?)([1-6])$', jyutping)
    if match is None: return ValidationStatus.INVALID
    return validate_args(*match.groups())

def validate_args(*args):
    '''
    >>> validate('j', 'yu', 't', '6')
    0  # ValidationStatus.VALID
    >>> validate('gw', 'e', 'k', '6')
    1  # ValidationStatus.UNCOMMON
    >>> validate('ng', 'u', 'k', '1')
    2  # ValidationStatus.INVALID
    '''
    valid, alert, error = ValidationStatus.VALID, ValidationStatus.UNCOMMON, ValidationStatus.INVALID
    return Validator(args).test({
        'Onset - Nucleus - Coda': [
            (valid, ('- h', '-', 'm ng')),
            (error, (None, '-', None)),

            (error, ('b p m f gw kw w', 'o', 'i')),
            (valid, ('z c s j', 'yu', '-')),
            (error, (None, 'yu', '-')),

            (error, ('f', 'a', 'k')),
            (error, ('f', 'o', 'u')),
            (error, ('f d t', 'aa', 'u ng')),
            (error, ('t', 'e', '- i')),

            (alert, ('w', 'i', '-')),
            (error, ('w', 'i', 'n t')),
            (error, ('w', 'u', 'ng k')),

            (error, ('kw', 'aa', 'n')),
            (error, ('kw', 'a', 'k')),
            (error, ('kw', 'o', '-')),
            (error, ('kw', 'i', 'ng')),

            (error, ('j', 'aa', 'm n t')),
            (error, ('j', 'a', 'ng k')),
        ],
        'Nucleus - Coda': [
            (valid, ('l g', 'a', '-')),
            (alert, ('- m z', 'a', '-')),
            (error, (None, 'a', '-')),

            (valid, ('- g ng h', 'o', 'n')),
            (valid, ('g h', 'o', 't')),
            (error, (None, 'o', 'm n p t')),
            (alert, (None, 'e', 'u m p t')),
            (error, (None, 'e', 'n')),

            (valid, (None, 'oe', '- ng k')),
            (valid, ('z c', 'oe', 't')),
            (error, (None, 'oe', None)),
            (valid, (None, 'eo', 'i n t')),
            (error, (None, 'eo', None)),

            (error, (None, 'i', 'i')),
            (error, (None, 'u', 'u m p')),
            (valid, (None, 'yu', '- n t')),
            (error, (None, 'yu', None)),
        ],
        'Onset - Coda': [
            (error, ('gw kw w', None, 'u')),
            (valid, ('b', 'a', 'm')),
            (error, ('b p m f gw kw w', None, 'm p')),
            (error, ('kw', None, 't')),
        ],
        'Onset - Nucleus': [
            (error, ('- b p m f ng gw kw w', 'oe eo yu', None)),
            (alert, ('f', 'i', None)),

            (alert, ('j', 'o', '-')),
            (error, ('j', 'o', None)),

            (valid, ('-', 'e', '-')),
            (alert, ('-', 'e', 'i')),
            (error, ('-', 'e', None)),

            (valid, ('-', 'u', 'ng k')),
            (alert, ('-', 'i', 'k')),
            (error, ('-', 'i u', None)),

            (alert, ('- ng gw w', 'e', None)),
            (error, ('kw', 'e', None)),
            (valid, ('gw kw', 'i', 'ng k')),
            (error, ('ng gw kw', 'i u', None)),

            (valid, ('l', 'u', '-')),
            (valid, ('d t n l h z c s j', 'u', 'ng k')),
            (error, ('d t n l h z c s j', 'u', None)),
        ],
        'Other': [
            (alert, (None, None, 'p t k', '4 5')),
        ],
    })
