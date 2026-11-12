# Homebrew formula for the `lite` CLI

[`lite.rb`](./lite.rb) is the canonical source for the Homebrew formula that installs the thin Linten CLI (`linten[cli]`). It lives here so it is versioned with the code, but Homebrew serves formulae from a tap, so it has to be published to the `LintenAI/homebrew-linten` tap to be installable.

Once published, end users install with

```shell
brew install LintenAI/linten/lite
```

which gives them the `lite` command (`lite login`, `lite claude`, `lite models list`, ...) without the proxy server runtime. For the full proxy server, they keep using pip/uv with `linten[proxy]` or the Docker image.

## Why a tap and not homebrew-core

The formula builds the published `linten` sdist with the `cli` extra and resolves that extra's dependencies from PyPI at build time. homebrew-core forbids network access during `install` and would require every transitive dependency declared as a pinned `resource`, regenerated on each release. For a fast-moving CLI that tradeoff is not worth it, so this stays a tap formula.

## Release runbook

The formula can only point at a published artifact, so it activates with the first `linten` release that ships the `cli` extra (added in [pyproject.toml](../../pyproject.toml)).

1. Cut a `linten` release whose `pyproject.toml` includes the `cli` extra and confirm it is on PyPI.
2. Fetch the sdist URL and checksum for that version: `curl -fsSL https://pypi.org/pypi/linten/<version>/json | jq -r '.urls[] | select(.packagetype=="sdist") | "\(.url)\n\(.digests.sha256)"'`
3. Set `url` and `sha256` in `lite.rb` to those values; `version` is parsed from `url`.
4. Copy `lite.rb` into the tap repo under `Formula/lite.rb`, then run `brew install --build-from-source ./Formula/lite.rb` and `brew test lite` to verify a clean build and that `lite --help` works.
5. Commit and push to `LintenAI/homebrew-linten`.

Keep `lite.rb` here in sync with the tap copy so the in-repo formula stays the source of truth.
