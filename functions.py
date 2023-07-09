
from user_agents import parse
import jwt


def filter_request_agent(request):
    user_agent_string = request.user_agent.string
    user_agent = parse(user_agent_string)
    if user_agent.browser.family == 'Edge':
        browser = 'Microsoft Edge'
    elif user_agent.browser.family == 'Chrome':
        browser = 'Google Chrome'
    elif user_agent.browser.family == 'Firefox':
        browser = 'Mozilla Firefox'
    elif user_agent.browser.family == 'Safari':
        browser = 'Apple Safari'
    elif user_agent.browser.family == 'Opera':
        browser = 'Opera'
    elif user_agent.browser.family == 'IE':
        browser = 'Internet Explorer'
    else:
        browser = 'Unknown'
    return browser


def get_user_from_token(token: str, secret_key: str) -> None | str:
    try:
        decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'])
        # Assuming the user information is stored under the 'user' key
        user = decoded_token.get('public_id')
        return user
    except jwt.DecodeError:
        # Handle decoding error
        return None
    except jwt.ExpiredSignatureError:
        # Handle expired token error
        return None
