# freight-tenders frontend

The Angular frontend of the freight tender demo app. What the app does, the
backend it talks to, and how to run both together are described in
[`../README.md`](../README.md).

```bash
npm ci && npm run build      # production build
npm test -- --watch=false    # Vitest unit tests; the bare `ng test`/`npm test` default watches and never exits
npm run lint                 # `ng lint`
npm start                    # dev server on :4200, proxying /api to localhost:8080 (the backend must already be running)
```
