#!/bin/bash

# Chiede il messaggio all'utente
read -p "Messaggio del commit: " MSG

# Se il messaggio è vuoto, annulla tutto
if [ -z "$MSG" ]; then
  echo "⚠️  Nessun messaggio inserito. Commit annullato."
  exit 1
fi

git add .
git commit -m "$MSG"
git push

# Mostra gli ultimi 5 commit
echo "📜 Ultimi 5 commit:"
git log -5 --pretty=format:"%h | %an | %ad | %s" --date=iso
echo ""