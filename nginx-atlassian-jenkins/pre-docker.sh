rm -rf data-dira data-confluence
rm -rf server-jenkins server-jira server-confluence

mkdir data-jira data-confluence
mkdir server-jenkins server-jira server-confluence

curl http://updates.jenkins-ci.org > /dev/null

ECHO
ECHO Now you need to add the following to /etc/hosts:
ECHO 127.0.0.1       mytestdomain.com
ECHO 127.0.0.1       jira.mytestdomain.com
ECHO 127.0.0.1       confluence.mytestdomain.com
ECHO 127.0.0.1       jenkins.mytestdomain.com
