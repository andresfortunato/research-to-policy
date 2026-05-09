import { planInit } from '../lib/plan-init.js';

export async function planInitCommand(slug) {
  await planInit(slug);
}
