#!/bin/sh

set -o errexit
set -o pipefail
set -o nounset


celery -A iffapp.taskapp beat -l INFO
