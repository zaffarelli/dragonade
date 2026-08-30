#!/usr/bin/env bash

git add --all && git commit -m "v$1" && git push && uv version $2