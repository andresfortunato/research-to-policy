#!/usr/bin/env node

import { Command } from 'commander';
import { initCommand } from './commands/init.js';

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

program.parse();
