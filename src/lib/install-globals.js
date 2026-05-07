// Global install: symlinks the framework's .claude/skills/ and .claude/agents/
// subdirectories into ~/.claude/skills/ and ~/.claude/agents/ so Claude Code
// picks them up across all projects. Near-verbatim port of
// super-claudio-code/src/commands/init.js:128-217 — source paths point at
// `<framework>/.claude/skills/` (not `<framework>/skills/`) because the
// research framework keeps skills under .claude/.

import { mkdir, access, symlink, readlink, unlink, readdir } from 'node:fs/promises';
import { join, resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { homedir } from 'node:os';

const __dirname = dirname(fileURLToPath(import.meta.url));
const FRAMEWORK_ROOT = resolve(__dirname, '../..');

async function fileExists(path) {
  try {
    await access(path);
    return true;
  } catch {
    return false;
  }
}

async function installSkills() {
  const skillsSource = join(FRAMEWORK_ROOT, '.claude', 'skills');
  const skillsDir = join(homedir(), '.claude', 'skills');

  await mkdir(skillsDir, { recursive: true });

  let entries;
  try {
    entries = await readdir(skillsSource, { withFileTypes: true });
  } catch {
    console.log('  · Skills source not found (skipping)');
    return;
  }

  const skillDirs = entries.filter((e) => e.isDirectory());
  let installed = 0;

  for (const dir of skillDirs) {
    const source = join(skillsSource, dir.name);
    const target = join(skillsDir, dir.name);

    try {
      const existing = await readlink(target).catch(() => null);
      if (existing === source) continue;

      if (existing !== null) await unlink(target);

      await symlink(source, target, 'dir');
      installed++;
    } catch {
      // Target exists as a real directory — don't overwrite user's files
    }
  }

  if (installed > 0) {
    console.log(`  ✓ ~/.claude/skills/ (${installed} skills linked)`);
  } else {
    console.log('  · ~/.claude/skills/ (skills already installed)');
  }
}

async function installAgents() {
  const agentsSource = join(FRAMEWORK_ROOT, '.claude', 'agents');
  const agentsDir = join(homedir(), '.claude', 'agents');

  await mkdir(agentsDir, { recursive: true });

  let entries;
  try {
    entries = await readdir(agentsSource, { withFileTypes: true });
  } catch {
    console.log('  · Agents source not found (skipping)');
    return;
  }

  const agentFiles = entries.filter((e) => e.isFile() && e.name.endsWith('.md'));
  let installed = 0;

  for (const file of agentFiles) {
    const source = join(agentsSource, file.name);
    const target = join(agentsDir, file.name);

    try {
      const existing = await readlink(target).catch(() => null);
      if (existing === source) continue;

      if (existing !== null) {
        await unlink(target);
      } else if (await fileExists(target)) {
        continue;
      }

      await symlink(source, target);
      installed++;
    } catch {
      // Target exists as a real file — don't overwrite
    }
  }

  if (installed > 0) {
    console.log(`  ✓ ~/.claude/agents/ (${installed} agents linked)`);
  } else {
    console.log('  · ~/.claude/agents/ (agents already installed or none to install)');
  }
}

export async function installGlobals() {
  console.log('');
  console.log('Installing global skills/agents to ~/.claude/');
  await installSkills();
  await installAgents();
}
