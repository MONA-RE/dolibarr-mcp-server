# Script de Rebuild et Restart - MCP Dolibarr

## Description

Le script `rebuild_and_restart.sh` permet de reconstruire automatiquement les serveurs MCP Dolibarr (projets et tâches) et de redémarrer le gateway MCP pour une utilisation avec n8n.

## Quand utiliser ce script ?

Utilisez ce script après avoir modifié :
- ✅ Le code des serveurs MCP (`dolibarr_projects_server.py` ou `dolibarr_tasks_server.py`)
- ✅ Les dépendances Python (`requirements.txt`)
- ✅ La configuration du Dockerfile
- ✅ Toute modification nécessitant une reconstruction des images Docker

## Usage

### Mode Quick (Recommandé)

**Rebuild rapide + Restart sans arrêt complet**

```bash
cd /home/teddy/docker-workspace/dolibarr-mcp-server/mcp-gateway-standalone
./rebuild_and_restart.sh --quick
```

ou simplement :

```bash
./rebuild_and_restart.sh
```

**Ce mode :**
- ✅ Reconstruit les images Docker (projects + tasks)
- ✅ Redémarre le gateway sans interruption de service
- ⚡ Rapide (~ 10-15 secondes)

### Mode Full

**Arrêt complet + Rebuild + Redémarrage**

```bash
./rebuild_and_restart.sh --full
```

**Ce mode :**
- ⬇️ Arrête complètement le gateway
- 🔨 Reconstruit les images Docker
- ⬆️ Redémarre le gateway
- ⏱️ Plus long (~ 20-30 secondes)

### Aide

```bash
./rebuild_and_restart.sh --help
```

## Exemple de sortie

```
╔══════════════════════════════════════════════════════════╗
║  MCP Dolibarr - Rebuild & Restart                       ║
╚══════════════════════════════════════════════════════════╝

✓ Configuration valide
  DOLIBARR_URL: http://dev-smta/htdocs
  API Key: S3KXYQ1og1...

═══ Mode QUICK: Rebuild + Restart ═══

[1/3] Construction des images MCP...
      - dolibarr-projects-mcp-server:latest
      - dolibarr-tasks-mcp-server:latest
✓ Images construites

[2/3] Redémarrage du gateway...
✓ Gateway redémarré

[3/3] Vérification du démarrage...
═══ Vérification finale ═══

✓ Container mcp_dolibarr est en cours d'exécution
  Container ID: f59d709dbcaa

Images MCP disponibles:
  ✓ dolibarr-projects-mcp-server:latest
  ✓ dolibarr-tasks-mcp-server:latest

✓ Port 8811 exposé correctement

╔══════════════════════════════════════════════════════════╗
║  Configuration n8n                                      ║
╠══════════════════════════════════════════════════════════╣
║  URL du MCP Gateway:                                   ║
║    http://localhost:8811/sse                          ║
║                                                          ║
║  Outils MCP disponibles:                               ║
║    • dolibarr_projects (8 outils)                      ║
║    • dolibarr_tasks (4 outils)                         ║
╚══════════════════════════════════════════════════════════╝

✓ Rebuild et redémarrage terminés avec succès!
```

## Workflow complet après modification du code

### Exemple : Correction d'un bug dans le serveur tasks

```bash
# 1. Modifier le code
vim dolibarr-mcp-server/mcp-server-tasks/dolibarr_tasks_server.py

# 2. Rebuild et restart
cd dolibarr-mcp-server/mcp-gateway-standalone
./rebuild_and_restart.sh

# 3. Vérifier les logs
docker logs mcp_dolibarr -f

# 4. Tester dans n8n
# L'agent MONA_IA devrait maintenant utiliser la nouvelle version
```

## Vérifications effectuées par le script

Le script vérifie automatiquement :

1. ✅ **Docker accessible** - Docker daemon est running
2. ✅ **Fichier .env présent** - Configuration des secrets
3. ✅ **Variables d'environnement** - DOLIBARR_URL et DOLIBARR_API_KEY
4. ✅ **Images construites** - dolibarr-projects-mcp-server et dolibarr-tasks-mcp-server
5. ✅ **Container running** - mcp_dolibarr est démarré
6. ✅ **Port exposé** - Port 8811 accessible
7. ✅ **Logs du gateway** - Pas d'erreurs au démarrage

## Erreurs courantes

### Erreur: Docker n'est pas accessible

```bash
✗ Erreur: Docker n'est pas accessible
Vérifiez que Docker est démarré et que vous avez les permissions nécessaires
```

**Solution :** Démarrez Docker Desktop ou vérifiez vos permissions.

### Erreur: Fichier .env manquant

```bash
✗ Erreur: Fichier .env manquant
Créez un fichier .env avec:
  DOLIBARR_URL=http://votre-dolibarr
  DOLIBARR_API_KEY=votre_cle_api
```

**Solution :** Créez un fichier `.env` dans le dossier `mcp-gateway-standalone/`

### Container ne démarre pas

Si le container `mcp_dolibarr` ne démarre pas, le script affichera automatiquement les 20 dernières lignes de logs pour diagnostic.

## Commandes utiles après le rebuild

```bash
# Voir les logs en temps réel
docker logs mcp_dolibarr -f

# Arrêter le gateway
cd docker-workspace/dolibarr-mcp-server/mcp-gateway-standalone
docker compose down

# Voir les containers MCP
docker ps | grep dolibarr

# Voir les images MCP
docker images | grep dolibarr
```

## Configuration n8n

Après le rebuild, assurez-vous que votre workflow n8n pointe vers :

**URL du MCP Gateway :** `http://localhost:8811/sse`

### Workflow n8n recommandé

```
Trigger Chat → Agent AI → MCP Client Tool → Response
```

**Configuration du MCP Client Tool :**
- URL : `http://localhost:8811/sse`
- Transport : SSE
- Outils disponibles : 12 outils (8 projects + 4 tasks)

## Référence rapide

| Commande | Usage |
|----------|-------|
| `./rebuild_and_restart.sh` | Rebuild rapide (mode par défaut) |
| `./rebuild_and_restart.sh --quick` | Rebuild rapide explicite |
| `./rebuild_and_restart.sh --full` | Rebuild complet avec arrêt |
| `./rebuild_and_restart.sh --help` | Affiche l'aide |
| `docker logs mcp_dolibarr -f` | Voir les logs en temps réel |
| `docker compose down` | Arrêter le gateway |

## Maintenance

### Nettoyage des anciennes images

Si vous voulez nettoyer les anciennes images Docker non utilisées :

```bash
# Supprimer les images Docker non utilisées
docker image prune -a

# Supprimer uniquement les images MCP anciennes
docker images | grep dolibarr | grep "<none>" | awk '{print $3}' | xargs docker rmi
```

## Support

Pour toute question ou problème :
1. Consultez les logs : `docker logs mcp_dolibarr -f`
2. Vérifiez la configuration dans `compose.yml`
3. Vérifiez le fichier `.env`
4. Consultez le fichier `readme.md` pour la documentation complète

## Licence

MIT License
