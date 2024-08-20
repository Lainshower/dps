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
    r"([0-9]{2,3}-[0-9]{2,4}-[0-9]{2,4})|(\([0-9]{2,3}\)[0-9]{2,4}[0-9]{2,4})"
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
KOREAN_NEWS_PATTERN = {
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
