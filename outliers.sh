#/bin/bash

SERVER_URL="http://127.0.0.1:5000"
name=$0
cluster=
threshold=
curl_opts=

usage()
{
  echo "usage: ${name} [-h] [-c <cluster>] [-t <threshold %>]"
}

while [[ $# > 0 ]]
do
  opt="$1"
  case $opt in
    -c)
      cluster="$2"
      shift
    ;;
    -t)
      threshold="$2"
      shift
    ;;
    -h)
      usage
      exit 0
    ;;
    *)
      curl_opts="${opt} ${curl_opts}"
    ;;
  esac
  shift
done

url="${SERVER_URL}/v1/clusters"

if [[ -n ${cluster} ]]
then
  url="${url}/${cluster}"
fi

url="${url}/caches/outliers"

if [[ -n ${threshold} ]]
then
  url="${url}?threshold=${threshold}"
fi

curl ${curl_opts} ${url}
echo

