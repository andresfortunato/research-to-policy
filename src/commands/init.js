// Phase 3: per-project install + global skills/agents symlinks.
// Phase 4 will add the --upgrade flow via src/lib/upgrade.js.

import { installProject, printNextSteps } from '../lib/install-project.js';
import { installGlobals } from '../lib/install-globals.js';

export async function initCommand(options = {}) {
  if (options.upgrade) {
    console.log('scr init --upgrade: not implemented yet (Phase 4)');
    return;
  }

  const target = process.cwd();
  const ok = await installProject(target);
  if (!ok) return;

  await installGlobals();
  printNextSteps();
}
