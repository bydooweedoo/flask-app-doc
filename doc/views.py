"""
flask-app-doc
-------------

Web HTTP routes documentation generator.
"""
from operator import itemgetter
from flask import Blueprint, render_template


class DocBlueprint(Blueprint):
    """
    Documentation blueprint.
    """
    app = None

    def register(self, app, options, first_registration=False):
        """
        Override register to save given app.
        """
        DocBlueprint.app = app
        return super(DocBlueprint,
                     self).register(app, options, first_registration)


__documentation__ = DocBlueprint('doc', __name__,
                                 url_prefix='/doc',
                                 template_folder='templates',
                                 static_folder='static',
                                 static_url_path='/static')


def get_rule_doc(rule):
    """
    Return documentation from given rule.
    """
    views = DocBlueprint.app.view_functions
    if views.get(rule.endpoint):
        return views.get(rule.endpoint).__doc__.lstrip()
    return



@__documentation__.route('/')
def get_doc():
    """
    Return all documentation for project.
    """
    rules = []
    sections = []
    for rule in DocBlueprint.app.url_map.iter_rules():
        section = rule.rule.split('/')[1]
        if section not in sections:
            sections.append(section)
        rules.append({'url': rule.rule,
                      'section': section,
                      'doc': get_rule_doc(rule) or ''})
    sections.sort()
    rules.sort(key=itemgetter('url'))
    return render_template('rules.html', rules=rules, sections=sections)
