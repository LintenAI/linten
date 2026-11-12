Additional files for the proxy. Reduces the size of the main linten package.

Currently, only stores the migration.sql files for linten-proxy.

To install, run:

```bash
uv add linten-proxy-extras
```
OR 

```bash
uv tool install 'linten[proxy]' # installs linten-proxy-extras and other proxy dependencies
```

To use the migrations, run:

```bash
linten --use_prisma_migrate
```
