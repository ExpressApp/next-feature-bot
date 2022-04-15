import re

ADD_BOT_CREDENIALS_REGEXP = re.compile(
    r"^(?P<host>\S+\.\S+)\s+(?P<secret_key>\w+)\s+(?P<bot_id>[a-f0-9-]+)$"
)
BOTX_METHOD_ARGS_REGEXP = re.compile(
    (
        r"^(?P<http_method>(GET|POST|PUT|PATCH|DELETE)) +(?P<path_with_query>\/\S+)"
        r"(\s+(```)?(?P<embedded_payload>.*?)(```)?)?$"
    ),
    re.S,
)
CREATE_CHAT_ARGS_REGEXP = re.compile(
    r"^(?P<chat_type>personal_chat|group_chat|channel)\s+"
    r"(?P<chat_name>.+?)(?P<shared_history>\s+shared_history)?$"
)
CREATE_MARKUP_ARGS_REGEXP = re.compile(
    r"^(?P<rows>\d+)\s+(?P<columns>\d+)"
    r"(\s+)?(?P<buttons_auto_adjust>buttons_auto_adjust)?$"
)
ENABLE_STEALTH_MODE_ARGS_REGEXP = re.compile(
    r"^(?P<burn_in>\d+)\s+(?P<expire_in>\d+)(\s+)?"
    r"(?P<disable_web>disable_web)?(\s+)?(?P<chat_id>[\w-]+)?$"
)
SEARCH_USER_REGEXP = re.compile(
    r"^(?P<by_huid>huid)\s+(?P<huid>[a-f0-9-]+)$"
    r"|^(?P<by_ad>ad)\s+((?P<ad_login>\S+)\s+(?P<ad_domain>\S+))$"
    r"|^(?P<by_email>email)\s+(?P<email>\S+@\S+\.\S+)$"
)
SPAM_ARGS_REGEXP = re.compile(r"^(?P<quantity>\d+)(\s+(?P<delay>\d+))?$")
