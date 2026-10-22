# Architecture

DocumentReady is built on a simple three-tier architecture:

```mermaid
graph TD;
    Browser[Browser (HTML+CSS+Vanilla JS)] -->|HTTP GET/POST| Routes[Flask Routes];
    Routes --> API[API Blueprint (/api/*)];
    Routes --> Pages[Pages Blueprint (/*)];
    
    API --> Services[Services Layer];
    Pages --> Services;
    
    Services --> Graph[graph.py (DAG, Topological Sort)];
    Services --> Req[requirements.py (Resolution)];
    Services --> Ready[readiness.py (Evaluation Engine)];
    Services --> Search[search.py (Fuzzy Text Search)];
    
    Graph --> Repo[repository.py (In-Memory Store)];
    Req --> Repo;
    Ready --> Repo;
    Search --> Repo;
    
    Repo --> Data[(JSON Files)];
```

- **Data**: Static JSON files loaded once at startup. Validated using `jsonschema`.
- **Repository**: Singleton store holding parsed domain entities in memory and providing fast indexed lookups.
- **Services**: Pure functions containing business logic. No web request parsing or HTTP logic here.
- **Routes**: Flask blueprints mapping HTTP endpoints to service function calls.
- **Frontend**: ES2020 modules with a central store for checklist state.
