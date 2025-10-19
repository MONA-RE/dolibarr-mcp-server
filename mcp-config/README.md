# Configuration MCP pour Dolibarr

Ce dossier contient les fichiers de configuration nécessaires pour utiliser les serveurs MCP Dolibarr avec Claude Desktop.

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
3. Vérifier que Claude Desktop est configuré
4. Vous demander de configurer les secrets

### Méthode 2 : Installation manuelle

#### Étape 1 : Copier les fichiers de configuration

```bash
# Créer le dossier si nécessaire
mkdir -p ~/.docker/mcp/catalogs

# Sauvegarder vos fichiers existants (optionnel)
cp ~/.docker/mcp/catalogs/custom.yaml ~/.docker/mcp/catalogs/custom.yaml.backup
cp ~/.docker/mcp/registry.yaml ~/.docker/mcp/registry.yaml.backup

# Copier les nouveaux fichiers
cp custom.yaml ~/.docker/mcp/catalogs/custom.yaml
cp registry.yaml ~/.docker/mcp/registry.yaml
```

#### Étape 2 : Configurer Claude Desktop

Éditez le fichier de configuration de Claude Desktop :
- **Linux** : `~/.config/Claude/claude_desktop_config.json`
- **macOS** : `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows** : `%APPDATA%\Claude\claude_desktop_config.json`

Assurez-vous que votre configuration inclut le catalogue custom :

```json
{
  "mcpServers": {
    "mcp-toolkit-gateway": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-v", "/var/run/docker.sock:/var/run/docker.sock",
        "-v", "[YOUR_HOME]/.docker/mcp:/mcp",
        "docker/mcp-gateway",
        "--catalog=/mcp/catalogs/docker-mcp.yaml",
        "--catalog=/mcp/catalogs/custom.yaml",
        "--config=/mcp/config.yaml",
        "--registry=/mcp/registry.yaml",
        "--tools-config=/mcp/tools.yaml",
        "--transport=stdio"
      ]
    }
  }
}
```

**Important** : Remplacez `[YOUR_HOME]` par :
- Linux : `/home/votre_nom_utilisateur`
- macOS : `/Users/votre_nom_utilisateur`
- Windows : `C:\\Users\\votre_nom_utilisateur` (doubles backslashes)

#### Étape 3 : Construire les images Docker

```bash
# Depuis la racine du projet

# Construire l'image Projects
cd mcp-server
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

#### Étape 5 : Redémarrer Claude Desktop

1. Quittez complètement Claude Desktop
2. Redémarrez Claude Desktop
3. Les outils Dolibarr devraient maintenant être disponibles !

## Vérification

### Vérifier que les serveurs sont enregistrés

```bash
docker mcp server list
```

Vous devriez voir `dolibarr_projects` et `dolibarr_tasks` dans la liste.

### Vérifier les secrets

```bash
docker mcp secret ls
```

Vous devriez voir `DOLIBARR_URL` et `DOLIBARR_API_KEY`.

### Tester les serveurs

```bash
# Tester le serveur Projects
docker run -i --rm \
  -e DOLIBARR_URL="$DOLIBARR_URL" \
  -e DOLIBARR_API_KEY="$DOLIBARR_API_KEY" \
  dolibarr-projects-mcp-server:latest \
  <<< '{"jsonrpc":"2.0","method":"tools/list","id":1}'

# Tester le serveur Tasks
docker run -i --rm \
  -e DOLIBARR_URL="$DOLIBARR_URL" \
  -e DOLIBARR_API_KEY="$DOLIBARR_API_KEY" \
  dolibarr-tasks-mcp-server:latest \
  <<< '{"jsonrpc":"2.0","method":"tools/list","id":1}'
```

## Utilisation dans Claude Desktop

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

### Les outils n'apparaissent pas

1. Vérifiez que les images Docker sont construites :
   ```bash
   docker images | grep dolibarr
   ```

2. Vérifiez que les fichiers de configuration sont corrects :
   ```bash
   cat ~/.docker/mcp/catalogs/custom.yaml
   cat ~/.docker/mcp/registry.yaml
   ```

3. Vérifiez les logs Claude Desktop

4. Redémarrez complètement Claude Desktop

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
│   ├── custom.yaml          # Catalogue des serveurs
│   ├── registry.yaml        # Registre MCP
│   ├── install.sh           # Script d'installation
│   └── README.md            # Ce fichier
├── mcp-server/              # Serveur MCP Projects
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
3. Ajoutez une entrée dans `mcp-config/custom.yaml`
4. Ajoutez une entrée dans `mcp-config/registry.yaml`
5. Mettez à jour ce README

## Support

Pour toute question ou problème :
- Ouvrez une issue sur GitHub
- Consultez la documentation API dans `Dolibarr_api_documentation/`
- Vérifiez les README des serveurs individuels

## Licence

MIT License
