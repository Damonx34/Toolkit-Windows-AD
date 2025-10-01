# AD Toolkit — enum & checks (labo / pentest éducatif)

**Résumé rapide**  
AD Toolkit est un ensemble d'outils pédagogiques pour l'**énumération** et la **vérification** de configurations d'Active Directory. Il aide à collecter des informations (LDAP/DNS), exécuter des checks de sécurité non destructifs et générer des rapports JSON/HTML.

---

## ⚠️ Avertissement légal & éthique (à lire absolument)
Cet outil est conçu **pour les chercheurs en sécurité, étudiants, administrateurs et pentesteurs éthiques**.  
**N'utilisez pas ce projet sur des systèmes ou réseaux dont vous n'êtes pas propriétaire ou pour lesquels vous n'avez pas une autorisation écrite explicite.**

En pratique :
- Utilisez cet outil **uniquement** sur un environnement de test / labo ou avec une **autorisation écrite** du propriétaire de l'infrastructure.
- N'effectuez aucune action destructive, intrusives ou illégale.
- Toute utilisation non autorisée est de votre responsabilité et peut entraîner des conséquences légales.

---

## But pédagogique
- Apprendre les protocoles AD (LDAP, Kerberos, DNS) et les méthodes d'énumération.
- Détecter des mauvaises configurations (comptes non expirés, flags suspects, etc.).
- Produire des rapports pour des audits internes et exercices de remédiation.

---

## Fonctionnalités principales
- Enumération LDAP non destructive (naming contexts, comptes utilisateurs).
- Découverte basique de contrôleurs de domaine via DNS SRV.
- Checks automatiques simples (ex : comptes avec `password never expires`).
- Génération de rapports JSON et HTML.
- (Option) Interface Streamlit locale pour usage facilité.

---

## Installation rapide (Windows / PowerShell)
1. Cloner le repo / créer le dossier `ad-toolkit`.  
2. Créer & activer un venv :
```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
