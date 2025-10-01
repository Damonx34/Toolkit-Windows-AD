from ldap3 import Server, Connection, ALL, NTLM, SUBTREE, core
from rich import print
import socket
import json

def try_connect_ldap(domain, user=None, password=None, timeout=5):
    # Tentative de connexion LDAP (non-destructive)
    server = Server(domain, get_info=ALL, connect_timeout=timeout)
    if user and password:
        conn = Connection(server, user=user, password=password, authentication=NTLM, receive_timeout=10)
    else:
        conn = Connection(server)  # anonymous bind attempt
    try:
        conn.open()
        conn.bind()
        return conn
    except core.exceptions.LDAPExceptionError as e:
        print(f"[yellow]Impossible de binder LDAP : {e}[/]")
        return None

def ldap_enumerate(target, user=None, password=None):
    """
    Connecte au service LDAP du target et récupère des infos basiques.
    Retourne un dict avec les résultats.
    """
    res = {"target": target, "ldap": {"connected": False, "info": {}, "users": []}}
    conn = try_connect_ldap(target, user, password)
    if not conn or not conn.bound:
        return res

    res["ldap"]["connected"] = True

    # Récupérer le namingContext / baseDN
    server_info = conn.server.info
    res["ldap"]["info"]["server_name"] = str(server_info.name)
    res["ldap"]["info"]["vendor"] = server_info.vendor
    res["ldap"]["info"]["naming_contexts"] = server_info.naming_contexts

    # Exemple : rechercher les 10 premiers comptes utilisateurs (non-destructif)
    try:
        base = server_info.naming_contexts[0] if server_info.naming_contexts else None
        if base:
            conn.search(search_base=base,
                        search_filter='(objectClass=user)',
                        search_scope=SUBTREE,
                        attributes=["sAMAccountName", "displayName", "userAccountControl"],
                        size_limit=50)
            for entry in conn.entries:
                res["ldap"]["users"].append({
                    "sAMAccountName": str(entry.sAMAccountName) if "sAMAccountName" in entry else None,
                    "displayName": str(entry.displayName) if "displayName" in entry else None,
                    "uac": str(entry.userAccountControl) if "userAccountControl" in entry else None,
                })
    except Exception as e:
        print(f"[red]Erreur lors de la recherche LDAP: {e}[/]")

    conn.unbind()
    return res
