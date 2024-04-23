# Micromongo

Micromongo is a HTTP microservice to interact with a mongo database.

```
Usage:
  GET    /<collection>?number=<n>&skip=<s>&filter=<f> => get n entries in collection that match f (skip s)
  GET    /<collection>/<id>                           => get entry in collection with id
  POST   /<collection> [json]                         => add an entry to collection using json
  PATCH  /<collection>?filter=<f> [json]              => update the entries in collection that match f using json
  PATCH  /<collection>/<id> [json]                    => update the entry in collection with id using json
  PUT    /<collection>/<id> [json]                    => replace the entry in collection with id using json
  DELETE /<collection>?filter=<f>                     => delete all entries in collection that match f
  DELETE /<collection>/<id>                           => delete the entry in collection with id
```

Environment variables:
 - `HOST`: The host of the mongo database
 - `USER`: The username to authenticate to the database with
 - `PASS`: The password to authenticate to the database with
 - `DATABASE`: The database to use for queries with mongo

There is a basic kubernetes deployment and service in `micromongo.yaml`, and it can be run in docker using the image `rhysperry111/micromongo`. The default port exposed it `8000`
