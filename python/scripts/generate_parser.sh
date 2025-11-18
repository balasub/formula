#!/bin/bash
# Script to generate Python parser from ANTLR4 grammar files

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Generating FORMULA Parser for Python${NC}"

# Paths
GRAMMAR_DIR="../Src/Core/API/Parser"
OUTPUT_DIR="formula/parser"
ANTLR_JAR="antlr-4.13.1-complete.jar"
ANTLR_URL="https://www.antlr.org/download/${ANTLR_JAR}"

# Check if ANTLR jar exists, download if not
if [ ! -f "${ANTLR_JAR}" ]; then
    echo -e "${BLUE}Downloading ANTLR4...${NC}"
    curl -O "${ANTLR_URL}"
fi

# Clean previous generated files
echo -e "${BLUE}Cleaning previous generated files...${NC}"
rm -rf "${OUTPUT_DIR}"/Formula*.py
rm -f "${OUTPUT_DIR}"/*.interp
rm -f "${OUTPUT_DIR}"/*.tokens

# Generate lexer
echo -e "${BLUE}Generating lexer...${NC}"
java -jar "${ANTLR_JAR}" \
    -Dlanguage=Python3 \
    -o "${OUTPUT_DIR}" \
    -visitor \
    -no-listener \
    "${GRAMMAR_DIR}/FormulaLexer.g4"

# Generate parser
echo -e "${BLUE}Generating parser...${NC}"
java -jar "${ANTLR_JAR}" \
    -Dlanguage=Python3 \
    -o "${OUTPUT_DIR}" \
    -visitor \
    -no-listener \
    "${GRAMMAR_DIR}/FormulaParser.g4"

echo -e "${GREEN}Parser generation complete!${NC}"
echo -e "${GREEN}Generated files in: ${OUTPUT_DIR}${NC}"
