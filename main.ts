import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { join } from 'node:path';

const botDir = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

await mkdir(outputDir, { recursive: true });
const launchPath = join(botDir, 'LAUNCH.json');
const launchBytes = await readFile(launchPath);
const launch = JSON.parse(launchBytes.toString('utf8')) as Record<string, unknown>;
const base58 = /^[1-9A-HJ-NP-Za-km-z]+$/;

for (const field of ['mint', 'create_signature']) {
  if (typeof launch[field] !== 'string' || !base58.test(launch[field] as string)) {
    throw new Error(`LAUNCH.json must contain a non-empty base58 ${field}`);
  }
}

await writeFile(join(outputDir, 'LAUNCH.json'), launchBytes);
