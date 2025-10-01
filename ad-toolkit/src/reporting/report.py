import json
from jinja2 import Template

def save_json_report(data, path="results.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# petit HTML report (optionnel)
HTML_TMPL = """
<html><head><meta charset="utf-8"><title>AD Toolkit Report</title></head><body>
<h1>Report - {{ target }}</h1>
{% if ldap.connected %}
<h2>LDAP Info</h2>
<ul>
{% for k,v in ldap.info.items() %}
  <li><strong>{{ k }}:</strong> {{ v }}</li>
{% endfor %}
</ul>
<h3>Users sample</h3>
<ul>
{% for u in ldap.users %}
  <li>{{ u.sAMAccountName }}  {{ u.displayName }}</li>
{% endfor %}
</ul>
{% else %}
<p>LDAP non reachable</p>
{% endif %}
</body></html>
"""

def save_html_report(data, path="report.html"):
    tmpl = Template(HTML_TMPL)
    with open(path, "w", encoding="utf-8") as f:
        f.write(tmpl.render(**data))
