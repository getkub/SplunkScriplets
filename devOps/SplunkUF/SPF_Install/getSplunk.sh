#!/bin/bash

set -e

# ----------- Default Configurable Inputs -----------
product=""
version=""
arch="amd64"
os="linux"        # linux | windows
pkg=""            # deb | tgz | rpm | msi
hash=""           # Replace with actual hash from Splunk
# ------------------------------------------

# Function to display usage
usage() {
  echo "Usage: $0 -p product -v version -k package -h hash"
  echo "  -p product   : The product name (e.g., splunk, uf)"
  echo "  -v version   : The version number (e.g., 9.4.2)"
  echo "  -k package   : The package type (deb, tgz, rpm, msi)"
  echo "  -h hash      : The build hash"
  exit 1
}

# Parse command-line options
while getopts "p:v:k:h:" opt; do
  case "$opt" in
    p) product="$OPTARG" ;;
    v) version="$OPTARG" ;;
    k) pkg="$OPTARG" ;;
    h) hash="$OPTARG" ;;
    *) usage ;;
  esac
done

# Check if all required options are provided
if [ -z "$product" ] || [ -z "$version" ] || [ -z "$pkg" ] || [ -z "$hash" ]; then
  usage
fi

# Handle special case for "uf" (Universal Forwarder)
if [ "$product" = "uf" ]; then
  product="splunkforwarder"
fi

log() {
  local level="$1"; shift
  local msg="$1"; shift
  local kv_pairs="$*"
  echo "timestamp=\"$(date -u +'%Y-%m-%dT%H:%M:%SZ')\" level=\"$level\" msg=\"$msg\" $kv_pairs"
}

log info "Starting download process" "product=\"$product\" version=\"$version\" hash=\"$hash\" os=\"$os\" arch=\"$arch\" pkg=\"$pkg\""

# Determine filename
case "$os" in
  "linux")
    if [ "$pkg" = "deb" ]; then
      filename="${product}-${version}-${hash}-${os}-${arch}.${pkg}"
    elif [ "$pkg" = "rpm" ]; then
      arch="x86_64"
      filename="${product}-${version}-${hash}-${arch}.${pkg}"
    else
      filename="${product}-${version}-${hash}-${os}-${arch}.${pkg}"
    fi
    ;;
  "windows")
    arch="x64"
    pkg="msi"
    filename="${product}-${version}-${hash}-windows-${arch}.${pkg}"
    ;;
  *)
    log error "Unsupported OS type" "os=\"$os\""
    exit 1
    ;;
esac

# Construct the URL with 'universalforwarder' instead of $product if it's uf
if [ "$product" = "splunkforwarder" ]; then
  download_base_url="https://download.splunk.com/products/universalforwarder/releases"
else
  download_base_url="https://download.splunk.com/products/${product}/releases"
fi

md5_url="${download_base_url}/${version}/${os}/${filename}.md5"
file_url="${download_base_url}/${version}/${os}/${filename}"

log info "Constructed download URLs" "filename=\"$filename\" md5_url=\"$md5_url\" file_url=\"$file_url\""

# Download MD5 file
if wget -c "$md5_url"; then
  log info "MD5 file downloaded successfully" "filename=\"${filename}.md5\""
else
  log error "Failed to download MD5 file" "url=\"$md5_url\""
  exit 1
fi

# Download package file
if wget -c "$file_url"; then
  log info "Package downloaded successfully" "filename=\"$filename\""
else
  log error "Failed to download package file" "url=\"$file_url\""
  exit 1
fi
