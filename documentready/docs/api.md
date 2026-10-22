# API Documentation

All API responses are JSON and wrapped in an envelope containing `data` and `meta`.
Errors return a standard error object with a specific error code.

## Search
`GET /api/search?q={query}`
Returns array of matched services and documents sorted by relevance score.

## Services
`GET /api/services`
Lists all known services.

`GET /api/services/{id}?category={cat}`
Returns the full definition of a service, including resolved requirements for the optional category.

`POST /api/services/{id}/readiness`
Evaluates readiness.
**Body:**
```json
{
  "statuses": {
    "doc_id_1": "available",
    "doc_id_2": "missing"
  },
  "applicant_category": "student"
}
```

## Documents
`GET /api/documents/{id}`
Returns details of a document, including services that require it.

`GET /api/documents/{id}/guide`
Returns the guide for the document, including a dependency tree and prerequisite metadata.
