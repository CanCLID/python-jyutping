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
        return 0

    @staticmethod
    def match(matcher, group):
        return matcher is None or group in ['' if part == '-' else part for part in matcher.split(' ')]

def validations(r):
    def generate(n):
        def fire(*args):
            return (n, args)
        return fire
    return tuple(generate(n) for n in range(r))

MESSAGE = ['PASS: Valid', 'WARNING: Uncommon', 'Error: Invalid']

def validate(jyutping):
    '''
    >>> validate('jyut6')
    'PASS: Valid'
    >>> validate('gwek6')
    'WARNING: Uncommon'
    >>> validate('nguk1')
    'Error: Invalid'
    '''
    match = re.match('^([gk]w?|ng|[bpmfdtnlhwzcsj]?)(?![1-6]?$)(aa?|oe?|eo?|y?u|i?)(ng|[iumnptk]?)([1-6]?)$', jyutping)
    if match is None: return MESSAGE[-1]
    valid, alert, error = validations(3)
    return MESSAGE[
        Validator(match.groups()).test({
            'Initial - Nucleus - Coda': [
                valid('- h', '-', 'm ng'),
                error(None, '-', None),

                error('b p m f gw kw w', 'o', 'i'),
                valid('z c s j', 'yu', '-'),
                error(None, 'yu', '-'),
                
                error('w', 'u', 'ng k'),
                error('kw', 'i', 'ng'),
            ],
            'Nucleus - Coda': [
                error(None, 'o', 'm p'),
                valid(None, 'oe', '- ng k'),
                valid('z c', 'oe', 't'),
                error(None, 'oe', None),
                valid(None, 'eo', 'i n t'),
                error(None, 'eo', None),
                error(None, 'i', 'i'),
                error(None, 'u', 'u m p'),
                valid(None, 'yu', '- n t'),
                error(None, 'yu', None),
            ],
            'Initial - Coda': [
                error('gw kw w', None, 'u'),
                alert('b', 'a', 'm'), # 泵
                error('b p m f gw kw w', None, 'm p'),
                error('kw', None, 't'),
            ],
            'Initial - Nucleus': [
                error('- b p m f ng gw kw w', 'oe eo yu', None),

                valid('-', 'u', 'ng k'),
                alert('-', 'i', 'k'),
                error('-', 'i u', None),

                alert('- ng gw w', 'e', None),
                error('kw', 'e', None),
                error('kw', 'i', 'ng'),
                valid('gw kw', 'i', 'ng k'),
                error('ng gw kw', 'i u', None),

                valid('l', 'u', '-'),
                valid('d t n l h z c s j', 'u', 'ng k'),
                error('d t n l h z c s j', 'u', None),
            ]
        })
    ]
