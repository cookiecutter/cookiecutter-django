#!/bin/bash

CURRENT_VERSION="$1"
COMMIT_MESSAGE="$2"

echo "Using current version: ${CURRENT_VERSION}"
echo "Using commit message: ${COMMIT_MESSAGE}"

SEMVER_TYPES=([MINOR] [MAJOR] [PATCH])
COUNTER=0
BUMP_RULE=""
for semver in "${SEMVER_TYPES[@]}"; do
    if [[ "${COMMIT_MESSAGE}" == *"${semver}"* ]]; then
        if [ ${COUNTER} -gt 0 ] ; then
            echo "[ERROR] Multiple semvers Found. You can only use one of the following semvers: ${SEMVER_TYPES[*]}"
            exit 1
        fi
        BUMP_RULE=$(echo "${semver}" | tr '[:upper:]' '[:lower:]' | tr -d '[],')
        COUNTER=$((COUNTER+1))
    fi
done

if [ ${COUNTER} -eq 0 ]; then
    echo "[WARNING] No semver found in your commit message. Defaulting to PATCH"
    echo "No semver found in your commit message. Defaulting to PATCH" >> "$GITHUB_STEP_SUMMARY"
    BUMP_RULE="patch"
fi


pip install semver
echo "Using bump rule: ${BUMP_RULE}"
BUMPED_VERSION=$(python -m semver bump "${BUMP_RULE}" "${CURRENT_VERSION}")
echo "Bump version number: ${BUMPED_VERSION}"

# Return the bumped version
echo "version=$BUMPED_VERSION" >> "$GITHUB_OUTPUT"
