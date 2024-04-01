#!/command/with-contenv bash
# shellcheck shell=bash disable=SC1091

# Copyright 2023 Ramon F Kolb https://github.com/kx1t
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

source /scripts/common

RETRIES=5

# We need to do this a few times to make sure the interface is up
for ((n=0; n<RETRIES; n++)); do
  c="$(curl -sSL localhost:9274/metrics 2>&1|tail -1)"
  if [[ "$(awk '{print $1}' <<< "$c")" == "geiger_usvh" ]]; then break; fi
  sleep 1
done

if [[ "$(awk '{print $1}' <<< "$c")" == "geiger_usvh" ]] && (( $(bc -l <<< "$(awk '{print $2}' <<< "$c") > 0") == 1 )); then
  echo "HEALTHY: at $(date), latest measurement $(awk '{print $2}' <<< "$c") uSv/hr "
  exit 0
else
  echo "UNHEALTHY: at $(date), ping returned $c"
  exit 1
fi

