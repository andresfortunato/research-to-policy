import { mkdir, copyFile, writeFile, access } from 'node:fs/promises';
import { join, dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const FRAMEWORK_ROOT = resolve(__dirname, '../..');

const SLUG_PATTERN = /^[a-z][a-z0-9-]*$/;

async function fileExists(path) {
  try {
    await access(path);
    return true;
  } catch {
    return false;
  }
}

async function copyIfAbsent(src, dst, label) {
  if (await fileExists(dst)) {
    console.log(`  ~ ${label} (exists, skipping)`);
    return;
  }
  await mkdir(dirname(dst), { recursive: true });
  await copyFile(src, dst);
  console.log(`  + ${label}`);
}

async function writeIfAbsent(dst, contents, label) {
  if (await fileExists(dst)) {
    console.log(`  ~ ${label} (exists, skipping)`);
    return;
  }
  await mkdir(dirname(dst), { recursive: true });
  await writeFile(dst, contents);
  console.log(`  + ${label}`);
}

export async function planInit(slug) {
  if (!slug) {
    console.error('Error: slug is required.');
    console.error('Usage: scr plan init <slug>');
    process.exit(1);
  }

  const cleanSlug = slug.replace(/^plan-/, '');

  if (!SLUG_PATTERN.test(cleanSlug)) {
    console.error(
      `Error: slug "${cleanSlug}" must be lowercase letters, digits, or hyphens, starting with a letter.`,
    );
    console.error('Examples: wage-gaps, eph-harmonization, deflator-choice');
    process.exit(1);
  }

  const target = process.cwd();
  const planDir = join(target, 'plan', `plan-${cleanSlug}`);

  console.log(`Scaffolding plan-${cleanSlug} in ${target}`);

  await mkdir(planDir, { recursive: true });
  await mkdir(join(planDir, 'phases'), { recursive: true });
  await mkdir(join(planDir, 'context'), { recursive: true });

  await copyIfAbsent(
    join(FRAMEWORK_ROOT, 'templates/plan/plan.md'),
    join(planDir, 'plan.md'),
    `plan/plan-${cleanSlug}/plan.md`,
  );

  await copyIfAbsent(
    join(FRAMEWORK_ROOT, 'templates/handoff.md'),
    join(planDir, 'handoff.md'),
    `plan/plan-${cleanSlug}/handoff.md`,
  );

  await writeIfAbsent(
    join(planDir, 'log.md'),
    `# Log: plan-${cleanSlug}\n\nDirection changes, dead ends, and decisions made during implementation.\n`,
    `plan/plan-${cleanSlug}/log.md`,
  );

  console.log('');
  console.log(
    `Done. Edit plan/plan-${cleanSlug}/plan.md to fill in goal, constraints, decisions, and file manifest.`,
  );
}
