# AD Toolkit — enum & checks

# **CRÉÉ PAR : DAMONX**

**Résumé**  
Outil d'énumération et de vérification pour Active Directory — collecte LDAP/DNS, checks non destructifs, export JSON/HTML.

---

## ⚠️ Avertissement légal & éthique
Cet outil est destiné **aux hackers éthiques** (pentesters autorisés, chercheurs en sécurité, administrateurs). **N'utilisez pas ce projet sur des systèmes dont vous n'avez pas l'autorisation écrite explicite.** Toute utilisation non autorisée est de votre responsabilité.

---

## Fonctionnalités principales
- Enumération LDAP non destructive (naming contexts, comptes utilisateurs)  
- Découverte basique des contrôleurs de domaine (DNS SRV)  
- Checks simples (ex : comptes `password never expires`)  
- Export JSON et HTML, UI Streamlit optionnelle

---

## Installation rapide
1. Installer les dépendances :
```powershell
pip install -r requirements.txt
