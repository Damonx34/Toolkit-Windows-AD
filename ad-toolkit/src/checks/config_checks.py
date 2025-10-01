# src/checks/config_checks.py
# Checks de configuration AD (placeholder)
# Ajout d'une fonction run_all_checks pour l'UI

def sample_check(results):
    findings = []
    # Exemple trivial : si un user n'a pas de displayName
    users = results.get("ldap", {}).get("users", [])
    for u in users:
        if not u.get("displayName"):
            findings.append({
                "severity": "low",
                "message": f"User {u.get('sAMAccountName')} has no displayName"
            })
    return findings

def run_all_checks(results):
    """
    Exécute tous les checks configurés et retourne la liste des findings.
    """
    findings = []
    findings.extend(sample_check(results))
    # ici tu peux ajouter d'autres checks plus tard
    return findings
