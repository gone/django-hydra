#!/bin/bash

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

if ! [ -d .git ] || ! [ -d ../django-hydra ]; then
    log_error "Must be run from project root with template at ../django-hydra"
    exit 1
fi

if [ $# -eq 1 ]; then
    if ! [ "$(git cat-file -t "$1" 2>/dev/null)" = "commit" ]; then
        log_error "'$1' is not a valid git commit"
        exit 1
    fi
    PATCH_COMMIT=$1
    BASE_COMMIT=$(git rev-parse "$PATCH_COMMIT^1")
elif [ $# -eq 2 ]; then
    PATCH_COMMIT=$1
    BASE_COMMIT=$2
else
    PATCH_COMMIT=$(git rev-parse HEAD)
    BASE_COMMIT=$(git rev-parse "$PATCH_COMMIT^1")
fi

PROJECT_NAME="${PWD##*/}"
WORK_DIR=$(mktemp -d)
trap 'rm -rf "$WORK_DIR"' EXIT

# Get original branch name
ORIGINAL_BRANCH=$(cd ../django-hydra && git branch --show-current)

# Extract commit message and patch
COMMIT_MSG=$(git log -1 --format=%B "$PATCH_COMMIT")
git format-patch --binary --minimal --stdout "$BASE_COMMIT..$PATCH_COMMIT" > "$WORK_DIR/changes.patch"
sed -i.bak "s/$PROJECT_NAME/[[project_name]]/g" "$WORK_DIR/changes.patch"

pushd "../django-hydra" >/dev/null
TEMP_BRANCH="temp_patch_$(date +%s)"
git checkout -b "$TEMP_BRANCH"

if ! git apply -v --reject --directory="[[project_name]]" "$WORK_DIR/changes.patch" ; then
    log_warning "Merge conflicts detected. Resolve the conflicts then:"
    log_warning "1. git add changed files"
    log_warning "2. git commit -m '$COMMIT_MSG'"
    exit 1
else
    git add .
    git commit -m "$COMMIT_MSG"
fi

git checkout "$ORIGINAL_BRANCH"
if ! git merge "$TEMP_BRANCH" -m "Applied patch from instance project: $COMMIT_MSG"; then
    log_warning "Conflict during merge to $ORIGINAL_BRANCH. Resolve conflicts and merge manually."
    exit 1
fi
git branch -d "$TEMP_BRANCH"
log_info "Successfully applied changes to template"
popd >/dev/null
