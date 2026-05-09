#!/usr/bin/env node

import { Command } from 'commander';
import { initCommand } from './commands/init.js';
import { planInitCommand } from './commands/plan.js';

const program = new Command();

program
  .name('scr')
  .description('Super Claudio Research — research-engagement framework for Claude Code')
  .version('0.1.0');

program
  .command('init')
  .description('Scaffold a research project with framework conventions, hooks, and global skills/agents')
  .option('--upgrade', 'Refresh framework-tracked files; emit .framework-new sidecars on divergence')
  .action(initCommand);

const planCmd = program
  .command('plan')
  .description('Manage research plans (multi-session work captured in plan/plan-<slug>/)');

planCmd
  .command('init <slug>')
  .description('Scaffold plan/plan-<slug>/{plan.md, handoff.md, log.md, phases/, context/}')
  .action(planInitCommand);

program.parse();
