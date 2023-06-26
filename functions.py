
from user_agents import parse


def filter_request(request):
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
