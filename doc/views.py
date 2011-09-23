"""
Web HTTP routes documentation generator.
"""
from operator import itemgetter
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from yourapp import __app__


__documentation__ = Blueprint('doc', __name__, \
                                  url_prefix='/doc', \
                                  template_folder='templates', \
                                  static_folder='static', \
                                  static_url_path='/static')


def get_rule_doc(rule):
    """
    Return documentation from given rule.
    """
    views = __app__.view_functions
    if views.get(rule.endpoint) is not None:
        return views.get(rule.endpoint).__doc__.lstrip()
    return ''



@__documentation__.route('/')
def get_doc():
    """
    Return all documentation for project.
    """
    rules = []
    sections = []
    for rule in __app__.url_map.iter_rules():
        section = rule.rule.split('/')[1]
        if section not in sections:
            sections.append(section)
        rules.append({'url': rule.rule, \
                          'section': section, \
                          'doc': get_rule_doc(rule)})
    sections.sort()
    rules.sort(key=itemgetter('url'))
    print repr(rules)
    try:
        return render_template('rules.html', rules=rules, sections=sections)
    except TemplateNotFound:
        abort(404)
