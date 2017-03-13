WESTERN_SIGNS = [(22, 'capricorn'),
                 (21, 'aquarius'),
                 (19, 'pisces'),
                 (21, 'aries'),
                 (21, 'taurus'),
                 (21, 'gemini'),
                 (21, 'cancer'),
                 (23, 'leo'),
                 (23, 'virgo'),
                 (23, 'libra'),
                 (23, 'scorpio'),
                 (22, 'sagittarius'),
                 (22, 'capricorn')
                 ]

CHINESE_SIGNS = ['rat', 'ox', 'tiger', 'rabbit', 'dragon',
                 'snake', 'horse', 'sheep', 'monkey',
                 'rooster', 'dog', 'pig'
                 ]


def interpret_western_sign(day, month):
    """ Returns the zodiac sign, according to the Western Zodiac. """
    if day >= WESTERN_SIGNS[month][0]:
        return WESTERN_SIGNS[month][1]
    else:
        return WESTERN_SIGNS[month - 1][1]


def interpret_chinese_sign(year):
    """ Returns the zodiac sign, according to the Chinese Zodiac. """
    year_offset = year - 1900
    return CHINESE_SIGNS[year_offset % 12]


def interpret_both_signs(day, month, year):
    """ Returns the Western and Chinese zodiacs of a person. """
    western_sign = interpret_western_sign(day, month)
    chinese_sign = interpret_chinese_sign(year)

    return (western_sign, chinese_sign)