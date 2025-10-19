# Champs API retournés pour les tâches

Liste complète des champs disponibles dans les réponses de l'API Dolibarr pour les tâches.

## Champs principaux

| Champ API | Type | Description |
|-----------|------|-------------|
| **id** | string | ID unique de la tâche |
| **ref** | string | Référence de la tâche (ex: TK2509-0001) |
| **label** | string | Libellé de la tâche |
| **description** | string | Description de la tâche |
| **fk_project** | string | ID du projet parent |
| **fk_task_parent** | string | ID de la tâche parente (0 si racine) |
| **fk_statut** | string | Statut (0=brouillon, 1=validé) |
| **status** | string/null | Statut actif |

## Champs de dates

| Champ API | Type | Description |
|-----------|------|-------------|
| **date_c** | number | Date de création (timestamp) |
| **date_start** | number | Date de début prévue (timestamp) |
| **date_end** | number | Date de fin prévue (timestamp) |
| **datee** | string/null | Date de fin |

## Champs de suivi

| Champ API | Type | Description |
|-----------|------|-------------|
| **progress** | string | Avancement en pourcentage (0-100) |
| **duration_effective** | string | Durée effective en secondes |
| **planned_workload** | string | Charge planifiée en secondes |
| **priority** | string | Priorité de la tâche |

## Champs utilisateur

| Champ API | Type | Description |
|-----------|------|-------------|
| **fk_user_creat** | string | ID utilisateur créateur |
| **fk_user_valid** | string/null | ID utilisateur validateur |

## Champs budget et hiérarchie

| Champ API | Type | Description |
|-----------|------|-------------|
| **budget_amount** | string/null | Budget de la tâche |
| **project_budget_amount** | string/null | Budget du projet |
| **rang** | string | Ordre d'affichage |

## Champs temps passé

| Champ API | Type | Description |
|-----------|------|-------------|
| **timespent_min_date** | string/null | Date min temps passé |
| **timespent_max_date** | string/null | Date max temps passé |
| **timespent_total_duration** | string/null | Durée totale temps passé |
| **timespent_total_amount** | string/null | Montant total temps passé |
| **timespent_nblines** | string/null | Nombre de lignes temps passé |
| **timespent_thm** | string/null | Taux horaire moyen |

## Champs notes et système

| Champ API | Type | Description |
|-----------|------|-------------|
| **note_public** | string/null | Notes publiques |
| **note_private** | string/null | Notes privées |
| **entity** | string/null | Entité multi-société |
| **model_pdf** | string/null | Modèle PDF |
| **import_key** | string/null | Clé d'import |

## Champs techniques (metadata)

| Champ API | Type | Description |
|-----------|------|-------------|
| **array_options** | array | Options supplémentaires |
| **validateFieldsErrors** | array | Erreurs de validation |
| **specimen** | number | Indicateur spécimen |

## ⚠️ IMPORTANT : Utilisation dans Fields

Pour le paramètre 'Fields', utiliser les noms API SANS préfixe :

'''
✅ CORRECT: Fields: id,ref,label,progress,fk_project,date_start
❌ FAUX: Fields: t.id,t.ref,t.label
'''

## Exemples d'utilisation

### Champs essentiels
'''
id,ref,label,progress,fk_project
'''

### Avec dates et durée
'''
id,ref,label,date_start,date_end,duration_effective,planned_workload
'''

### Avec budget et avancement
'''
id,ref,label,progress,budget_amount,priority
'''

### Avec temps passé
'''
id,ref,label,timespent_total_duration,timespent_nblines
'''

### Complet
'''
id,ref,label,description,fk_project,fk_task_parent,progress,date_start,date_end,duration_effective,planned_workload,budget_amount,priority,note_public
'''
