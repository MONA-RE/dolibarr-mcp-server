# Champs API retournés pour les projets

Liste complète des champs disponibles dans les réponses de l'API Dolibarr pour les projets.

## Champs principaux

| Champ API | Type | Description |
|-----------|------|-------------|
| **id** | string | ID unique du projet |
| **ref** | string | Référence du projet (ex: PJ2508-0001) |
| **title** | string | Titre du projet |
| **description** | string | Description du projet |
| **ref_ext** | string | Référence externe |
| **status** / **statut** | string | Statut (0=brouillon, 1=validé) |
| **public** | string | Projet public (0=non, 1=oui) |

## Champs tiers / société

| Champ API | Type | Description |
|-----------|------|-------------|
| **socid** | string | ID du tiers associé |
| **thirdparty_name** | string | Nom du tiers |

## Champs de dates

| Champ API | Type | Description |
|-----------|------|-------------|
| **date_creation** / **date_c** | number | Date de création (timestamp) |
| **date_modification** / **date_m** | number | Date modification (timestamp) |
| **date_start** / **dateo** | number/null | Date de début (timestamp) |
| **date_end** / **datee** | string/null | Date de fin |
| **date_close** | string | Date de clôture |

## Champs utilisateur

| Champ API | Type | Description |
|-----------|------|-------------|
| **user_author_id** | string | ID utilisateur créateur |
| **user_creation_id** | string/null | ID utilisateur création |
| **user_modification_id** | string | ID utilisateur modification |
| **user_close_id** / **fk_user_close** | string/null | ID utilisateur clôture |

## Champs opportunité

| Champ API | Type | Description |
|-----------|------|-------------|
| **opp_status** / **fk_opp_status** | string/null | Statut opportunité |
| **opp_percent** | string/null | Pourcentage opportunité |
| **opp_amount** | string/null | Montant opportunité |

## Champs budget et usage

| Champ API | Type | Description |
|-----------|------|-------------|
| **budget_amount** | string/null | Budget du projet |
| **usage_opportunity** | number | Usage opportunité (0/1) |
| **usage_task** | number | Usage tâches (0/1) |
| **usage_bill_time** | number | Usage facturation temps (0/1) |
| **usage_organize_event** | number | Usage organisation événement (0/1) |

## Champs événements

| Champ API | Type | Description |
|-----------|------|-------------|
| **accept_conference_suggestions** | number | Accepte suggestions conférences (0/1) |
| **accept_booth_suggestions** | number | Accepte suggestions stands (0/1) |
| **max_attendees** | string/null | Nombre max participants |
| **price_registration** | string/null | Prix inscription |
| **price_booth** | string/null | Prix stand |

## Champs notes et système

| Champ API | Type | Description |
|-----------|------|-------------|
| **note_public** | string/null | Notes publiques |
| **note_private** | string/null | Notes privées |
| **entity** | string | Entité multi-société |
| **model_pdf** | string/null | Modèle PDF |
| **last_main_doc** | string/null | Dernier document principal |
| **import_key** | string/null | Clé d'import |
| **email_msgid** | string/null | Message ID email |

## Champs techniques (metadata)

| Champ API | Type | Description |
|-----------|------|-------------|
| **array_options** | array | Options supplémentaires |
| **validateFieldsErrors** | array | Erreurs de validation |
| **linked_objects** | null | Objets liés |
| **linkedObjectsIds** | null | IDs objets liés |
| **specimen** | number | Indicateur spécimen |

## ⚠️ IMPORTANT : Utilisation dans Fields

Pour le paramètre `Fields`, utiliser les noms API SANS préfixe :

'
✅ CORRECT: Fields: id,ref,title,status,socid,date_start
❌ FAUX: Fields: t.id,t.ref,t.title
'

## Exemples d'utilisation

### Champs essentiels
'
id,ref,title,status,socid
'

### Avec dates et budget
'
id,ref,title,status,date_start,date_end,budget_amount
'

### Avec opportunité
'
id,ref,title,opp_status,opp_amount,opp_percent
'

### Complet
'
id,ref,title,description,status,socid,thirdparty_name,date_start,date_end,budget_amount,opp_amount,usage_task,note_public
'
