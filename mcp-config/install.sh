#!/bin/bash

# Script d'installation de la configuration MCP Dolibarr
# Usage: ./install.sh

set -e

echo "================================================"
echo "Installation de la configuration MCP Dolibarr"
echo "================================================"
echo ""

# Couleurs pour l'affichage
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Détection du système d'exploitation
OS="$(uname -s)"
case "${OS}" in
    Linux*)     MACHINE=Linux;;
    Darwin*)    MACHINE=Mac;;
    CYGWIN*)    MACHINE=Windows;;
    MINGW*)     MACHINE=Windows;;
    *)          MACHINE="UNKNOWN:${OS}"
esac

echo -e "${GREEN}Système détecté: ${MACHINE}${NC}"
echo ""

# Définir le chemin home selon l'OS
if [ "$MACHINE" = "Windows" ]; then
    MCP_DIR="$APPDATA/.docker/mcp"
    CLAUDE_CONFIG="$APPDATA/Claude/claude_desktop_config.json"
else
    MCP_DIR="$HOME/.docker/mcp"
    if [ "$MACHINE" = "Mac" ]; then
        CLAUDE_CONFIG="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
    else
        CLAUDE_CONFIG="$HOME/.config/Claude/claude_desktop_config.json"
    fi
fi

# Créer les dossiers nécessaires
echo -e "${YELLOW}Étape 1/5:${NC} Création des dossiers MCP..."
mkdir -p "$MCP_DIR/catalogs"
echo -e "${GREEN}✓${NC} Dossiers créés"
echo ""

# Sauvegarder les fichiers existants
echo -e "${YELLOW}Étape 2/5:${NC} Sauvegarde des fichiers existants..."
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

if [ -f "$MCP_DIR/catalogs/custom.yaml" ]; then
    cp "$MCP_DIR/catalogs/custom.yaml" "$MCP_DIR/catalogs/custom.yaml.backup-$TIMESTAMP"
    echo -e "${GREEN}✓${NC} Sauvegarde de custom.yaml créée"
else
    echo -e "${YELLOW}⚠${NC}  Aucun custom.yaml existant"
fi

if [ -f "$MCP_DIR/registry.yaml" ]; then
    cp "$MCP_DIR/registry.yaml" "$MCP_DIR/registry.yaml.backup-$TIMESTAMP"
    echo -e "${GREEN}✓${NC} Sauvegarde de registry.yaml créée"
else
    echo -e "${YELLOW}⚠${NC}  Aucun registry.yaml existant"
fi
echo ""

# Copier les nouveaux fichiers
echo -e "${YELLOW}Étape 3/5:${NC} Installation des fichiers de configuration..."
cp custom.yaml "$MCP_DIR/catalogs/custom.yaml"
echo -e "${GREEN}✓${NC} custom.yaml installé"

cp registry.yaml "$MCP_DIR/registry.yaml"
echo -e "${GREEN}✓${NC} registry.yaml installé"
echo ""

# Vérifier la configuration Claude Desktop
echo -e "${YELLOW}Étape 4/5:${NC} Vérification de la configuration Claude Desktop..."
if [ -f "$CLAUDE_CONFIG" ]; then
    if grep -q "custom.yaml" "$CLAUDE_CONFIG"; then
        echo -e "${GREEN}✓${NC} Configuration Claude Desktop OK"
    else
        echo -e "${RED}⚠${NC}  ATTENTION: custom.yaml n'est pas référencé dans la configuration Claude Desktop"
        echo ""
        echo "Veuillez ajouter cette ligne dans la section 'args' de $CLAUDE_CONFIG :"
        echo '  "--catalog=/mcp/catalogs/custom.yaml",'
        echo ""
    fi
else
    echo -e "${YELLOW}⚠${NC}  Fichier de configuration Claude Desktop non trouvé"
    echo "   Emplacement attendu: $CLAUDE_CONFIG"
    echo ""
fi

# Vérifier Docker et les images
echo -e "${YELLOW}Étape 5/5:${NC} Vérification de Docker..."
if command -v docker &> /dev/null; then
    echo -e "${GREEN}✓${NC} Docker est installé"

    # Vérifier les images
    if docker images | grep -q "dolibarr-projects-mcp-server"; then
        echo -e "${GREEN}✓${NC} Image dolibarr-projects-mcp-server trouvée"
    else
        echo -e "${YELLOW}⚠${NC}  Image dolibarr-projects-mcp-server non trouvée"
        echo "   Construisez-la avec: cd ../mcp-server && docker build -t dolibarr-projects-mcp-server:latest ."
    fi

    if docker images | grep -q "dolibarr-tasks-mcp-server"; then
        echo -e "${GREEN}✓${NC} Image dolibarr-tasks-mcp-server trouvée"
    else
        echo -e "${YELLOW}⚠${NC}  Image dolibarr-tasks-mcp-server non trouvée"
        echo "   Construisez-la avec: cd ../mcp-server-tasks && docker build -t dolibarr-tasks-mcp-server:latest ."
    fi
else
    echo -e "${RED}✗${NC} Docker n'est pas installé ou n'est pas dans le PATH"
    exit 1
fi
echo ""

# Instructions pour les secrets
echo "================================================"
echo -e "${GREEN}Installation terminée avec succès!${NC}"
echo "================================================"
echo ""
echo -e "${YELLOW}Prochaines étapes:${NC}"
echo ""
echo "1. Configurez les secrets Docker MCP:"
echo "   docker mcp secret set DOLIBARR_URL=\"https://votre-dolibarr.com\""
echo "   docker mcp secret set DOLIBARR_API_KEY=\"votre_cle_api\""
echo ""
echo "2. Construisez les images Docker si ce n'est pas déjà fait:"
echo "   cd ../mcp-server && docker build -t dolibarr-projects-mcp-server:latest ."
echo "   cd ../mcp-server-tasks && docker build -t dolibarr-tasks-mcp-server:latest ."
echo ""
echo "3. Vérifiez les serveurs MCP:"
echo "   docker mcp server list"
echo ""
echo "4. Redémarrez Claude Desktop pour activer les nouveaux outils"
echo ""
echo -e "${GREEN}Les outils Dolibarr seront alors disponibles dans Claude Desktop!${NC}"
echo ""
