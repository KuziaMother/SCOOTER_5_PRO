// Нон-интерактивный драйвер для `bubblewrap init` (без TTY).
// Вызывает реальные init()/loadOrCreateConfig() из @bubblewrap/cli с
// scripted-промптом: ответы выбираются по ТЕКСТУ вопроса, не по позиции.
import { createRequire } from 'node:module';
import { existsSync, readdirSync } from 'node:fs';
import os from 'node:os';

const require = createRequire(import.meta.url);
// Ищем @bubblewrap/cli в кэше npx (хэш-каталог меняется от версии/машин).
function findBwCli() {
  const npxDir = process.env.NPM_CONFIG_CACHE
    || (process.platform === 'win32'
      ? `${os.homedir()}\\AppData\\Local\\npm-cache\\_npx`
      : `${os.homedir()}/.npm/_npx`);
  for (const d of readdirSync(npxDir, { withFileTypes: true }).filter(e => e.isDirectory())) {
    const p = `${npxDir}/${d.name}/node_modules/@bubblewrap/cli`;
    if (existsSync(p)) return p;
  }
  throw new Error('@bubblewrap/cli не найден в кэше npx — сначала прогоните `npx -y @bubblewrap/cli version`');
}
const BW_CLI = findBwCli();
const { InquirerPrompt } = require(BW_CLI + '/dist/lib/Prompt.js');
const { loadOrCreateConfig } = require(BW_CLI + '/dist/lib/config.js');
const { init } = require(BW_CLI + '/dist/lib/cmds/init.js');

const RULES = [
  [/install the Android SDK/i, 'y'],
  [/terms and conditions/i, 'y'],
  [/Application ID:/i, 'ru.scooter5pro.app'],
  [/Short name:/i, 'Scooter 5Pro'], // ≤12 символов
  [/Play billing/i, 'n'],
  [/Location delegation/i, 'n'],
  [/create one now/i, 'y'],
  [/First and Last names/i, 'Scooter 5 Pro'],
  [/Organizational Unit/i, 'home'],
  [/Organization \(eg/i, 'entosis'],
  [/Country/i, 'RU'],
  [/Password for the Key Store/i, 'scooter5pro-key-2026'],
  [/Password for the Key:/i, 'scooter5pro-key-2026'],
];

class ScriptedPrompt extends InquirerPrompt {
  pick(message, def) {
    for (const [re, a] of RULES) if (re.test(message)) return a;
    return def;
  }
  async promptInput(message, def, validate) {
    const val = this.pick(message, def);
    console.log(`[Q input ] ${message.trim()} => ${JSON.stringify(val)}`);
    const r = await validate(val);
    if (!r.isOk()) throw new Error(`invalid answer for "${message}": ${r.unwrapError().message}`);
    return r.unwrap();
  }
  async promptChoice(message, choices, def, validate) {
    const val = this.pick(message, def);
    console.log(`[Q choice] ${message.trim()} => ${JSON.stringify(val)}`);
    const r = await validate(val);
    if (!r.isOk()) throw new Error(`invalid answer for "${message}": ${r.unwrapError().message}`);
    return r.unwrap();
  }
  async promptConfirm(message, def) {
    const a = this.pick(message, def ? 'y' : 'n');
    console.log(`[Q confirm] ${message.trim()} => ${a}`);
    return /^y/i.test(String(a));
  }
  async promptPassword(message, validate) {
    const val = this.pick(message, '');
    console.log(`[Q passwrd] ${message.trim()} => <set>`);
    const r = await validate(val);
    if (!r.isOk()) throw new Error(`invalid answer for "${message}"`);
    return r.unwrap();
  }
}

// git-bash/MSYS экспортирует PATH (верхний регистр), а JdkHelper на win32 пишет
// в 'Path' → JDK-bin не попадает в действующий PATH, keytool не находится.
// Переименовываем до любого вызова bubblewrap.
if (process.env.PATH && !process.env.Path) {
  process.env.Path = process.env.PATH;
  delete process.env.PATH;
}

const prompt = new ScriptedPrompt();
process.chdir('D:/SCOOTER_5_PRO/mobile/twa');

console.log('=== loadOrCreateConfig (SDK install) ===');
const config = await loadOrCreateConfig(undefined, prompt);
console.log('config:', JSON.stringify(config));

console.log('=== init ===');
// host БЕЗ порта: validateHost (domainToASCII) отклоняет любые "host:port".
const ok = await init({ manifest: process.env.BW_MANIFEST || 'http://127.0.0.1/manifest.webmanifest' }, config, prompt);
console.log(ok ? 'INIT OK' : 'INIT FAILED');
process.exit(ok ? 0 : 1);
