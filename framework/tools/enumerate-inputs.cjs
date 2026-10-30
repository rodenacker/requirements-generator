'use strict';
// enumerate-inputs.cjs — the one deterministic walk of documentation_dir.
//
// Mechanical rendering of framework/shared/input-exclusions.md > Enumeration depth + IX-01..IX-04,
// so the input-handler (Steps S/V) and check-manifest-freshness (Step 2) list identical paths.
// Read-only: stats and hashes files, writes nothing. Stdlib-only.
//
// CLI: node framework/tools/enumerate-inputs.cjs <documentation_dir>
//   → stdout JSON { files: [{ relpath, sha256, mtime }], stadium_units: [{ relpath, kind }] }

const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');

const ordinal = (a, b) => (a < b ? -1 : a > b ? 1 : 0);

// IX-03: a directory that directly holds administration.db, App_Data/Updates/*.sapz, or ClientApp/.
function isStadiumDir(dir) {
  const has = (p, dirWanted) => {
    try { const s = fs.statSync(path.join(dir, p)); return dirWanted ? s.isDirectory() : s.isFile(); } catch { return false; }
  };
  if (has('administration.db', false) || has('ClientApp', true)) return true;
  try {
    return fs.readdirSync(path.join(dir, 'App_Data', 'Updates')).some((n) => n.toLowerCase().endsWith('.sapz'));
  } catch { return false; }
}

function enumerate(root) {
  const files = [];
  const units = [];
  const walk = (abs, rel) => {
    for (const ent of fs.readdirSync(abs, { withFileTypes: true })) {
      const name = ent.name;
      const childRel = rel ? `${rel}/${name}` : name;
      const childAbs = path.join(abs, name);
      if (name.startsWith('.')) continue; // IX-01 — and a dot-directory is pruned
      if (ent.isDirectory()) {
        if (isStadiumDir(childAbs)) { units.push({ relpath: childRel, kind: 'folder' }); continue; } // IX-03, pruned
        if (name === 'embedded' && !rel.includes('/') && rel.endsWith('.stadium-assets')) continue; // IX-04
        walk(childAbs, childRel);
        continue;
      }
      if (!ent.isFile()) continue;
      if (name.endsWith('.converted.md')) continue; // IX-02
      if (name.endsWith('.stadium')) { units.push({ relpath: childRel, kind: 'pointer' }); continue; } // IX-03
      const bytes = fs.readFileSync(childAbs);
      files.push({
        relpath: childRel,
        sha256: crypto.createHash('sha256').update(bytes).digest('hex'),
        mtime: fs.statSync(childAbs).mtime.toISOString(),
      });
    }
  };
  walk(root, '');
  files.sort((a, b) => ordinal(a.relpath, b.relpath));
  units.sort((a, b) => ordinal(a.relpath, b.relpath));
  return { files, stadium_units: units };
}

module.exports = { enumerate };

if (require.main === module) {
  const dir = process.argv[2];
  if (!dir) { process.stderr.write('usage: node framework/tools/enumerate-inputs.cjs <documentation_dir>\n'); process.exit(2); }
  process.stdout.write(JSON.stringify(enumerate(dir), null, 2) + '\n');
}
