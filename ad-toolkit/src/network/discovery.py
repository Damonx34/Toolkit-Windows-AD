import dns.resolver
from rich import print

def find_domain_controllers(domain):
    """
    Recherche les enregistrements SRV _ldap._tcp.dc._msdcs.<domain> pour récupérer les DCs.
    """
    srv_record = "_ldap._tcp.dc._msdcs." + domain
    try:
        answers = dns.resolver.resolve(srv_record, "SRV")
        dcs = []
        for r in answers:
            target = str(r.target).rstrip(".")
            port = r.port
            dcs.append({"host": target, "port": port})
        return dcs
    except Exception as e:
        print(f"[yellow]Erreur DNS SRV: {e}[/]")
        return []
