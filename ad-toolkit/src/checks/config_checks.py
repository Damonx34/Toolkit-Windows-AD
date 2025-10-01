# Fichier placeholder pour checks de configuration AD
# Ici on ajoutera des fonctions qui examinent les résultats de ldap_enumerate()
# et retournent des "findings" (critique/medium/low) avec recommandations.

def sample_check(results):
    findings = []
    # Exemple: si on a des users, flagged si plus de X sans displayName (exemple trivial)
    users = results.get("ldap", {}).get("users", [])
    for u in users:
        if not u.get("displayName"):
            findings.append({
                "severity": "low",
                "message": f"User {u.get('sAMAccountName')} has no displayName"
            })
    return findings
