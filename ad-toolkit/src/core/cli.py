import argparse
from rich import print
from enumeration.ldap_enum import ldap_enumerate
from reporting.report import save_json_report, save_html_report

def parse_args():
    p = argparse.ArgumentParser(description="AD Toolkit - enum & checks (labo only)")
    p.add_argument("target", help="Domain or IP of target (ex: corp.example.com)")
    p.add_argument("--user", help="Username for bind (optional)")
    p.add_argument("--password", help="Password for bind (optional)")
    p.add_argument("--out", help="Output JSON file", default="results.json")
    p.add_argument("--html", help="Also write HTML report (path)", default=None)
    return p.parse_args()

def app():
    args = parse_args()
    print(f"[bold blue]Lancement de l\\'enum sur[/] {args.target}")
    results = ldap_enumerate(args.target, args.user, args.password)
    save_json_report(results, args.out)
    if args.html:
        save_html_report(results, args.html)
        print(f"[green]HTML report written to[/] {args.html}")
    print(f"[green]Terminé. Résultats sauvegardés dans[/] {args.out}")
