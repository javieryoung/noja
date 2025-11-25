import requests
from django.template import Template, Context

def render_remote_template(template_url, context_dict):
    response = requests.get(template_url)
    response.raise_for_status()
    template_string = response.text
    template = Template(template_string)
    context = Context(context_dict)
    return template.render(context)
