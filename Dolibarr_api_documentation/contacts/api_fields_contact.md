# Champs API retournés pour les contacts

Liste complète des champs disponibles dans les réponses de l'API Dolibarr pour les contacts (socpeople).

## Champs principaux

| Champ API | Type | Description |
|-----------|------|-------------|
| **id** / **rowid** | integer | ID unique du contact |
| **lastname** | string | Nom de famille (obligatoire) |
| **firstname** | string | Prénom |
| **civility_code** / **civility_id** | string | Code civilité (MR, MME, MLE, DR, PROF) |
| **civility** | string | Libellé de la civilité |
| **poste** | string | Poste / Fonction |
| **statut** | integer | Statut (0=inactif, 1=actif) |
| **priv** | integer | Visibilité (0=public, 1=privé) |
| **ref_ext** | string | Référence externe |

## Champs de contact

| Champ API | Type | Description |
|-----------|------|-------------|
| **email** | string | Adresse email |
| **phone** / **phone_pro** | string | Téléphone professionnel |
| **phone_mobile** | string | Téléphone mobile |
| **phone_perso** | string | Téléphone personnel |
| **fax** | string | Numéro de fax |
| **no_email** | integer | Désabonnement emails (0=actif, 1=désabonné) |
| **url** | string | Site web / URL |

## Champs adresse

| Champ API | Type | Description |
|-----------|------|-------------|
| **address** | string | Adresse postale |
| **zip** | string | Code postal |
| **town** | string | Ville |
| **state_id** / **fk_departement** | integer | ID du département/état |
| **state_code** | string | Code du département |
| **state** | string | Nom du département/état |
| **country_id** / **fk_pays** | integer | ID du pays |
| **country_code** | string | Code pays (ISO 3166-1 alpha-2) |
| **country** | string | Nom du pays |

## Champs tiers / société

| Champ API | Type | Description |
|-----------|------|-------------|
| **socid** / **fk_soc** | integer | ID du tiers associé |
| **thirdparty_name** | string | Nom du tiers |
| **thirdparty** | object | Objet tiers complet (parfois nettoyé) |

## Champs réseaux sociaux

| Champ API | Type | Description |
|-----------|------|-------------|
| **socialnetworks** | object/text | Réseaux sociaux (JSON) |
| **skype** | string | Pseudo Skype (déprécié, utiliser socialnetworks) |
| **twitter** | string | Pseudo Twitter (déprécié, utiliser socialnetworks) |
| **facebook** | string | Pseudo Facebook (déprécié, utiliser socialnetworks) |
| **linkedin** | string | Pseudo LinkedIn (déprécié, utiliser socialnetworks) |
| **jabberid** | string | ID Jabber (déprécié, utiliser socialnetworks) |

## Champs statut prospect

| Champ API | Type | Description |
|-----------|------|-------------|
| **fk_stcommcontact** | integer | Statut commercial du contact |
| **fk_prospectlevel** | string | Niveau de prospection |
| **prospectlevel** | string | Libellé du niveau de prospection |

## Champs personnels

| Champ API | Type | Description |
|-----------|------|-------------|
| **birthday** | integer | Date d'anniversaire (timestamp) |
| **default_lang** | string | Langue par défaut (ex: fr_FR, en_US) |
| **photo** | string | Nom du fichier photo |

## Champs notes et système

| Champ API | Type | Description |
|-----------|------|-------------|
| **note_public** | string | Notes publiques |
| **note_private** | string | Notes privées |
| **canvas** | string | Type de canvas |
| **entity** | integer | Entité multi-société |
| **import_key** | string | Clé d'import |

## Champs de dates

| Champ API | Type | Description |
|-----------|------|-------------|
| **date_creation** / **datec** | integer | Date de création (timestamp) |
| **date_modification** / **tms** | integer | Date modification (timestamp) |

## Champs utilisateur

| Champ API | Type | Description |
|-----------|------|-------------|
| **user_creation** / **fk_user_creat** | integer | ID utilisateur créateur |
| **user_creation_id** | integer | Alias de fk_user_creat |
| **user_modification** / **fk_user_modif** | integer | ID utilisateur modification |
| **user_modification_id** | integer | Alias de fk_user_modif |
| **user_id** | integer | ID utilisateur lié (si compte utilisateur) |

## Champs de comptage (avec includecount=1)

| Champ API | Type | Description |
|-----------|------|-------------|
| **ref_facturation** | integer | Nombre de factures liées |
| **ref_contrat** | integer | Nombre de contrats liés |
| **ref_commande** | integer | Nombre de commandes liées |
| **ref_propal** | integer | Nombre de propositions liées |

## Champs de rôles (avec includeroles=1)

| Champ API | Type | Description |
|-----------|------|-------------|
| **roles** | array | Liste des rôles du contact |

## Champs techniques (metadata)

| Champ API | Type | Description |
|-----------|------|-------------|
| **array_options** | array | Champs personnalisés (extrafields) |
| **validateFieldsErrors** | array | Erreurs de validation |
| **linked_objects** | null/array | Objets liés |
| **linkedObjectsIds** | null/array | IDs objets liés |
| **specimen** | integer | Indicateur spécimen |
| **oldcopy** | object | Copie originale (pour historique) |

## Champs nettoyés par l'API

Les champs suivants sont automatiquement supprimés de la réponse pour des raisons de sécurité :

- `total_ht`
- `total_tva`
- `total_localtax1`
- `total_localtax2`
- `total_ttc`
- `note` (utiliser note_public ou note_private)
- `lines`
- `thirdparty` (dans certains contextes)

## Codes de civilité

| Code | Description |
|------|-------------|
| **MR** | Monsieur |
| **MME** | Madame |
| **MLE** | Mademoiselle |
| **DR** | Docteur |
| **PROF** | Professeur |

## Valeurs de statut

| Valeur | Description |
|--------|-------------|
| **0** | Inactif |
| **1** | Actif |

## Valeurs de visibilité (priv)

| Valeur | Description |
|--------|-------------|
| **0** | Contact public (visible par tous) |
| **1** | Contact privé (visibilité restreinte) |

## Valeurs no_email

| Valeur | Description |
|--------|-------------|
| **0** | Peut recevoir des emails |
| **1** | Désabonné des emails de masse |

## ⚠️ IMPORTANT : Utilisation dans Fields

Pour le paramètre `Fields`, utiliser les noms API SANS préfixe :

```
✅ CORRECT: Fields: id,lastname,firstname,email,phone,socid
❌ FAUX: Fields: t.id,t.lastname,t.firstname
```

## Exemples d'utilisation

### Champs essentiels
```
id,lastname,firstname,email,phone,statut
```

### Avec adresse complète
```
id,lastname,firstname,email,address,zip,town,state,country
```

### Avec société
```
id,lastname,firstname,email,phone,socid,thirdparty_name
```

### Avec statut prospect
```
id,lastname,firstname,email,phone,fk_stcommcontact,fk_prospectlevel
```

### Complet
```
id,lastname,firstname,civility_code,poste,email,phone,phone_mobile,address,zip,town,state,country,socid,statut,priv,birthday,note_public
```

### Avec réseaux sociaux
```
id,lastname,firstname,email,phone,socialnetworks
```

### Avec dates système
```
id,lastname,firstname,email,date_creation,date_modification,user_creation,user_modification
```

## Format des champs complexes

### socialnetworks (JSON)

```json
{
  "linkedin": "john-doe",
  "twitter": "@johndoe",
  "facebook": "john.doe",
  "instagram": "@johndoe"
}
```

### array_options (champs personnalisés)

```json
{
  "options_custom_field1": "value1",
  "options_custom_field2": "value2"
}
```

## Notes techniques

- Les champs `socid` et `fk_soc` sont des alias (même valeur)
- Les champs `date_creation` et `datec` sont des alias
- Les champs `date_modification` et `tms` sont des alias
- Les timestamps sont en secondes depuis le 1er janvier 1970 (Unix timestamp)
- Le champ `socialnetworks` est stocké en JSON dans la base de données
- Les champs `skype`, `twitter`, `facebook`, `linkedin`, `jabberid` sont dépréciés et remplacés par le champ `socialnetworks`
- Le type de catégorie pour les contacts est 4 dans le système de catégories Dolibarr
