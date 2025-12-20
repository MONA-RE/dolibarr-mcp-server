#!/bin/bash

##############################################################################
# Script de reconstruction et redémarrage des serveurs MCP Dolibarr
#
# Ce script permet de :
# - Reconstruire les images Docker des serveurs MCP (projects et tasks)
# - Redémarrer le MCP Gateway pour utilisation via n8n
#
# Usage: ./rebuild_and_restart.sh [options]
#
# Options:
#   --full       Arrêt complet, rebuild, et redémarrage
#   --quick      Rebuild rapide et restart seulement (défaut)
#   --help       Affiche cette aide
##############################################################################

set -e  # Arrêt en cas d'erreur

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Dossier de base
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo -e "${BLUE}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  MCP Dolibarr - Rebuild & Restart                       ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Fonction d'aide
show_help() {
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  --full       Arrêt complet, rebuild, et redémarrage"
    echo "  --quick      Rebuild rapide et restart seulement (défaut)"
    echo "  --help       Affiche cette aide"
    echo ""
    exit 0
}

# Mode par défaut
MODE="quick"

# Lecture des arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --full)
            MODE="full"
            shift
            ;;
        --quick)
            MODE="quick"
            shift
            ;;
        --help)
            show_help
            ;;
        *)
            echo -e "${RED}✗ Option inconnue: $1${NC}"
            echo "Utilisez --help pour voir les options disponibles"
            exit 1
            ;;
    esac
done

# Vérification que Docker est accessible
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}✗ Erreur: Docker n'est pas accessible${NC}"
    echo "Vérifiez que Docker est démarré et que vous avez les permissions nécessaires"
    exit 1
fi

# Vérification du fichier .env
if [ ! -f .env ]; then
    echo -e "${RED}✗ Erreur: Fichier .env manquant${NC}"
    echo "Créez un fichier .env avec:"
    echo "  DOLIBARR_URL=http://votre-dolibarr"
    echo "  DOLIBARR_API_KEY=votre_cle_api"
    exit 1
fi

# Lecture des variables d'environnement
source .env

# Vérification de la configuration
if [ -z "$DOLIBARR_URL" ]; then
    echo -e "${RED}✗ Erreur: DOLIBARR_URL non défini dans .env${NC}"
    exit 1
fi

if [ -z "$DOLIBARR_API_KEY" ]; then
    echo -e "${RED}✗ Erreur: DOLIBARR_API_KEY non défini dans .env${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Configuration valide${NC}"
echo -e "  DOLIBARR_URL: ${DOLIBARR_URL}"
echo -e "  API Key: ${DOLIBARR_API_KEY:0:10}..."
echo ""

if [ "$MODE" == "full" ]; then
    echo -e "${YELLOW}═══ Mode FULL: Arrêt complet + Rebuild + Redémarrage ═══${NC}"
    echo ""

    # Étape 1: Arrêt complet
    echo -e "${BLUE}[1/4]${NC} Arrêt du gateway..."
    docker compose down
    echo -e "${GREEN}✓ Gateway arrêté${NC}"
    echo ""

    # Étape 2: Construction des images
    echo -e "${BLUE}[2/4]${NC} Construction des images MCP..."
    echo "      - dolibarr-projects-mcp-server:latest"
    echo "      - dolibarr-tasks-mcp-server:latest"
    docker compose --profile build-only build
    echo -e "${GREEN}✓ Images construites${NC}"
    echo ""

    # Étape 3: Démarrage du gateway
    echo -e "${BLUE}[3/4]${NC} Démarrage du gateway..."
    docker compose up gateway -d
    echo -e "${GREEN}✓ Gateway démarré${NC}"
    echo ""

    # Étape 4: Attente et vérification
    echo -e "${BLUE}[4/4]${NC} Vérification du démarrage..."
    sleep 3

else
    echo -e "${YELLOW}═══ Mode QUICK: Rebuild + Restart ═══${NC}"
    echo ""

    # Étape 1: Construction des images
    echo -e "${BLUE}[1/3]${NC} Construction des images MCP..."
    echo "      - dolibarr-projects-mcp-server:latest"
    echo "      - dolibarr-tasks-mcp-server:latest"
    docker compose --profile build-only build
    echo -e "${GREEN}✓ Images construites${NC}"
    echo ""

    # Étape 2: Redémarrage du gateway
    echo -e "${BLUE}[2/3]${NC} Redémarrage du gateway..."
    docker compose restart gateway
    echo -e "${GREEN}✓ Gateway redémarré${NC}"
    echo ""

    # Étape 3: Attente et vérification
    echo -e "${BLUE}[3/3]${NC} Vérification du démarrage..."
    sleep 3
fi

# Vérification finale
echo -e "${BLUE}═══ Vérification finale ═══${NC}"
echo ""

# 1. Vérifier que le container est running
if docker ps | grep -q mcp_dolibarr; then
    echo -e "${GREEN}✓ Container mcp_dolibarr est en cours d'exécution${NC}"
    CONTAINER_ID=$(docker ps | grep mcp_dolibarr | awk '{print $1}')
    echo -e "  Container ID: ${CONTAINER_ID}"
else
    echo -e "${RED}✗ Container mcp_dolibarr n'est pas en cours d'exécution${NC}"
    echo ""
    echo "Logs du container:"
    docker logs mcp_dolibarr --tail 20
    exit 1
fi

# 2. Vérifier les images
echo ""
echo -e "${BLUE}Images MCP disponibles:${NC}"
docker images | grep -E "dolibarr-(projects|tasks)-mcp-server" | while read line; do
    echo -e "  ${GREEN}✓${NC} $line"
done

# 3. Vérifier le port
echo ""
if docker ps | grep mcp_dolibarr | grep -q "8811"; then
    echo -e "${GREEN}✓ Port 8811 exposé correctement${NC}"
else
    echo -e "${YELLOW}⚠ Port 8811 pourrait ne pas être exposé${NC}"
fi

# 4. Afficher les derniers logs
echo ""
echo -e "${BLUE}═══ Derniers logs du gateway (5 dernières lignes) ═══${NC}"
docker logs mcp_dolibarr --tail 5
echo ""

# 5. Informations de connexion
echo -e "${BLUE}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  Configuration n8n                                      ║${NC}"
echo -e "${BLUE}╠══════════════════════════════════════════════════════════╣${NC}"
echo -e "${BLUE}║${NC}  URL du MCP Gateway:                                   ${BLUE}║${NC}"
echo -e "${BLUE}║${NC}    ${GREEN}http://localhost:8811/sse${NC}                          ${BLUE}║${NC}"
echo -e "${BLUE}║${NC}                                                          ${BLUE}║${NC}"
echo -e "${BLUE}║${NC}  Outils MCP disponibles:                               ${BLUE}║${NC}"
echo -e "${BLUE}║${NC}    • dolibarr_projects (8 outils)                      ${BLUE}║${NC}"
echo -e "${BLUE}║${NC}    • dolibarr_tasks (4 outils)                         ${BLUE}║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""

# 6. Commandes utiles
echo -e "${BLUE}Commandes utiles:${NC}"
echo -e "  Voir les logs en temps réel:  ${YELLOW}docker logs mcp_dolibarr -f${NC}"
echo -e "  Arrêter le gateway:            ${YELLOW}docker compose down${NC}"
echo -e "  Rebuild complet:               ${YELLOW}$0 --full${NC}"
echo ""

echo -e "${GREEN}✓ Rebuild et redémarrage terminés avec succès!${NC}"
echo ""
