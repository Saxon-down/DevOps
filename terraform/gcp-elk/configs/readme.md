Config files, where they should be stored, and how they've been modified (most haven't yet, but should be as the environment is built).


ELASTICSEARCH.YML
    Stored in elasticsearch/config/
    Modified slightly to use a proper cluster name, rather than the default
LOGSTASH.CONF
    Stored in logstash/conf/ (make sure it's the only file in there!!)
LOGSTASH.YML
    Stored in logstash/config/
KIBANA.YML
    Stored in kibana/config/
    elasticsearch.url will need to be changed once we know the IP for the
        elastic server (defaults to 127.0.0.1:9200)
METRICBEAT.YML
    Stored in metricbeat/

