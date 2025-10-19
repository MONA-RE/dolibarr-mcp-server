# Champs MySQL de la table llx_projet_task

Liste complète des champs disponibles dans la base MySQL pour les tâches.

## Champs principaux

| Champ MySQL | Type | Description |
|------------|------|-------------|
| **t.rowid** | int(11) | ID unique de la tâche |
| **t.ref** | varchar(50) | Référence de la tâche |
| **t.fk_projet** | int(11) | ID du projet parent (OBLIGATOIRE) |
| **t.fk_task_parent** | int(11) | ID de la tâche parente (0 si racine) |
| **t.label** | varchar(255) | Libellé de la tâche (OBLIGATOIRE) |
| **t.description** | text | Description de la tâche |
| **t.fk_statut** | smallint(6) | Statut de la tâche (0=brouillon, 1=validé) |
| **t.status** | int(11) | Statut actif (0=inactif, 1=actif) |

## Champs de dates

| Champ MySQL | Type | Description |
|------------|------|-------------|
| **t.datec** | datetime | Date de création |
| **t.dateo** | datetime | Date de début prévue |
| **t.datee** | datetime | Date de fin prévue |
| **t.datev** | datetime | Date de validation |
| **t.tms** | timestamp | Dernière modification |

## Champs de suivi

| Champ MySQL | Type | Description |
|------------|------|-------------|
| **t.progress** | int(11) | Avancement (0-100%) |
| **t.duration_effective** | double | Durée effective (en secondes) |
| **t.planned_workload** | double | Charge de travail planifiée (en secondes) |
| **t.priority** | int(11) | Priorité de la tâche |

## Champs utilisateur

| Champ MySQL | Type | Description |
|------------|------|-------------|
| **t.fk_user_creat** | int(11) | ID utilisateur créateur |
| **t.fk_user_modif** | int(11) | ID utilisateur modificateur |
| **t.fk_user_valid** | int(11) | ID utilisateur validateur |

## Champs budget et hiérarchie

| Champ MySQL | Type | Description |
|------------|------|-------------|
| **t.budget_amount** | double(24,8) | Budget de la tâche |
| **t.rang** | int(11) | Ordre d'affichage |

## Champs notes et système

| Champ MySQL | Type | Description |
|------------|------|-------------|
| **t.note_private** | text | Notes privées |
| **t.note_public** | text | Notes publiques |
| **t.entity** | int(11) | Entité multi-société |
| **t.model_pdf** | varchar(255) | Modèle PDF |
| **t.import_key** | varchar(14) | Clé d'import |

## ⚠️ IMPORTANT : Utilisation dans sqlfilters

Pour les filtres SQL, utiliser TOUJOURS le préfixe `t.` :

```
✅ CORRECT: (t.label:like:'%développement%')
❌ FAUX: (label:like:'%développement%')

✅ CORRECT: (t.fk_statut:=:1)
❌ FAUX: (statut:=:1)

✅ CORRECT: (t.fk_projet:=:5)
❌ FAUX: (fk_project:=:5)
```

## Exemples de filtres

### Tâches d'un projet spécifique
```sql
(t.fk_projet:=:5)
```

### Tâches avec avancement supérieur à 50%
```sql
(t.progress:>:50)
```

### Tâches validées et actives
```sql
(t.fk_statut:=:1) and (t.status:=:1)
```

### Tâches avec priorité élevée
```sql
(t.priority:>=:3)
```
