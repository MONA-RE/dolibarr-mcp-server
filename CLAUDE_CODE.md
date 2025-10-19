# Utilisation avec Claude Code

Ce projet inclut une configuration `.mcp.json` pour utiliser les serveurs MCP Dolibarr directement dans Claude Code.

## Installation rapide

### 1. Prérequis

- Docker Desktop installé et en cours d'exécution
- Claude Code (version récente avec support MCP)
- Images Docker construites

### 2. Construire les images Docker

```bash
# Depuis la racine du projet

# Construire l'image Projects
cd mcp-server
docker build -t dolibarr-projects-mcp-server:latest .

# Construire l'image Tasks
cd ../mcp-server-tasks
docker build -t dolibarr-tasks-mcp-server:latest .
```

### 3. Configurer les variables d'environnement

```bash
# Copier le fichier d'exemple
cp .env.example .env

# Éditer le fichier .env avec vos valeurs
nano .env
```

Ou définir les variables dans votre shell :

```bash
# Linux/macOS
export DOLIBARR_URL="http://172.19.0.1/dev-smta/htdocs"
export DOLIBARR_API_KEY="votre_cle_api"

# Windows PowerShell
$env:DOLIBARR_URL="http://172.19.0.1/dev-smta/htdocs"
$env:DOLIBARR_API_KEY="votre_cle_api"
```

### 4. Utiliser dans Claude Code

Claude Code détectera automatiquement le fichier `.mcp.json` à la racine du projet.

**Méthode 1 : Automatique**
- Ouvrez le projet dans Claude Code
- Les serveurs MCP seront automatiquement disponibles

**Méthode 2 : Commande /mcp**
```
/mcp connect dolibarr-projects
/mcp connect dolibarr-tasks
```

## Outils disponibles

### Serveur Dolibarr Projects

- `dolibarr_get_project` - Obtenir les détails d'un projet
- `dolibarr_list_projects` - Lister tous les projets
- `dolibarr_create_project` - Créer un nouveau projet
- `dolibarr_update_project` - Mettre à jour un projet
- `dolibarr_delete_project` - Supprimer un projet
- `dolibarr_get_project_tasks` - Obtenir les tâches d'un projet

### Serveur Dolibarr Tasks

- `dolibarr_get_task` - Obtenir les détails d'une tâche
- `dolibarr_create_task` - Créer une nouvelle tâche
- `dolibarr_modify_task` - Modifier une tâche
- `dolibarr_task_add_spenttime` - Ajouter du temps passé

## Exemples d'utilisation

Dans Claude Code, vous pouvez utiliser le langage naturel :

```
"Liste tous mes projets Dolibarr"
"Crée un projet 'Site Web 2025' avec la référence PROJ-2025-001"
"Montre-moi les détails de la tâche 15 avec le temps passé"
"Ajoute 3.5 heures de travail sur la tâche 12 pour hier"
```

## Configuration du .mcp.json

Le fichier `.mcp.json` à la racine du projet définit deux serveurs MCP :

```json
{
  "mcpServers": {
    "dolibarr-projects": {
      "command": "docker",
      "args": ["run", "-i", "--rm", ...],
      "env": {
        "DOLIBARR_URL": "${DOLIBARR_URL}",
        "DOLIBARR_API_KEY": "${DOLIBARR_API_KEY}"
      }
    },
    "dolibarr-tasks": { ... }
  }
}
```

Les variables d'environnement sont lues depuis :
1. Fichier `.env` (si présent)
2. Variables d'environnement du système
3. Valeurs par défaut dans `.mcp.json`

## Dépannage

### Les serveurs ne se connectent pas

1. Vérifiez que Docker est en cours d'exécution
2. Vérifiez que les images sont construites :
   ```bash
   docker images | grep dolibarr
   ```

3. Vérifiez les variables d'environnement :
   ```bash
   echo $DOLIBARR_URL
   echo $DOLIBARR_API_KEY
   ```

### Erreurs d'authentification

1. Vérifiez que votre clé API est valide
2. Vérifiez que l'URL Dolibarr est accessible
3. Testez manuellement :
   ```bash
   docker run -i --rm \
     -e DOLIBARR_URL="votre_url" \
     -e DOLIBARR_API_KEY="votre_cle" \
     dolibarr-projects-mcp-server:latest
   ```

### Les outils n'apparaissent pas

1. Rechargez Claude Code
2. Vérifiez les logs MCP :
   - Menu Claude Code > Developer > Toggle MCP Logs
3. Vérifiez que le `.mcp.json` est valide (JSON bien formaté)

## Différences avec Claude Desktop

| Claude Code | Claude Desktop |
|-------------|----------------|
| Fichier `.mcp.json` dans le projet | Config globale dans `~/.config/Claude/` |
| Variables d'env du projet | Secrets Docker MCP |
| Détection automatique | Configuration manuelle du catalogue |
| Par projet | Global pour toutes les conversations |

## Développement

### Recharger après modifications

Après avoir modifié le code des serveurs :

```bash
# Reconstruire l'image
cd mcp-server  # ou mcp-server-tasks
docker build -t dolibarr-[projects|tasks]-mcp-server:latest .

# Recharger dans Claude Code
# Commande : Developer > Reload Window
```

### Logs et debugging

Pour voir les logs des serveurs MCP :

```bash
# Logs du conteneur Projects
docker logs mcp-dolibarr-projects

# Logs du conteneur Tasks
docker logs mcp-dolibarr-tasks
```

## Avantages de l'utilisation avec Claude Code

✅ **Configuration par projet** - Chaque projet peut avoir ses propres serveurs MCP
✅ **Détection automatique** - Pas de configuration globale nécessaire
✅ **Variables d'environnement** - Facilement personnalisables par projet
✅ **Développement rapide** - Rechargement simple après modifications
✅ **Isolation** - Conteneurs Docker isolés par session

## Ressources

- [Documentation MCP](https://docs.claude.com/en/docs/claude-code/mcp)
- [API Dolibarr](./Dolibarr_api_documentation/)
- [Serveur Projects](./mcp-server/README.md)
- [Serveur Tasks](./mcp-server-tasks/README.md)

## Contribution

Pour ajouter de nouveaux serveurs MCP au projet :

1. Créez un nouveau dossier `mcp-server-[nom]/`
2. Ajoutez une entrée dans `.mcp.json`
3. Documentez les outils dans ce fichier
4. Soumettez une Pull Request

---

**Note** : Ce projet utilise aussi une configuration pour Claude Desktop via `mcp-config/`.
Consultez `mcp-config/README.md` pour l'utilisation avec Claude Desktop.
