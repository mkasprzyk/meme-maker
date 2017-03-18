#!/usr/bin/env bash

set -e

script_dir="$(cd "$(dirname "$0")"; pwd)"

envsubst < "${script_dir}/pypirc.tmpl" > ~/.pypirc

git clean -fd
git checkout "${TRAVIS_BRANCH}"
git reset --hard "${TRAVIS_COMMIT}"
git fetch --tags

bumpversion --no-input --feature
release --no-input

git push --tags
