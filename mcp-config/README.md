# Configuration MCP pour Dolibarr

Ce dossier contient les fichiers de configuration nécessaires pour utiliser les serveurs MCP Dolibarr avec Claude code.

## Fichiers inclus

- **`dolibarr-mcp-servers.yaml`** - Catalogue MCP définissant les serveurs Dolibarr disponibles
- **`registry.yaml`** - Registre MCP pour enregistrer les serveurs
- **`install.sh`** - Script d'installation automatique (Linux/macOS)

## Serveurs MCP disponibles

### 1. Dolibarr Projects (`dolibarr_projects`)
Gestion des projets Dolibarr avec 6 outils :
- `dolibarr_get_project` - Obtenir les détails d'un projet
- `dolibarr_list_projects` - Lister tous les projets
- `dolibarr_create_project` - Créer un nouveau projet
- `dolibarr_update_project` - Mettre à jour un projet
- `dolibarr_delete_project` - Supprimer un projet
- `dolibarr_get_project_tasks` - Obtenir les tâches d'un projet

### 2. Dolibarr Tasks (`dolibarr_tasks`)
Gestion des tâches Dolibarr avec 4 outils :
- `dolibarr_get_task` - Obtenir les détails d'une tâche
- `dolibarr_create_task` - Créer une nouvelle tâche
- `dolibarr_modify_task` - Modifier une tâche
- `dolibarr_task_add_spenttime` - Ajouter du temps passé

## Installation

### Méthode 1 : Installation automatique (Recommandée)

```bash
# Depuis la racine du projet
cd mcp-config
chmod +x install.sh
./install.sh
```

Le script va :
1. Créer des backups de vos fichiers existants
2. Copier les configurations dans `~/.docker/mcp/catalogs/` et `~/.docker/mcp/`
3.  Vous demander de configurer les secrets

### Méthode 2 : Installation manuelle

#### Étape 1 : Copier les fichiers de configuration

```bash
# Créer le dossier si nécessaire
mkdir -p ~/.docker/mcp/catalogs

# Sauvegarder vos fichiers existants (optionnel)
cp ~/.docker/mcp/catalogs/dolibarr-mcp-servers.yaml ~/.docker/mcp/catalogs/dolibarr-mcp-servers.yaml.backup
cp ~/.docker/mcp/registry.yaml ~/.docker/mcp/registry.yaml.backup

# Copier les nouveaux fichiers
cp dolibarr-mcp-servers.yaml ~/.docker/mcp/catalogs/dolibarr-mcp-servers.yaml
cp registry.yaml ~/.docker/mcp/registry.yaml
```
#### Étape 2 : fichier de configuration  pour claude code dans ce projet : 

lancez claude-code à la racine de ce projet. Ce dernier liera le ficheir .mcp.json pour trouver les serveurs mcp disponibles dans ce projet.

#### Étape 3 : Construire les images Docker

```bash
# Depuis la racine du projet

# Construire l'image Projects
cd mcp-server-projects
docker build -t dolibarr-projects-mcp-server:latest .

# Construire l'image Tasks
cd ../mcp-server-tasks
docker build -t dolibarr-tasks-mcp-server:latest .
```

#### Étape 4 : Configurer les secrets Docker MCP

```bash
# Configurer l'URL de votre instance Dolibarr
docker mcp secret set DOLIBARR_URL="https://votre-dolibarr.com"

# Configurer votre clé API Dolibarr
docker mcp secret set DOLIBARR_API_KEY="votre_cle_api"

# Vérifier les secrets
docker mcp secret ls
```

**Où trouver votre clé API Dolibarr ?**
1. Connectez-vous à votre Dolibarr
2. Allez dans votre profil utilisateur
3. Onglet "API/Webhooks"
4. Générez une nouvelle clé API si nécessaire

#### Étape 5 : Importer le catalogue et activer les serveurs

**IMPORTANT** : Cette étape est cruciale ! Sans elle, les outils ne seront pas disponibles.

```bash
# Importer le catalogue Dolibarr MCP
docker mcp catalog import ~/.docker/mcp/catalogs/dolibarr-mcp-servers.yaml

# Vérifier que le catalogue est bien importé
docker mcp catalog ls

# Activer les serveurs
docker mcp server enable dolibarr_projects
docker mcp server enable dolibarr_tasks

# Vérifier que les serveurs sont actifs
docker mcp server list
```

#### Étape 6 : Redémarrer Claude Code

1. Quittez complètement Claude Code
2. Redémarrez Claude Code
3. Les 10 outils Dolibarr devraient maintenant être disponibles !

## Vérification

### 1. Vérifier que le catalogue est importé

```bash
docker mcp catalog ls
```

Vous devriez voir `dolibarr-mcp-servers: DolibarrMCP Servers` dans la liste.

### 2. Vérifier que les serveurs sont actifs

```bash
docker mcp server list
```

Vous devriez voir `dolibarr_projects` et `dolibarr_tasks` dans la liste.

### 3. Vérifier que les outils sont disponibles

```bash
docker mcp tools list
```

Vous devriez voir **10 outils Dolibarr** :
- 6 outils `dolibarr_*_project*` (Projects)
- 4 outils `dolibarr_*_task*` (Tasks)

### 4. Vérifier les secrets

```bash
docker mcp secret ls
```

Vous devriez voir `DOLIBARR_URL` et `DOLIBARR_API_KEY`.

### 5. Tester les serveurs

```bash
# Tester la liste des projets
docker mcp tools call dolibarr_list_projects

# Tester la récupération d'un projet spécifique (remplacez 1 par un ID réel)
docker mcp tools call dolibarr_get_project project_id=1

# Tester la récupération d'une tâche (remplacez 1 par un ID réel)
docker mcp tools call dolibarr_get_task task_id=1 includetimespent=0

# Créer un nouveau projet
docker mcp tools call dolibarr_create_project ref=TEST001 title="Mon projet test"

# Ajouter du temps passé à une tâche
docker mcp tools call dolibarr_task_add_spenttime task_id=1 date=2025-01-19 duration=2.5 note="Développement API"
```

## Utilisation dans Claude code

Une fois configuré, vous pouvez interagir avec Dolibarr en langage naturel :

### Exemples pour Projects

- "Liste tous mes projets Dolibarr"
- "Montre-moi les détails du projet 5"
- "Crée un nouveau projet appelé 'Site Web 2025' avec la référence PROJ-2025-001"
- "Mets à jour le budget du projet 3 à 50000 euros"

### Exemples pour Tasks

- "Montre-moi les détails de la tâche 15"
- "Crée une tâche 'Design UI' dans le projet 5 avec 8 heures prévues"
- "Mets la tâche 20 à 75% de progression"
- "Ajoute 3.5 heures de travail sur la tâche 12 pour hier"

## Dépannage

### Les outils n'apparaissent pas dans `docker mcp tools list`

**Symptôme** : Les serveurs apparaissent dans `docker mcp server list` mais les outils ne sont pas visibles.

**Solution** : Le catalogue n'est pas importé ou les serveurs ne sont pas activés.

```bash
# 1. Vérifier que le catalogue est importé
docker mcp catalog ls

# Si le catalogue n'apparaît pas, l'importer
docker mcp catalog import ~/.docker/mcp/catalogs/dolibarr-mcp-servers.yaml

# 2. Activer les serveurs
docker mcp server enable dolibarr_projects
docker mcp server enable dolibarr_tasks

# 3. Vérifier que les outils sont maintenant disponibles
docker mcp tools list
```

### Les images Docker ne sont pas trouvées

1. Vérifiez que les images Docker sont construites :
   ```bash
   docker images | grep dolibarr
   ```

2. Si les images n'existent pas, construisez-les :
   ```bash
   cd /chemin/vers/dolibarr-mcp-server/mcp-server-projects
   docker build -t dolibarr-projects-mcp-server:latest .

   cd ../mcp-server-tasks
   docker build -t dolibarr-tasks-mcp-server:latest .
   ```

### Problèmes de configuration

1. Vérifiez que les fichiers de configuration sont corrects :
   ```bash
   cat ~/.docker/mcp/catalogs/dolibarr-mcp-servers.yaml
   docker mcp catalog show dolibarr-mcp-servers
   ```

2. Redémarrez complètement Claude Code

### Erreurs d'authentification

1. Vérifiez que les secrets sont configurés :
   ```bash
   docker mcp secret ls
   ```

2. Vérifiez que l'URL Dolibarr n'a pas de slash final

3. Vérifiez que votre clé API est valide dans Dolibarr

4. Assurez-vous que le module "API/Web Services" est activé dans Dolibarr

### Erreurs de permissions

Assurez-vous que votre utilisateur Dolibarr a les permissions nécessaires :
- `projet->lire` - Lecture des projets/tâches
- `projet->creer` - Création/modification des projets/tâches
- `projet->supprimer` - Suppression des projets

## Structure du projet

```
dolibarr-mcp-server/
├── mcp-config/              # Configuration MCP (ce dossier)
│   ├── dolibarr-mcp-servers.yaml          # Catalogue des serveurs
│   ├── registry.yaml        # Registre MCP
│   ├── install.sh           # Script d'installation
│   └── README.md            # Ce fichier
├── mcp-server-projects/              # Serveur MCP Projects
│   ├── Dockerfile
│   ├── dolibarr_projects_server.py
│   └── README.md
├── mcp-server-tasks/        # Serveur MCP Tasks
│   ├── Dockerfile
│   ├── dolibarr_tasks_server.py
│   └── README.md
└── Dolibarr_api_documentation/  # Documentation API
    ├── projects.md
    ├── tasks.md
    ├── thirdparties.md
    ├── contacts.md
    ├── invoices.md
    └── products.md
```

## Contribuer

Pour ajouter de nouveaux serveurs MCP :

1. Créez un nouveau dossier `mcp-server-[nom]/`
2. Implémentez votre serveur en suivant les patterns existants
3. Ajoutez une entrée dans `mcp-config/dolibarr-mcp-servers.yaml`
4. Ajoutez une entrée dans `mcp-config/registry.yaml`
5. Mettez à jour ce README

## Support

Pour toute question ou problème :
- Ouvrez une issue sur GitHub
- Consultez la documentation API dans `Dolibarr_api_documentation/`
- Vérifiez les README des serveurs individuels

## Licence

MIT License




