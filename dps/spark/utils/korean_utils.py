import re


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
    r"([0-9]{2,3}-[0-9]{3,4}-[0-9]{4})|([0-9]{2,3}[0-9]{3,4}[0-9]{4})"
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
    ),
    # yyyy.mm.dd <|email|>
    (
        re.compile("([0-9]{4}\.[0-9]{1,2}\.[0-9]{1,2})( |\w)(<\|email\|>|<\|url\|>)"),
        "",
    ),
    # ~~했다. <|email|>
    (
        re.compile("(다\. <\|email\|>)|다\. <\|url\|>"),
        "다.",
    ),
    # ~~~기자 <|email|>
    (
        re.compile("기자 <\|email\|>"),
        "기자",
    ),
]
