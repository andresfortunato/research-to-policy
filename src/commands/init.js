// Phase 1 stub — proves the distribution path is wired.
// Phase 2 ports install.sh's per-project work into src/lib/install-project.js.
// Phase 3 adds global skills/agents symlinks via src/lib/install-globals.js.
// Phase 4 adds the --upgrade flow via src/lib/upgrade.js.

export async function initCommand(options = {}) {
  if (options.upgrade) {
    console.log('scr init --upgrade: not implemented yet (Phase 1 stub)');
  } else {
    console.log('scr init: not implemented yet (Phase 1 stub)');
  }
}
