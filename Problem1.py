import re
from string import punctuation

def strip_special_chars(name):
    return name.strip(''.join([punctuation, " "]))

def clean_names(raw_names):
    cleaned = []
    dba_regex = re.compile(
        "(?P<first>.*)(d[\W]*)(b[\W]*)(a[\W]+)(?P<second>.*)",
        re.IGNORECASE)

    for raw_name in raw_names:
        match = dba_regex.match(raw_name)
        if match:
            cleaned.append((strip_special_chars(match.group('first')),
                            strip_special_chars(match.group('second'))))
        else:
            cleaned.append((strip_special_chars(raw_name), None))

    return cleaned


if __name__ == '__main__':
    RAW_NAMES = [
        'SPV  Inc., DBA:   Super  Company',
        'Michael Forsky LLC d.b.a F/B Burgers .',
        '*** Youthful You Aesthetics ***',
        'Aruna Indika (dba. NGXess)',
        'Diot SA,  -  D. B. A.   *Diot-Technologies*',
        'PERFECT PRIVACY, LLC, d-b-a Perfection,',
        'PostgreSQL DB Analytics',
        '/JAYE INC/',
        ' ETABLISSEMENTS  SCHEPENS /D.B.A./ ETS_SCHEPENS',
        'DUIKERSTRAINING OOSTENDE | D.B.A.:  D.T.O. '
    ]
    ans = clean_names(RAW_NAMES)
    print(ans)