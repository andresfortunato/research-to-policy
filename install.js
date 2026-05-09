#!/usr/bin/env node

// Post-install script for Research to Policy.
// Delegates to `r2p init` which handles per-project scaffolding and global
// skills/agents symlinks. This script exists for npm postinstall — it resolves
// the project root and runs init.

import { accessSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));

async function main() {
  const projectRoot = findProjectRoot();

  console.log('Research to Policy — setting up project...\n');

  const { initCommand } = await import('./src/commands/init.js');
  const origCwd = process.cwd();
  process.chdir(projectRoot);
  await initCommand();
  process.chdir(origCwd);

  console.log('\nResearch to Policy ready.');
}

function findProjectRoot() {
  if (process.env.INIT_CWD) return process.env.INIT_CWD;

  let dir = process.cwd();
  while (dir !== dirname(dir)) {
    try {
      accessSync(join(dir, 'package.json'));
      return dir;
    } catch {
      dir = dirname(dir);
    }
  }
  return process.cwd();
}

main().catch(err => {
  console.error('R2P install failed:', err.message);
  process.exit(1);
});
