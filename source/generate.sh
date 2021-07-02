#!/bin/bash

set -xeu -o pipefail

site_dir="source"
yml_dir="../docs"
pages_dir="pages"

cd "$site_dir"
mkdir -p "$pages_dir"
cp ../docs/*.md .
./yaml_to_md.py "$yml_dir/functions.yml" "$yml_dir/hooks.yml" "$pages_dir"

bundle install
bundle exec jekyll build
