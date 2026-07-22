#!/usr/bin/env bash
 
set -euo pipefail
 
SOURCE_FILE="grades.csv"
ARCHIVE_DIR="archive"
LOG_FILE="organizer.log"
 
#1) This part checks if the isn something to archive.
if [ ! -f "$SOURCE_FILE" ]; then
    echo "Error: $SOURCE_FILE not found in $(pwd)." >&2
    exit 1
fi
 
#2) This creates the archive directory .
if [ ! -d "$ARCHIVE_DIR" ]; then
    mkdir -p "$ARCHIVE_DIR"
    echo "Created directory: $ARCHIVE_DIR"
fi
 
# 3) This creates the timestap
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
ARCHIVED_NAME="grades_${TIMESTAMP}.csv"
 
# 4) This move + rename the original file into the archive.
mv "$SOURCE_FILE" "${ARCHIVE_DIR}/${ARCHIVED_NAME}"
echo "Archived $SOURCE_FILE -> ${ARCHIVE_DIR}/${ARCHIVED_NAME}"
 
# 5)This reset the workspace with a fresh, empty grades.csv.
touch "$SOURCE_FILE"
echo "Created a new empty $SOURCE_FILE"
 
# 6) This append this run to the log (accumulates across runs).
echo "[$(date '+%Y-%m-%d %H:%M:%S')] timestamp=${TIMESTAMP} original=${SOURCE_FILE} archived=${ARCHIVE_DIR}/${ARCHIVED_NAME}" >> "$LOG_FILE"
echo "Logged operation to $LOG_FILE"
 
exit 0
