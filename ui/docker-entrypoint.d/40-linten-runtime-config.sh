#!/bin/sh
set -eu

runtime_dir=/tmp/linten-ui
runtime_file=$runtime_dir/runtime-config.json
rm -f "$runtime_file" 2>/dev/null || true

if [ "${LINTEN_BACKEND_URL+x}" = "" ]; then
  exit 0
fi

newline='
'
case "$LINTEN_BACKEND_URL" in
  *"$newline"*)
    printf '%s\n' 'WARN: ignoring invalid LINTEN_BACKEND_URL' >&2
    exit 0
    ;;
esac

if ! printf '%s\n' "$LINTEN_BACKEND_URL" | grep -Eq '^https?://[^"\\ ]+$'; then
  printf '%s\n' 'WARN: ignoring invalid LINTEN_BACKEND_URL' >&2
  exit 0
fi

backend_url=$LINTEN_BACKEND_URL
while [ "${backend_url%/}" != "$backend_url" ]; do
  backend_url=${backend_url%/}
done

mkdir -p "$runtime_dir"
printf '{"backend_url":"%s"}\n' "$backend_url" > "$runtime_file"
