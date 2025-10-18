# Dolibarr MCP Server

## Objectif

Ce projet vise à créer un serveur MCP (Model Context Protocol) pour Dolibarr, permettant une intégration transparente avec des outils d'IA et d'automatisation. Le serveur MCP expose les fonctionnalités de Dolibarr via ses API REST et les rend accessibles via le protocole MCP.

## Architecture

Ce serveur MCP s'appuie sur le module **docker-mcp-gateway** pour fournir une interface standardisée entre les clients MCP et l'API REST de Dolibarr.

### Composants

- **Dolibarr API**: API REST native de Dolibarr exposant les fonctionnalités de gestion (projets, tâches, tiers, etc.)
- **docker-mcp-gateway**: Module gateway permettant d'exposer les API via le protocole MCP
- **MCP Server**: Serveur implémentant le protocole MCP pour Dolibarr

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
- Module docker-mcp-gateway

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

Une fois le serveur MCP démarré, il expose les ressources et outils Dolibarr via le protocole MCP, permettant aux clients MCP (comme Claude Desktop, IDE avec support MCP, etc.) d'interagir avec Dolibarr.

## Structure du projet

```
dolibarr-mcp-server/
├── README.md                      # Ce fichier
├── Dolibarr_api_documentation/    # Documentation des API Dolibarr
│   ├── README.md                  # Vue d'ensemble de l'API
│   └── projects.md                # Documentation API Projects
├── prompt/                        # Prompts et instructions
│   └── prompt-api-documentation.md
└── src/                          # Code source (à venir)
```

## Roadmap

- [ ] Implémentation du serveur MCP de base
- [ ] Support de l'API Projects
- [ ] Support de l'API Tasks
- [ ] Support de l'API Thirdparties
- [ ] Support de l'API Contacts
- [ ] Support de l'API Invoices
- [ ] Support de l'API Products/Services
- [ ] Documentation complète d'utilisation
- [ ] Tests d'intégration

## Contribuer

Les contributions sont les bienvenues! N'hésitez pas à ouvrir des issues ou des pull requests.

## Remerciements

Ce serveur MCP a été construit en utilisant le guide et le template de [theNetworkChuck's Docker MCP Tutorial](https://github.com/theNetworkChuck/docker-mcp-tutorial/blob/main/README.md).

Un grand merci à **NetworkChuck** pour avoir créé un excellent tutoriel et un template qui ont rendu possible la construction de ce serveur MCP !

## Licence

[À définir]

## Références

- [Dolibarr](https://www.dolibarr.org/)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [docker-mcp-gateway](https://github.com/docker/mcp-gateway)
