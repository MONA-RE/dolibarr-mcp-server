# Champs MySQL de la table llx_projet

Liste complète des champs disponibles dans la base MySQL pour les projets.

## Champs principaux

| Champ MySQL | Type | Description |
|------------|------|-------------|
| **t.rowid** | int(11) | ID unique du projet |
| **t.ref** | varchar(50) | Référence du projet |
| **t.title** | varchar(255) | Titre du projet |
| **t.description** | text | Description du projet |
| **t.fk_soc** | int(11) | ID du tiers associé |
| **t.fk_statut** | int(11) | Statut du projet (0=brouillon, 1=validé) |
| **t.public** | int(11) | Projet public (0=non, 1=oui) |

## Champs de dates

| Champ MySQL | Type | Description |
|------------|------|-------------|
| **t.datec** | datetime | Date de création |
| **t.dateo** | date | Date de début du projet |
| **t.datee** | date | Date de fin du projet |
| **t.date_close** | datetime | Date de clôture |
| **t.tms** | timestamp | Dernière modification |

## Champs utilisateur

| Champ MySQL | Type | Description |
|------------|------|-------------|
| **t.fk_user_creat** | int(11) | ID utilisateur créateur |
| **t.fk_user_modif** | int(11) | ID utilisateur modificateur |
| **t.fk_user_close** | int(11) | ID utilisateur ayant clos le projet |

## Champs opportunité commerciale

| Champ MySQL | Type | Description |
|------------|------|-------------|
| **t.fk_opp_status** | int(11) | Statut opportunité |
| **t.opp_percent** | double(5,2) | Pourcentage opportunité |
| **t.opp_amount** | double(24,8) | Montant opportunité |
| **t.fk_opp_status_end** | int(11) | Statut final opportunité |

## Champs budget et usage

| Champ MySQL | Type | Description |
|------------|------|-------------|
| **t.budget_amount** | double(24,8) | Budget du projet |
| **t.usage_opportunity** | int(11) | Usage opportunité (0/1) |
| **t.usage_task** | int(11) | Usage tâches (0/1) |
| **t.usage_bill_time** | int(11) | Usage facturation temps (0/1) |
| **t.usage_organize_event** | int(11) | Usage organisation événement (0/1) |

## Champs événements

| Champ MySQL | Type | Description |
|------------|------|-------------|
| **t.accept_conference_suggestions** | int(11) | Accepte suggestions conférences (0/1) |
| **t.accept_booth_suggestions** | int(11) | Accepte suggestions stands (0/1) |
| **t.max_attendees** | int(11) | Nombre max participants |
| **t.price_registration** | double(24,8) | Prix inscription |
| **t.price_booth** | double(24,8) | Prix stand |

## Champs notes et système

| Champ MySQL | Type | Description |
|------------|------|-------------|
| **t.note_private** | text | Notes privées |
| **t.note_public** | text | Notes publiques |
| **t.entity** | int(11) | Entité multi-société |
| **t.email_msgid** | varchar(175) | Message ID email |
| **t.model_pdf** | varchar(255) | Modèle PDF |
| **t.last_main_doc** | varchar(255) | Dernier document principal |
| **t.import_key** | varchar(14) | Clé d'import |

## ⚠️ IMPORTANT : Utilisation dans sqlfilters

Pour les filtres SQL, utiliser TOUJOURS le préfixe `t.` :

```
✅ CORRECT: (t.title:like:'%projet%')
❌ FAUX: (title:like:'%projet%')

✅ CORRECT: (t.fk_statut:=:1)
❌ FAUX: (status:=:1)
```
