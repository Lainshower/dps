from ast import Index
import html
import re

import sys

import html2text
from bs4 import BeautifulSoup
import unicodedata
import random

from stdnum import bitcoin
import itertools

def preprocess_text(input_text: str):
    processing_function_list = [
        process_html_and_uri_text,
        reduce_emoticon,
        remove_whitespace,
        replace_email_and_url,
        replace_korean_pii,
        spam_words_filter,
        remove_html_tags,
        remove_general_news_pattern, # [Joonwon]
        remove_repeated_text,
    ]

    for func in processing_function_list:
        input_text = func(input_text)

    if isinstance(input_text, str):
        processed_text = input_text
    else:
        processed_text = " ".join(input_text)

    return processed_text

KOR_BEGIN = 44032
KOR_END = 55203
CHOSUNG_BASE = 588
JUNGSUNG_BASE = 28
JAUM_BEGIN = 12593
JAUM_END = 12622
MOUM_BEGIN = 12623
MOUM_END = 12643

CHOSUNG = [
    "ㄱ",
    "ㄲ",
    "ㄴ",
    "ㄷ",
    "ㄸ",
    "ㄹ",
    "ㅁ",
    "ㅂ",
    "ㅃ",
    "ㅅ",
    "ㅆ",
    "ㅇ",
    "ㅈ",
    "ㅉ",
    "ㅊ",
    "ㅋ",
    "ㅌ",
    "ㅍ",
    "ㅎ",
]

JUNGSUNG = [
    "ㅏ",
    "ㅐ",
    "ㅑ",
    "ㅒ",
    "ㅓ",
    "ㅔ",
    "ㅕ",
    "ㅖ",
    "ㅗ",
    "ㅘ",
    "ㅙ",
    "ㅚ",
    "ㅛ",
    "ㅜ",
    "ㅝ",
    "ㅞ",
    "ㅟ",
    "ㅠ",
    "ㅡ",
    "ㅢ",
    "ㅣ",
]

JONGSUNG = [
    " ",
    "ㄱ",
    "ㄲ",
    "ㄳ",
    "ㄴ",
    "ㄵ",
    "ㄶ",
    "ㄷ",
    "ㄹ",
    "ㄺ",
    "ㄻ",
    "ㄼ",
    "ㄽ",
    "ㄾ",
    "ㄿ",
    "ㅀ",
    "ㅁ",
    "ㅂ",
    "ㅄ",
    "ㅅ",
    "ㅆ",
    "ㅇ",
    "ㅈ",
    "ㅊ",
    "ㅋ",
    "ㅌ",
    "ㅍ",
    "ㅎ",
]

JAUM = [
    "ㄱ",
    "ㄲ",
    "ㄳ",
    "ㄴ",
    "ㄵ",
    "ㄶ",
    "ㄷ",
    "ㄸ",
    "ㄹ",
    "ㄺ",
    "ㄻ",
    "ㄼ",
    "ㄽ",
    "ㄾ",
    "ㄿ",
    "ㅀ",
    "ㅁ",
    "ㅂ",
    "ㅃ",
    "ㅄ",
    "ㅅ",
    "ㅆ",
    "ㅇ",
    "ㅈ",
    "ㅉ",
    "ㅊ",
    "ㅋ",
    "ㅌ",
    "ㅍ",
    "ㅎ",
]

MOUM = [
    "ㅏ",
    "ㅐ",
    "ㅑ",
    "ㅒ",
    "ㅓ",
    "ㅔ",
    "ㅕ",
    "ㅖ",
    "ㅗ",
    "ㅘ",
    "ㅙ",
    "ㅚ",
    "ㅛ",
    "ㅜ",
    "ㅝ",
    "ㅞ",
    "ㅟ",
    "ㅠ",
    "ㅡ",
    "ㅢ",
    "ㅣ",
]

JAMO = CHOSUNG + JUNGSUNG

# HTML PROCESSING
HTML_REMOVE = [
    "javascript",
    "/",
    "#",
    "*",
    "![",
    "[!",
    "[(",
    ")]",
    "[]",
    "()",
    ";",
    "뉴스",
    "기사",
    "신문",
    "카카오",
    "네이버",
    "티스토리",
    "무단전재",
    "저작권",
    "재배포",
    "구독",
    "검색어",
    "=",
    "__",
]
HTML_SPLIT = [
    "더보기",
    "더 보기",
]

# PHONE NUMBER
PHONE_NUMBER_PATTERN = re.compile(
    r"([0-9]{2,3}-[0-9]{2,4}-[0-9]{2,4})|(\(?[0-9]{2,3}\)?[0-9]{2,4}[0-9]{2,4})" # [Joonwon]
)

# RRN
RRN_PATTERN = re.compile(r"([0-9]{6}-[0-9]{7})")

# CARD
CARD_PATTERN = re.compile(r"([0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{4})")

# BANK ACCOUNT
ACCOUNT_PATTERN = re.compile(
    r"([0-9]\d{13})|([0-9,\-]{3,6}\-[0-9,\-]{2,6}\-[0-9,\-]{2,6})"  # IBK
    + r"([0-9]\d{13})|([0-9,\-]{3,6}\-[0-9,\-]{2,6}\-[0-9,\-]{2,6})"  # KB
    + r"([0-9]\d{12})|([0-9,\-]{3,6}\-[0-9,\-]{2,6}\-[0-9,\-]{2,6}\-[0-9,\-]{2})"  # NH
    + r"([0-9]\d{11})|([0-9,\-]{3,6}\-[0-9,\-]{2,6}\-[0-9,\-]{2,6})"  # SHINHAN
    + r"([0-9]\d{12})|([0-9,\-]{3,6}\-[0-9,\-]{2,6}\-[0-9,\-]{2,6})"  # WOORI
    + r"([0-9]\d{13})|([0-9,\-]{3,6}\-[0-9,\-]{2,6}\-[0-9,\-]{2,6})"  # KEB
    + r"([0-9]\d{11})|([0-9,\-]{3,6}\-[0-9,\-]{2,6}\-[0-9,\-]{2,6})"  # CITI
    + r"([0-9]\d{11})|([0-9]\d{11})|([0-9,\-]{3,6}\-[0-9,\-]{2,6}\-[0-9,\-]{2,6}\-[0-9,\-])"  # DGB
    + r"([0-9]\d{12})|([0-9]\d{12})|([0-9,\-]{3,6}\-[0-9,\-]{2,6}\-[0-9,\-]{2,6}\-[0-9,\-]{2})"  # BNK
    + r"([0-9]\d{10})|([0-9]\d{10})|([0-9,\-]{3,6}\-[0-9,\-]{2,6}\-[0-9,\-]{2,6})"  # SC
    + r"([0-9]\d{11})|([0-9]\d{10})|([0-9,\-]{3,6}\-[0-9,\-]{2,6}\-[0-9,\-]{2,6})"  # KBANK
    + r"([0-9]\d{12})|([0-9]\d{10})|([0-9,\-]{3,6}\-[0-9,\-]{2,6}\-[0-9,\-]{2,7})"  # KAKAO
)

# SPAM FILTERING
_NEWS = [
    f"{prefix}{word}"
    for word in [
        "폴리뉴스는 인터넷신문위원회의",
        "[조세금융신문",
        "[사진] ⓒ",
        "▶DAUM에서",
        "▶NAVER에서",
        "Copyright",
        "Copyrights",
        "저작권자©",
        "저작권자 ©",
        "저작권자ⓒ",
        "저작권자 ⓒ",
        "저작권자(c)",
        "저작권자 (c)",
        "저작권자:",
        "저작권자 :",
        "저작권자|",
        "저작권자 |",
        "©",
        "ⓒ",
        "무단전재",
        "무단 전재",
        "방송된 기사 내용은",
        "촬영기자:",
        "촬영기자 :",
        "영상편집:",
        "영상편집 :",
        "▷ 카카오톡:",
        "▷ 카카오톡 :",
        "카카오톡:",
        "카카오톡 :",
        "▷ 전화:",
        "▷ 전화 :",
        "전화:",
        "전화 :",
        "■ 제보하기",
        "연합뉴스TV 기사문의 및 제보",
        "제보는 카카오톡",
        "(끝)",
        "기사제보 및 보도자료 제공",
    ]
    for prefix in [
        "<",
        "< ",
        "〈",
        "〈 ",
        "[",
        "[ ",
        "(",
        "( ",
        "( ",
        "- ",
        "",
    ]
]
_WEBSITE_FOOTER = [
    f"{prefix}{word}{suffix}"
    for word in [
        "이메일",
        "TEL",
        "FAX",
        "PHONE",
        "EMAIL",
        "전화번호",
        "전화 번호",
        "주소",
        "대표자명",
        "대표자 명",
        "사업자등록번호",
        "사업자 등록번호",
        "사업자등록 번호",
        "사업자 등록 번호",
        "대표이사",
        "대표 이사",
        "통신판매번호",
        "통신 판매번호",
        "통신판매 번호",
        "통신 판매 번호",
    ]
    for prefix in ["", "|", "| "]
    for suffix in [":", " :"]
]
SPAM_SPLIT = [
    # 이전 모델에서 많이 나오던 패턴.
    "공유하기 글 요소",
    # 지금까지 (공백 0~6개) ~~기자였습니다.
    re.compile(
        r"(?i)(?:\b(지금까지|.{2,7}에서)\b)\W+(?:\w+[^\w]+){0,6}?\b(기자|특파원|교통정보|KBS 뉴스|SBS 뉴스|MBC 뉴스|YTN|MBN|뉴스더하기)"
    ),
    # KBS 뉴스 (공백 0~3개) ~~입니다.
    re.compile(
        r"(?i)(?:\b(KBS 뉴스|SBS 뉴스|MBC 뉴스|YTN|MBN)\b)\W+(?:\w+){0,3}?(였습니다\.|입니다\.).*"
    ),
    re.compile("|".join([re.escape(p) for p in _NEWS + _WEBSITE_FOOTER])),
]
SPAM_REMOVE = [
    (
        # (서울=연합뉴스) ~~기자 =
        # 사진=연합뉴스
        re.compile("\(+.+=연합뉴스\)+.+(기자 =|특파원 =)|=연합뉴스|"),
        "",
    )
]

BAD_WORDS = [
    "콜걸",
    "출장 안마",
    "출장안마",
    "출장 마사지",
    "출장마사지",
    "출장만남",
    "출장 만남",
    "조건만남",
    "조건 만남",
    "출장서비스",
    "출장 서비스",
    "스포츠토토",
    "스포츠 토토",
    "바카라",
    "폰섹",
    "카지노사이트",
    "카지노 사이트",
    "토토사이트",
    "토토 사이트",
    "바다 이야기",
    "바다이야기",
    "조건 카톡",
    "조건카톡",
    "출장샵",
    "출장 샵",
    "마사지샵",
    "마사지 샵",
    "사설토토",
    "사설 토토",
    "카지노추천",
    "카지노 추천",
    "카지노주소",
    "카지노 주소",
    "안전놀이터",
    "안전 놀이터",
    "먹튀사이트",
    "먹튀 사이트",
]

PHONE_NUMBER_START_TOKEN = "<|tel_start|>"
PHONE_NUMBER_END_TOKEN = "<|tel_end|>"

RRN_START_TOKEN = "<|rrn_start|>"
RRN_END_TOKEN = "<|rrn_end|>"

URL_START_TOKEN = "<|url_start|>"
URL_END_TOKEN = "<|url_end|>"

EMAIL_START_TOKEN = "<|email_start|>"
EMAIL_END_TOKEN = "<|email_end|>"

CARD_START_TOKEN = "<|crd_start|>"
CARD_END_TOKEN = "<|crd_end|>"

ACCOUNT_START_TOKEN = "<|acc_start|>"
ACCOUNT_END_TOKEN = "<|acc_end|>"

NAME_START_TOKEN = "<|name_start|>"
NAME_END_TOKEN = "<|name_end|>"

ORG_START_TOKEN = "<|org_start|>"
ORG_END_TOKEN = "<|org_end|>"

# URL
URL_PATTERN = re.compile(
    r"""\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b"""
)

# EMAIL
EMAIL_PATTERN = re.compile(
    r"[a-z0-9.\-+_]+@[a-z0-9.\-+_]+\.[a-z]+|[a-z0-9.\-+_]+@[a-z0-9.\-+_]+\.[a-z]+\.[a-z]"
)

# IP PATTERN
IP_PATTERN = re.compile(
    r"""
     \b
     (?: (?: 25[0-5] | 2[0-4][0-9] | [01]?[0-9][0-9]? ) \. ){3}
     (?: 25[0-5] | 2[0-4][0-9] | [01]?[0-9][0-9]?)
     \b
"""
)

# BANK ACCOUNT
BANK_ACCOUNT_PATTERN = re.compile(
    r"([0-9]\d{13})|([0-9,\-]{3,6}\-[0-9,\-]{2,6}\-[0-9,\-]{2,6})"  # IBK
    + r"([0-9]\d{13})|([0-9,\-]{3,6}\-[0-9,\-]{2,6}\-[0-9,\-]{2,6})"  # KB
    + r"([0-9]\d{12})|([0-9,\-]{3,6}\-[0-9,\-]{2,6}\-[0-9,\-]{2,6}\-[0-9,\-]{2})"  # NH
    + r"([0-9]\d{11})|([0-9,\-]{3,6}\-[0-9,\-]{2,6}\-[0-9,\-]{2,6})"  # SHINHAN
    + r"([0-9]\d{12})|([0-9,\-]{3,6}\-[0-9,\-]{2,6}\-[0-9,\-]{2,6})"  # WOORI
    + r"([0-9]\d{13})|([0-9,\-]{3,6}\-[0-9,\-]{2,6}\-[0-9,\-]{2,6})"  # KEB
    + r"([0-9]\d{11})|([0-9,\-]{3,6}\-[0-9,\-]{2,6}\-[0-9,\-]{2,6})"  # CITI
    + r"([0-9]\d{11})|([0-9]\d{11})|([0-9,\-]{3,6}\-[0-9,\-]{2,6}\-[0-9,\-]{2,6}\-[0-9,\-])"  # DGB
    + r"([0-9]\d{12})|([0-9]\d{12})|([0-9,\-]{3,6}\-[0-9,\-]{2,6}\-[0-9,\-]{2,6}\-[0-9,\-]{2})"  # BNK
    + r"([0-9]\d{10})|([0-9]\d{10})|([0-9,\-]{3,6}\-[0-9,\-]{2,6}\-[0-9,\-]{2,6})"  # SC
    + r"([0-9]\d{11})|([0-9]\d{10})|([0-9,\-]{3,6}\-[0-9,\-]{2,6}\-[0-9,\-]{2,6})"  # KBANK
    + r"([0-9]\d{12})|([0-9]\d{10})|([0-9,\-]{3,6}\-[0-9,\-]{2,6}\-[0-9,\-]{2,7})"  # KAKAO
)

CREDIT_CARD_PATTERN = re.compile(
    r"^(4026|417500|4405|4508|4844|4913|4917)\d+$|"  # VISA Electron
    + r"^(?:50|5[6-9]|6[0-9])\d+$|"  # Maestro
    + r"^(5019|4571)\d+$|"  # Dankort
    + r"^(62|81)\d+$|"  # China UnionPay
    + r"^4[0-9]\d+$|"  # Visa
    + r"^(?:5[1-5]|222[1-9]|22[3-9][0-9]|2[3-6][0-9][0-9]|27[0-1][0-9]|2720)\d+$|"  # MasterCard
    + r"^(34|37)\d+$|"  # American Express
    + r"^6(?:011|22(12[6-9]|1[3-9][0-9]|[2-8][0-9][0-9]|9[01][0-9]|92[0-5])|5|4|2[4-6][0-9]{3}|28[2-8][0-9]{2})\d+$|"  # Discover
    + r"^(35[2-8][0-9])\d+$|"  # JCB
    + r"^(636)\d+$|"  # InterPayment
    + r"^9[0-9]\d+$|"  # KOREAN
    + r"^(220[0-4])\d+$"  # MIR
)

# From https://github.com/unicode-org/cldr/blob/release-26-0-1/common/supplemental/postalCodeData.xml
# Extracting the most common to avoid the checking of 158 countries
ZIP_PATTERN = re.compile(
    r"GIR[ ]?0AA|((AB|AL|B|BA|BB|BD|BH|BL|BN|BR|BS|BT|CA|CB|CF|CH|CM|CO|CR|CT|CV|CW|DA|DD|DE|DG|DH|DL|DN|DT|DY|E|EC|EH|EN|EX|FK|FY|G|GL|GY|GU|HA|HD|HG|HP|HR|HS|HU|HX|IG|IM|IP|IV|JE|KA|KT|KW|KY|L|LA|LD|LE|LL|LN|LS|LU|M|ME|MK|ML|N|NE|NG|NN|NP|NR|NW|OL|OX|PA|PE|PH|PL|PO|PR|RG|RH|RM|S|SA|SE|SG|SK|SL|SM|SN|SO|SP|SR|SS|ST|SW|SY|TA|TD|TF|TN|TQ|TR|TS|TW|UB|W|WA|WC|WD|WF|WN|WR|WS|WV|YO|ZE)(\d[\dA-Z]?[ ]?\d[ABD-HJLN-UW-Z]{2}))|BFPO[ ]?\d{1,4}|"
    + r"JE\d[\dA-Z]?[ ]?\d[ABD-HJLN-UW-Z]{2}|"  # Jersey
    + r"GY\d[\dA-Z]?[ ]?\d[ABD-HJLN-UW-Z]{2}|"  # Guernsey
    + r"IM\d[\dA-Z]?[ ]?\d[ABD-HJLN-UW-Z]{2}|"  # IM
    + r"\d{5}([ \-]\d{4})?|"  # US ZIP
    + r"[ABCEGHJKLMNPRSTVXY]\d[ABCEGHJ-NPRSTV-Z][ ]?\d[ABCEGHJ-NPRSTV-Z]\d|"  # Canada
    + r"\d{5}|"  # DE, IT, ES, FI, DZ
    + r"\d{3}-\d{4}|"  # JP
    + r"\d{2}[ ]?\d{3}|"  # FR
    + r"\d{4}|"  # AU, CH, AT, BE, DK, NO, AZ, BD
    + r"\d{4}[ ]?[A-Z]{2}|"  # NL
    + r"\d{3}[ ]?\d{2}|"  # SE
    + r"\d{5}[\-]?\d{3}|"  # BR
    + r"\d{4}([\-]\d{3})?|"  # PT
    + r"\d{3}[\-]\d{3}"  # KR
)

# BITCOIN PATTERN
BITCOIN_PATTERN = (
        r"( [13] ["
        + bitcoin._base58_alphabet
        + "]{25,34}"
        + "| bc1 ["
        + bitcoin._bech32_alphabet
        + "]{8,87})"
)

# https://stackoverflow.com/questions/827557/how-do-you-validate-a-url-with-a-regular-expression-in-python
ul = '\u00a1-\uffff'  # Unicode letters range (must not be a raw string).

# IP patterns
IPV4_PATTERN = r'(?:0|25[0-5]|2[0-4]\d|1\d?\d?|[1-9]\d?)(?:\.(?:0|25[0-5]|2[0-4]\d|1\d?\d?|[1-9]\d?)){3}'
IPV6_PATTERN = r'\[?((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,' \
    r'4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{' \
    r'1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[' \
    r'0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,' \
    r'3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[' \
    r'1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,' \
    r'2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([' \
    r'0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[' \
    r'0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[' \
    r'0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[' \
    r'0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,' \
    r'5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\]?'


# Host patterns
HOSTNAME_PATTERN = r'[a-z' + ul + r'0-9](?:[a-z' + ul + r'0-9-]{0,61}[a-z' + ul + r'0-9])?'
# Max length for domain name labels is 63 characters per RFC 1034 sec. 3.1
DOMAIN_PATTERN = r'(?:\.(?!-)[a-z' + ul + r'0-9-]{1,63}(?<!-))*'
TLD_PATTERN = (
        r'\.'                                # dot
        r'(?!-)'                             # can't start with a dash
        r'(?:[a-z' + ul + '-]{2,63}'         # domain label
        r'|xn--[a-z0-9]{1,59})'              # or punycode label
        r'(?<!-)'                            # can't end with a dash
        r'\.?'                               # may have a trailing dot
)

HOST_PATTERN = '(' + HOSTNAME_PATTERN + DOMAIN_PATTERN + TLD_PATTERN + '|localhost)'


URL2_PATTERN = re.compile(
    r'([a-z0-9.+-]*:?//)?'                                      # scheme is validated separately
    r'(?:[^\s:@/]+(?::[^\s:@/]*)?@)?'                           # user:pass authentication
    r'(?:' + IPV4_PATTERN + '|' + IPV6_PATTERN + '|' + HOST_PATTERN + ')'
    r'(?::\d{2,5})?'                                            # port
    r'(?:[/?#][^\s]*)?',                                        # resource path
    re.IGNORECASE
)

# [Joonwon] - NEWS
KOREAN_NEWS_REMOVE = [
    (
        # [Joonwon]
        re.compile(
            r"EBN산업뉴스|e대한경제|강원도민일보|강원일보|경기일보|경남도민일보|"
            r"경북일보|경상일보|경인일보|경향신문|광주매일신문|광주일보|국민일보|"
            r"국제신문|기호일보|남도일보|내일신문|노컷뉴스|뉴스핌|대구신문|대구일보|"
            r"대전일보|동양일보|매일신문|머니투데이|무등일보|미디어오늘|부산일보|"
            r"서울경제|서울신문|세계일보|스포츠서울|스포츠일간|아시아경제|아주경제|"
            r"영남일보|울산매일신문|이데일리|이투데이|인천일보|전남일보|전북도민일보|"
            r"전북일보|전자신문|제민일보|조선일보|중도일보|중부매일|중부일보|충북일보|"
            r"충청일보|충청 일보|충청투데이|파이낸셜뉴스|한겨레|한국경제|한국일보|"
            r"한라일보|헤럴드경제|환경일보|연합뉴스|(PG)"
            r"( TV)?",
            re.IGNORECASE
        ),
        "",
    ),
]

# [Joonwon] - NEWS
GENERAL_NEWS_PATTERN = {
    "email_and_symbols": re.compile(
        r"(\sⓒ\s?\([^\)]+\))|"  # ⓒ (email)
        r"(\w+@\(이메일\))|"    # Placeholder for email
        r"([^\s]+@(이메일))|"  # Email removal with placeholder
        r"전화\s?\b\d{2,3}[-]\d{3,4}[-]\d{4}\b|"       
        r"이메일\s?\b\S+@\S+\.\S+\b|"                  
        r"\w+\s?\@\w+|"  
        r"\b\d{2,3}[-]\d{3,4}[-]\d{4}\b|"    
        r"\b\S+@\S+\.\S+\b|"                 
        r"\@\w+",                             
        flags=re.IGNORECASE
    ),
    "news_references": re.compile(
        r"\((서울|[^\s\)]+)\s?=\s?[^\)]*\)|"     # (서울=Text) or (Word=Text)
        r"\[\w+\s?=\s?\w*\]|"                   # [Word=Word] or [Word=]
        r"【[^\】]*】|"                          # 【Content】 or 【】
        r"© [^\s]* 뉴스|"                       # News copyright
        r"무단 전재 및 재배포 금지|"            # Redistribution prohibition
        r"\<저작권자ⓒ [^\>]*\>|"               # Copyright notices
        r"\[[^\]]*\]|"                          # [Any=Text] or [Any=] general location or info
        r"\(\w+\s?=\s?[\w\s]*\)",               # (글자=글자 or 공백) or (글자=)
        flags=re.IGNORECASE
    ),
    "article_references": re.compile(
        r"(\[사진 [^\]]+\])|"          # [Picture] tags
        r"(\[포토\])|"                # [Photo] tags
        r"(\[동영상\])|"              # [Video] tags
        r"\<사진=.*?\>|"
        r"\<비디오=.*?\>|"
        r"\<동영상=.*?\>|"
        r"('호에 실린 기사')|"
        r"\d+호에 실린 기사|"
        r"☞ 본 기사는.*",
        flags=re.IGNORECASE
    ),
    "journalist_names": re.compile(
    r"\b\w+ ?= ?\w+ 기자|"               # Matches "Name = Name 기자", "Name=Name 기자"
    r"\b\w+ 기자 ?=|"                    # Matches "Name 기자 =", "Name 기자="
    r"\([^\)]+\) 기자 ?=|"               # Matches "(Name) 기자 =", "(Name) 기자="
    r"\b[a-zA-Z가-힣]+ 기자|"            # Matches "Name 기자"
    r"TV\s*.{2,7}\.|"
    r"◀ ?\w+ ?▶",                        # Matches "◀ Name ▶", "◀Name▶"
        flags=re.IGNORECASE
    ),
    "copyright": re.compile(
        r"\<저작권자\s*© [^\>]+\>|"                              # <Copyright Owner ⓒ ... >
        r"저작권자[ ©]+\s+[^\s,]+, 무단전재 및 재배포 금지|"      # Broad pattern for copyright notices
        r"뉴스[0-9]+코리아|"                                     # Patterns like News1Korea
        r"공감언론 뉴시스|"                                      # Specific news outlet
        r"[a-zA-Z가-힣]+ 뉴스|"                                  # General news media mention
        r"[a-zA-Z가-힣]+ 통신사|"                                # Communication companies
        r"[a-zA-Z가-힣]+방송",                                   # Broadcasting companies
        flags=re.IGNORECASE
    ),
    "promotional_content": re.compile(
        r"#[^\s]{1,7}|"
        r"^\[.*?\]",                 # Removing text within brackets at the start of the each line
        flags=re.IGNORECASE | re.MULTILINE
    ),
    "symbol_cleanup": re.compile(
        r"▶\.?|◎\.?|▷\.?|\(?<\|(?!.*\w)|(?<!\w)\|>\)?$",                   # Removing '▶' and everything after it in the line
        flags=re.IGNORECASE | re.MULTILINE
    ),
    "inquiry_and_tip_off": re.compile(
        r"\b[a-zA-Z가-힣]*\s*기사\s?문의 및 제보\s*:\s*.+",
        flags=re.IGNORECASE
    )
}


def replace_with_token(text, pattern, start, end, replaces, random_number=True):
    def replace_number(match):
        return str(random.randint(0, 9))

    found = re.findall(pattern, text)
    for one in found:
        if isinstance(one, str):
            one = [one]
        for o in one:
            if len(o) == 0:
                continue
            if random_number:
                replace = re.sub(r"\d", replace_number, o)
            else:
                replace = o
            replaces.append((f"{start}{end}", f"{start}{replace}{end}"))
            text = text.replace(o, f"{start}{end}")
    return text


def split_sentences(text):
    sents = re.split(r"\r\n|\n|\t|\v|\f", text)
    sents = [re.split(r"(?<=[.!?])\s", s) for s in sents]
    sents = list(itertools.chain(*sents))
    return sents

def split_sentences(text):
    sents = re.split(r"\r\n|\n|\t|\v|\f", text)
    sents = [re.split(r"(?<=[.!?])\s", s) for s in sents]
    sents = list(itertools.chain(*sents))
    return sents

def process_html_and_uri_text(text: str):
    text = html.unescape(text)
    text = re.sub(r"<\s*/?\s*br\s*/?\s*>", "\n", text)  # https://chojja7.tistory.com/34
    text = re.sub(r"<\s*/?\s*BR\s*/?\s*>", "\n", text)  # https://chojja7.tistory.com/34
    return text

def reduce_emoticon(text: str, num_repeats=3): # [Joonwon]
    """
    Original Code
    https://github.com/lovit/soynlp/blob/master/soynlp/normalizer/_normalizer.py

    Function that reduces repeating Korean characters
    ex) ㅋㅋㅋㅋㅋㅋㅋ => ㅋㅋ
    """

    repeatchars_pattern = re.compile("(\w)\\1{2,}")
    doublespace_pattern = re.compile("[^\S\r\n]+")
    if not text:
        return text

    def to_base(c):
        if sys.version_info.major == 2:
            if type(c) == str or type(c) == unicode:
                return ord(c)
            else:
                raise TypeError
        else:
            if type(c) == str or type(c) == int:
                return ord(c)
            else:
                raise TypeError

    def compose(chosung, jungsung, jongsung):
        return chr(
            KOR_BEGIN
            + CHOSUNG_BASE * CHOSUNG.index(chosung)
            + JUNGSUNG_BASE * JUNGSUNG.index(jungsung)
            + JONGSUNG.index(jongsung)
        )

    def decompose(c):
        if not character_is_korean(c):
            return None
        i = to_base(c)
        if JAUM_BEGIN <= i <= JAUM_END:
            return c, " ", " "
        if MOUM_BEGIN <= i <= MOUM_END:
            return " ", c, " "
        i -= KOR_BEGIN
        cho = i // CHOSUNG_BASE
        jung = (i - cho * CHOSUNG_BASE) // JUNGSUNG_BASE
        jong = i - cho * CHOSUNG_BASE - jung * JUNGSUNG_BASE
        return CHOSUNG[cho], JUNGSUNG[jung], JONGSUNG[jong]

    def character_is_korean(c):
        i = to_base(c)
        return (
            (KOR_BEGIN <= i <= KOR_END)
            or (JAUM_BEGIN <= i <= JAUM_END)
            or (MOUM_BEGIN <= i <= MOUM_END)
        )

    def repeat_normalize(sent, num_repeats=2):
        if num_repeats > 0:
            sent = repeatchars_pattern.sub("\\1" * num_repeats, sent)
        sent = doublespace_pattern.sub(" ", sent)
        return sent.strip()

    # Pattern matching ㅋ쿠ㅜ
    def pattern(idx):
        # Jaum: 0, Moum: 1, Complete: 2, else -1
        if 12593 <= idx <= 12622:
            return 0
        elif 12623 <= idx <= 12643:
            return 1
        elif 44032 <= idx <= 55203:
            return 2
        else:
            return -1

    indices = [pattern(ord(c)) for c in text]
    sent_ = []
    last_idx = len(indices) - 1
    for i, (idx, c) in enumerate(zip(indices, text)):
        if (0 < i < last_idx) and (
            indices[i - 1] == 0 and idx == 2 and indices[i + 1] == 1
        ):
            cho, jung, jong = decompose(c)
            if (cho == text[i - 1]) and (jung == text[i + 1]) and (jong == " "):
                sent_.append(cho)
                sent_.append(jung)
            else:
                sent_.append(c)
        elif (i < last_idx) and (idx == 2) and (indices[i + 1] == 0):
            cho, jung, jong = decompose(c)
            if jong == text[i + 1]:
                sent_.append(compose(cho, jung, " "))
                sent_.append(jong)
        elif (i > 0) and (idx == 2 and indices[i - 1] == 0):
            cho, jung, jong = decompose(c)
            if cho == text[i - 1]:
                sent_.append(cho)
                sent_.append(jung)
        else:
            sent_.append(c)

    return repeat_normalize("".join(sent_), num_repeats)

def remove_whitespace(text: str, remove_duplicate_whitespace: bool = True) -> str:
    if remove_duplicate_whitespace:
        return " ".join(re.split("[^\S\r\n\t\v\f]+", text.strip(), flags=re.UNICODE))
    return text.strip()

def replace_email_and_url(text: str):
    """
    TODO:
        email de-identification needed.
        cc @paulvn
    """
    replaces = []
    text = replace_with_token(
        text, EMAIL_PATTERN, EMAIL_START_TOKEN, EMAIL_END_TOKEN, replaces
    )
    text = replace_with_token(
        text, URL_PATTERN, URL_START_TOKEN, URL_END_TOKEN, replaces
    )

    for before, after in replaces:
        text = text.replace(before, after)

    return text

def replace_korean_pii(text: str):
    replaces = []
    text = replace_with_token(
        text, CARD_PATTERN, CARD_START_TOKEN, CARD_END_TOKEN, replaces
    )
    text = replace_with_token(
        text, RRN_PATTERN, RRN_START_TOKEN, RRN_END_TOKEN, replaces
    )
    text = replace_with_token(
        text,
        PHONE_NUMBER_PATTERN,
        PHONE_NUMBER_START_TOKEN,
        PHONE_NUMBER_END_TOKEN,
        replaces,
    )
    text = replace_with_token(
        text, ACCOUNT_PATTERN, ACCOUNT_START_TOKEN, ACCOUNT_END_TOKEN, replaces
    )
    
    for before, after in replaces:
        text = text.replace(before, after)

    return text

def spam_words_filter(text):
    """Remove spam words from the given input text"""
    for pattern, repl in SPAM_REMOVE:
        text = re.sub(pattern, repl, text)
    for pattern in SPAM_SPLIT:
        text = re.split(pattern, text, maxsplit=1)[0]
    return text.strip()

def remove_html_tags(text: str):
    def clean_space(text):
        text = re.sub("[\r\n\f\v\t]", " ", text)
        while "  " in text:
            text = text.replace("  ", " ")
        return text.strip()

    if bool(BeautifulSoup(text, "html.parser").find()):
        try:
            processed_html = html2text.html2text(text)
        except AssertionError:
            processed_html = text
        
        text = processed_html
        text = clean_space(text)

        for pattern in [
            URL_PATTERN,
            URL_START_TOKEN,
            URL_END_TOKEN,
            EMAIL_PATTERN,
            EMAIL_START_TOKEN,
            EMAIL_END_TOKEN,
        ]:
            text = re.sub(pattern, "", text)

        sents = re.split(r"(?<=[.!?])\s", text)

        filtered_sents = []
        for sent in sents:
            add = True
            for symbol in HTML_REMOVE:
                if symbol in sent:
                    add = False
                    break

            if add is True:
                for symbol in HTML_SPLIT:
                    sent = sent.split(symbol)[0]
                filtered_sents.append(sent)

        text = " ".join(filtered_sents)
        text = clean_space(text)
        text = text.replace(" !", "")
    return text


def remove_repeated_text(input_text, ngram_range=(3, 13), trial=3):
    def _remove_repeated_phrase(input_text, ngram_range):
        words = input_text.split()
        repeated_part_spans = []

        for i, word in enumerate(words):
            prev_ngrams = dict()
            next_ngrams = dict()

            for j in range(ngram_range[0], ngram_range[1] + 1):
                if i - j < 0 or i + j + 1 > len(words):
                    continue

                prev_ngrams[j] = " ".join(words[i - j : i])
                next_ngrams[j] = " ".join(words[i + 1 : i + j + 1])

            for j, (prev_ngram, next_ngram) in enumerate(
                zip(prev_ngrams.values(), next_ngrams.values())
            ):
                if prev_ngram == next_ngram:
                    repeated_part_spans.append(((i - j, i), (i + 1, i + j + 1)))

        for word_pos, word in enumerate(words):
            for span in repeated_part_spans:
                if word_pos in range(span[0][0], span[0][1]) or word_pos in range(
                    span[1][0], span[1][1]
                ):
                    words[word_pos] = ""

        input_text = " ".join(words)
        input_text = re.sub(r"\s+", " ", input_text)
        return input_text.strip(), repeated_part_spans

    def _remove_repeated_word_over_n_times(input_text, n=3):
        words = input_text.split()
        repeated = []

        for i, word in enumerate(words):
            for n_repeat in range(n):
                if i + n_repeat + 1 < len(words):
                    if word == words[i + n_repeat + 1]:
                        repeated.append(i)
                    else:
                        break

        # remove repeated
        for word_pos, word in enumerate(words):
            if word_pos in repeated:
                words[word_pos] = ""

        input_text = " ".join(words)
        input_text = re.sub(r"\s+", " ", input_text)
        return input_text

    total_len_spans = 0
    for _ in range(trial):
        input_text, spans = _remove_repeated_phrase(input_text, ngram_range)
        total_len_spans += len(spans)

    input_text = _remove_repeated_word_over_n_times(input_text)
    return input_text

def replace_with_token(text, pattern, start, end, replaces, random_number=True):
    def replace_number(match):
        return str(random.randint(0, 9))

    found = re.findall(pattern, text)
    for one in found:
        if isinstance(one, str):
            one = [one]
        for o in one:
            if len(o) == 0:
                continue
            if random_number:
                replace = re.sub(r"\d", replace_number, o)
            else:
                replace = o
            replaces.append((f"{start}{end}", f"{start}{replace}{end}"))
            text = text.replace(o, f"{start}{end}")
    return text

# [Joonwon]
def remove_general_news_pattern(text):
    for pattern, repl in KOREAN_NEWS_REMOVE:
        text = re.sub(pattern, repl, text)
    for pattern in GENERAL_NEWS_PATTERN.values():
        text = pattern.sub('', text)
    return text


def test(directory):
    import os
    import json

    jsonl_path = os.path.join(directory, 'sampled.jsonl')
    sampled_path = os.path.join(directory, 'preprocessed.jsonl')
    
    if not os.path.isfile(jsonl_path):
        raise FileNotFoundError(f"{jsonl_path} 파일을 찾을 수 없습니다.")
    
    data = []
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))
    
    data = [{'text': preprocess_text(datum['text'])} for datum in data]
    
    with open(sampled_path, 'w', encoding='utf-8') as outfile:
        for line in data:
            json_line = json.dumps(line, ensure_ascii=False) + "\n"
            outfile.write(json_line)
    
    print(f"{len(data)}개의 샘플링된 데이터가 {sampled_path}에 저장되었습니다.")

if __name__ == "__main__":
    import os
    import argparse
    import json

    parser = argparse.ArgumentParser(description="")
    parser.add_argument('directory', type=str, help="deduplication.jsonl 파일이 있는 디렉토리 경로")
    
    args = parser.parse_args()
    
    # 샘플링 수행
    test(args.directory)