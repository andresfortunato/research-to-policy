// Phase 2: per-project install wired in.
// Phase 3 will add global skills/agents symlinks via src/lib/install-globals.js.
// Phase 4 will add the --upgrade flow via src/lib/upgrade.js.

import { installProject, printNextSteps } from '../lib/install-project.js';

export async function initCommand(options = {}) {
  if (options.upgrade) {
    console.log('scr init --upgrade: not implemented yet (Phase 4)');
    return;
  }

  const target = process.cwd();
  const ok = await installProject(target);
  if (ok) printNextSteps();
}
