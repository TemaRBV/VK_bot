import re
from generate_ticket import generate_ticket

re_name = re.compile(r'^[\w\-\s]{2,30}$')
re_email = re.compile(r'(\b[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+\b)')


def handler_name(text, context):
    match = re_name.match(text)
    if match:
        context['name'] = text
        return True
    else:
        return False


def handler_email(text, context):
    matches = re_email.findall(text)
    if len(matches) > 0:
        if len(matches) > 1:
            emails = ', '.join(matches)
            context['email'] = emails
            return True
        else:
            context['email'] = matches[0]
            return True
    else:
        return False


def generate_ticket_handler(text, context):
    return generate_ticket(name=context['name'], email=context['email'])
