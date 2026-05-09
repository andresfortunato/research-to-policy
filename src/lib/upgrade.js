// Upgrade flow: pulls framework changes (under .claude/conventions/ and
// templates/) into a target project non-destructively. For each candidate
// file:
//   - absent in project           → copy in (log "+ <rel>")
//   - present and byte-identical  → silent skip
//   - present and divergent       → write "<rel>.framework-new" sidecar
//     (never overwrite the live file) and add to a tally
//
// At the end, prints a one-line summary and (separately) a one-line warning
// if the project still has the obsolete <project>/.claude/skills/ directory
// from a pre-Phase-3 install layout. Never auto-deletes anything.
//
// Excludes: files the user actively customizes — CLAUDE.md.template (the
// user edits CLAUDE.md immediately on install), various INDEX.md / log.md /
// registry.yaml / wiki-index files the user appends rows or content to, and
// loose template files (handoff.md, decision-record.md) that don't have a
// fixed project counterpart.

import {
  mkdir,
  copyFile,
  readFile,
  writeFile,
  access,
  stat,
  chmod,
  readdir,
} from 'node:fs/promises';
import { join, dirname, relative, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const FRAMEWORK_ROOT = resolve(__dirname, '../..');

// Paths are relative to FRAMEWORK_ROOT. Match exactly.
const EXCLUDE = new Set([
  'templates/CLAUDE.md.template',
  'templates/insights/INDEX.md',
  'templates/wiki/index.md',
  'templates/wiki/log.md',
  'templates/sources/registry.yaml',
  'templates/data_sources/INDEX.md',
  'templates/project_conventions/INDEX.md',
  // Archivist appends rows here across sessions; framework never overwrites.
  'templates/archive/index.md',
  // Loose templates referenced from convention docs; no fixed project copy.
  'templates/handoff.md',
  'templates/decision-record.md',
]);

async function fileExists(path) {
  try {
    await access(path);
    return true;
  } catch {
    return false;
  }
}

async function isFrameworkRepo(target) {
  const pkgPath = join(target, 'package.json');
  if (!(await fileExists(pkgPath))) return false;
  try {
    const pkg = JSON.parse(await readFile(pkgPath, 'utf-8'));
    return pkg.name === 'research-to-policy';
  } catch {
    return false;
  }
}

// Project-relative path for a given framework-relative path.
//   templates/foo/bar.md         → foo/bar.md
//   .claude/conventions/x.md     → .claude/conventions/x.md
function toProjectRel(frameworkRel) {
  const prefix = 'templates/';
  if (frameworkRel.startsWith(prefix)) return frameworkRel.slice(prefix.length);
  return frameworkRel;
}

// Recursively yield framework-relative file paths under `frameworkRel`.
async function* walkFiles(frameworkRel) {
  const absDir = join(FRAMEWORK_ROOT, frameworkRel);
  let entries;
  try {
    entries = await readdir(absDir, { withFileTypes: true });
  } catch {
    return;
  }
  for (const entry of entries) {
    if (entry.name === '.gitkeep') continue;
    const childRel = `${frameworkRel}/${entry.name}`;
    if (entry.isDirectory()) {
      yield* walkFiles(childRel);
    } else if (entry.isFile()) {
      yield childRel;
    }
  }
}

async function compareFiles(srcPath, dstPath) {
  const srcStat = await stat(srcPath);
  const dstStat = await stat(dstPath);
  if (srcStat.size !== dstStat.size) return false;
  const [srcBuf, dstBuf] = await Promise.all([readFile(srcPath), readFile(dstPath)]);
  return srcBuf.equals(dstBuf);
}

export async function upgradeProject(target) {
  if (await isFrameworkRepo(target)) {
    console.log('Refusing to run r2p init --upgrade against the framework repo itself.');
    console.log('  r2p init --upgrade is for target research projects, not research-to-policy.');
    return false;
  }

  console.log(`Upgrading research-to-policy framework files in: ${target}`);

  const candidates = [];
  for await (const rel of walkFiles('.claude/conventions')) candidates.push(rel);
  for await (const rel of walkFiles('.claude/hooks')) candidates.push(rel);
  for await (const rel of walkFiles('templates')) {
    if (!EXCLUDE.has(rel)) candidates.push(rel);
  }
  // settings.template.json is a single tracked file — surface as sidecar so
  // users can diff against their runtime .claude/settings.json.
  candidates.push('.claude/settings.template.json');

  let copied = 0;
  let identical = 0;
  const sidecars = [];

  for (const frameworkRel of candidates) {
    const srcPath = join(FRAMEWORK_ROOT, frameworkRel);
    const projectRel = toProjectRel(frameworkRel);
    const dstPath = join(target, projectRel);

    if (!(await fileExists(dstPath))) {
      await mkdir(dirname(dstPath), { recursive: true });
      await copyFile(srcPath, dstPath);
      if (projectRel.startsWith('.claude/hooks/') && projectRel.endsWith('.sh')) {
        await chmod(dstPath, 0o755);
      }
      console.log(`  + ${projectRel}`);
      copied++;
      continue;
    }

    if (await compareFiles(srcPath, dstPath)) {
      identical++;
      continue;
    }

    const sidecarPath = `${dstPath}.framework-new`;
    await copyFile(srcPath, sidecarPath);
    const sidecarRel = relative(target, sidecarPath);
    console.log(`  ⚠ ${sidecarRel} (divergent — sidecar written, original untouched)`);
    sidecars.push(sidecarRel);
  }

  // Old-shape skills layout warning. Skills now live globally in
  // ~/.claude/skills/; a project-local .claude/skills/ is leftover from the
  // old install.sh layout and should be removed manually.
  const oldSkillsDir = join(target, '.claude', 'skills');
  if (await fileExists(oldSkillsDir)) {
    console.log('');
    console.log(
      '  ⚠ .claude/skills/ exists in this project — obsolete (skills now live globally in ~/.claude/skills/).',
    );
    console.log('    Run `rm -rf .claude/skills/` to clean up. Not deleting automatically.');
  }

  console.log('');
  if (sidecars.length === 0 && copied === 0) {
    console.log('No upgrades needed — project is in sync with the framework.');
  } else if (sidecars.length === 0) {
    console.log(`Upgrade complete: ${copied} new file(s) added, ${identical} unchanged.`);
  } else {
    console.log(
      `${sidecars.length} file(s) have framework-new sidecars; review with \`git diff\` or your editor.`,
    );
    if (copied > 0) console.log(`  (${copied} new file(s) added, ${identical} unchanged.)`);
  }

  return true;
}
