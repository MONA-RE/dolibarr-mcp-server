# Dolibarr MCP Server

## Objectif

Ce projet vise à créer un serveur MCP (Model Context Protocol) pour Dolibarr, permettant une intégration transparente avec des outils d'IA et d'automatisation. Le serveur MCP expose les fonctionnalités de Dolibarr via ses API REST et les rend accessibles via le protocole MCP.

## Architecture

Ce serveur MCP expose les fonctionnalités de Dolibarr via une interface SSE (Server-Sent Events), permettant une intégration directe avec les clients MCP.

### Composants

- **Dolibarr API**: API REST native de Dolibarr exposant les fonctionnalités de gestion (projets, tâches, tiers, etc.)
- **MCP Server**: Serveur implémentant le protocole MCP pour Dolibarr, accessible via SSE

## Fonctionnalités

Le serveur MCP permet d'interagir avec Dolibarr pour:

- Gérer les projets (création, modification, suppression, consultation)
- Gérer les tâches associées aux projets
- Consulter et gérer les tiers (clients, fournisseurs)
- Accéder aux autres modules Dolibarr via leur API

## Documentation

### Documentation API Dolibarr

La documentation complète des API Dolibarr est disponible dans le dossier [`Dolibarr_api_documentation/`](./Dolibarr_api_documentation/):

- [Vue d'ensemble de l'API](./Dolibarr_api_documentation/README.md)
- [API Projects (Projets)](./Dolibarr_api_documentation/projects.md)

### Authentification

L'API Dolibarr utilise une clé API (DOLAPIKEY) pour l'authentification. Cette clé doit être générée depuis l'interface Dolibarr et configurée dans le serveur MCP.

## Prérequis

- Docker et Docker Compose
- Une instance Dolibarr fonctionnelle avec le module API/Web Services activé
- Un serveur MCP Dolibarr accessible via SSE

## Installation

```bash
# Cloner le repository
git clone <repository-url>
cd dolibarr-mcp-server

# Configuration (à venir)
# ...

# Lancement du serveur MCP (à venir)
# ...
```

## Configuration

Le serveur MCP nécessite les paramètres suivants:

- **DOLIBARR_URL**: URL de base de votre instance Dolibarr
- **DOLIBARR_API_KEY**: Clé API générée depuis Dolibarr

## Utilisation

### Avec Claude Code

Le projet inclut un fichier `.mcp.json` pour une utilisation directe dans Claude Code.

La configuration utilise le transport SSE :

```json
{
  "mcpServers": {
    "dolibarr": {
      "type": "sse",
      "url": "http://<MCP_SERVER_HOST>:<MCP_SERVER_PORT>/sse"
    }
  }
}
```

Remplacez `<MCP_SERVER_HOST>` et `<MCP_SERVER_PORT>` par les valeurs correspondant à votre déploiement, puis ouvrez le projet dans Claude Code — les outils MCP seront automatiquement disponibles.

Consultez [CLAUDE_CODE.md](./CLAUDE_CODE.md) pour plus de détails.

### Avec Claude Desktop

Le projet inclut une configuration complète pour Claude Desktop :

```bash
# Utiliser le script d'installation
cd mcp-config
./install.sh
```

Consultez [mcp-config/README.md](./mcp-config/README.md) pour plus de détails.

## Structure du projet

```
dolibarr-mcp-server/
├── .mcp.json                      # Configuration MCP pour Claude Code
├── .env.example                   # Exemple de variables d'environnement
├── README.md                      # Ce fichier
├── CLAUDE_CODE.md                 # Guide d'utilisation avec Claude Code
├── Dolibarr_api_documentation/    # Documentation des API Dolibarr
│   ├── README.md
│   ├── projects.md                # API Projects
│   ├── tasks.md                   # API Tasks
│   ├── thirdparties.md           # API Tiers
│   ├── contacts.md               # API Contacts
│   ├── invoices.md               # API Factures
│   └── products.md               # API Produits
├── mcp-server/                    # Serveur MCP Projects
│   ├── Dockerfile
│   ├── dolibarr_projects_server.py
│   ├── requirements.txt
│   ├── README.md
│   └── CLAUDE.md
├── mcp-server-tasks/              # Serveur MCP Tasks
│   ├── Dockerfile
│   ├── dolibarr_tasks_server.py
│   ├── requirements.txt
│   ├── README.md
│   └── CLAUDE.md
├── mcp-config/                    # Configuration pour Claude Desktop
│   ├── custom.yaml               # Catalogue MCP
│   ├── registry.yaml             # Registre MCP
│   ├── install.sh                # Script d'installation
│   └── README.md
└── prompt/                        # Prompts et instructions
    ├── prompt-api-documentation.md
    └── mcp-builder-prompt-mcp-dolibarr-task.md
```

## Roadmap

- [x] Implémentation du serveur MCP de base
- [x] Support de l'API Projects (6 outils)
- [x] Support de l'API Tasks (4 outils)
- [x] Documentation complète des API Dolibarr
  - [x] Projects API
  - [x] Tasks API
  - [x] Thirdparties API
  - [x] Contacts API
  - [x] Invoices API
  - [x] Products/Services API
- [x] Documentation complète d'utilisation
  - [x] Guide Claude Code
  - [x] Guide Claude Desktop
  - [x] Scripts d'installation
- [x] Configuration partageable pour contributeurs
- [ ] Support de l'API Thirdparties (serveur MCP)
- [ ] Support de l'API Contacts (serveur MCP)
- [ ] Support de l'API Invoices (serveur MCP)
- [ ] Support de l'API Products/Services (serveur MCP)
- [ ] Tests d'intégration automatisés
- [ ] CI/CD avec GitHub Actions

## Contribuer

Les contributions sont les bienvenues! N'hésitez pas à ouvrir des issues ou des pull requests.

## Remerciements

Ce serveur MCP a été construit en utilisant le guide et le template de [theNetworkChuck's Docker MCP Tutorial](https://github.com/theNetworkChuck/docker-mcp-tutorial/blob/main/README.md).

Un grand merci à **NetworkChuck** pour avoir créé un excellent tutoriel et un template qui ont rendu possible la construction de ce serveur MCP !

## Licence

MIT License - Voir le fichier LICENSE pour plus de détails.

Ce projet est open source et permet une utilisation commerciale et propriétaire.

## Références

- [Dolibarr](https://www.dolibarr.org/)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [Model Context Protocol - SSE Transport](https://modelcontextprotocol.io/docs/concepts/transports)
