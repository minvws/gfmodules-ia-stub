#!/usr/bin/env bash

set -e

# Usage: ./setup-config.sh [source_folder] [destination_folder]
SOURCE_FOLDER="${1:-.}"
DEST_FOLDER="${2:-.}"

copy_example_config () {
  local config_file="$1"
  local config_file_source_folder="${2:-.}"
  local config_file_destination_folder="${3:-.}"
  local src_path="$SOURCE_FOLDER/$config_file_source_folder/$config_file.example"
  local dest_path="$DEST_FOLDER/$config_file_destination_folder/$config_file"
  if [[ ! -f "$dest_path" ]]; then
    echo "copying $src_path to $dest_path"
    cp "$src_path" "$dest_path"
  fi
}

copy_example_config "app.conf" dist/configs
copy_example_config "clients.json" dist/configs
copy_example_config "settings.json" saml/tvs saml/tvs
copy_example_config "login_methods.json" dist/configs
copy_example_config "version.json" "static" "static"
copy_example_config "uzi_data.json" dist/configs
copy_example_config "digid_mock_identities.json" dist/configs
