# Setup: Node.js toolchain (for `/prototype`)

**Referenced by:** `RF-10 node_toolchain_missing` in `framework/shared/refusal-registry.md`.

**Why:** `/prototype` scaffolds and builds a real Next.js app under `prototypes/`. That requires a local Node.js + npm toolchain. The prototype app targets **Next.js 16 / React 19**, which need **Node.js ≥ 20** (LTS recommended).

## Install

**Windows (recommended — winget):**
```powershell
winget install OpenJS.NodeJS.LTS
```

**Or download the LTS installer:** https://nodejs.org/en/download (choose the Windows LTS build).

**Or use a version manager (nvm-windows):** https://github.com/coreybutler/nvm-windows — then:
```powershell
nvm install lts
nvm use lts
```

## Verify

Open a **new** terminal (so PATH refreshes) and run:
```powershell
node --version   # expect v20.x or newer
npm --version
```

If `node --version` reports below v20, install a newer LTS and ensure it is first on PATH.

## Then

Re-invoke `/prototype`. Resumption detects the prior progress and picks up at the scaffold step (Step F1); `npm install` runs once and the shared `prototypes/` app is created.

## Notes

- The one-time `npm install` happens inside `prototypes/` and is amortised across every prototype you generate (it never re-installs on later runs).
- `prototypes/node_modules/` is git-ignored and must never be committed.
