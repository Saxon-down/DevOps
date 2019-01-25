docker build -f dockerfile -t pre-receive.python3.alpine-3.3 .
docker create --name pre-receive.python3.alpine-3.3 pre-receive.python3.alpine-3.3 /bin/true
docker export pre-receive.python3.alpine-3.3 | gzip > alpine-3.3.tar.gz