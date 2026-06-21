// Encrypts an HTML file with a password (AES-256-GCM, PBKDF2-SHA256).
// The output is a single self-contained HTML: it only decrypts in the browser
// once the correct password is entered — no server, no plan, host anywhere.
//
// Usage:  node build-protected.mjs <input.html> <output.html> "<password>"
import { readFileSync, writeFileSync } from 'node:fs';

const [, , inFile, outFile, password] = process.argv;
if (!inFile || !outFile || !password) {
  console.error('Usage: node build-protected.mjs <input.html> <output.html> "<password>"');
  process.exit(1);
}

const ITER = 250000;
const html = readFileSync(inFile); // Buffer (UTF-8 bytes)
const enc = new TextEncoder();
const salt = crypto.getRandomValues(new Uint8Array(16));
const iv = crypto.getRandomValues(new Uint8Array(12));

const keyMat = await crypto.subtle.importKey('raw', enc.encode(password), 'PBKDF2', false, ['deriveKey']);
const key = await crypto.subtle.deriveKey(
  { name: 'PBKDF2', salt, iterations: ITER, hash: 'SHA-256' },
  keyMat,
  { name: 'AES-GCM', length: 256 },
  false,
  ['encrypt']
);
const ct = new Uint8Array(await crypto.subtle.encrypt({ name: 'AES-GCM', iv }, key, html));
const b64 = (u8) => Buffer.from(u8).toString('base64');

const gate = `<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Tesote &times; CAPCA</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@400;500&family=JetBrains+Mono&display=swap" rel="stylesheet">
<style>
  :root { --bg:#fafbfd; --surface:#fff; --line:rgba(13,17,23,0.12); --text:#0d1117; --dim:#4a5260; --faint:#97a1ae; --blue:#1661e2; --serif:'Instrument Serif',Georgia,serif; --sans:'Inter',-apple-system,sans-serif; --mono:'JetBrains Mono',monospace; }
  * { margin:0; padding:0; box-sizing:border-box; }
  body { background:var(--bg); color:var(--text); font-family:var(--sans); min-height:100vh; display:flex; align-items:center; justify-content:center; padding:24px; -webkit-font-smoothing:antialiased; }
  .card { width:100%; max-width:420px; text-align:center; }
  .eyebrow { font-family:var(--mono); font-size:12px; letter-spacing:0.22em; text-transform:uppercase; color:var(--faint); margin-bottom:22px; }
  h1 { font-family:var(--serif); font-weight:400; font-size:46px; line-height:1.05; letter-spacing:-0.01em; margin-bottom:14px; }
  h1 em { font-style:italic; color:var(--blue); }
  p.sub { color:var(--dim); font-size:15px; line-height:1.6; margin-bottom:30px; }
  form { display:flex; flex-direction:column; gap:12px; }
  input { font-family:var(--sans); font-size:16px; padding:14px 16px; border:1px solid var(--line); border-radius:10px; background:var(--surface); color:var(--text); outline:none; transition:border-color .15s; text-align:center; }
  input:focus { border-color:var(--blue); }
  button { font-family:var(--sans); font-size:15px; font-weight:500; padding:14px 16px; border:none; border-radius:10px; background:var(--blue); color:#fff; cursor:pointer; transition:opacity .15s; }
  button:hover { opacity:.9; }
  button:disabled { opacity:.5; cursor:default; }
  .err { color:#c2452f; font-size:13px; min-height:18px; margin-top:4px; font-family:var(--mono); letter-spacing:0.02em; }
  .foot { margin-top:28px; font-family:var(--mono); font-size:11px; letter-spacing:0.06em; color:var(--faint); }
</style>
</head>
<body>
  <div class="card">
    <div class="eyebrow">tesote &times; capca</div>
    <h1>Documento <em>privado.</em></h1>
    <p class="sub">Este contenido est&aacute; protegido. Ingresa la clave para acceder.</p>
    <form id="f" autocomplete="off">
      <input id="pw" type="password" placeholder="Clave de acceso" autofocus aria-label="Clave de acceso">
      <button id="b" type="submit">Acceder</button>
      <div class="err" id="e"></div>
    </form>
    <div class="foot">confidencial</div>
  </div>
<script>
(function () {
  var SALT="__SALT__", IV="__IV__", CT="__CT__", ITER=__ITER__;
  var b64 = function (s) { return Uint8Array.from(atob(s), function (c) { return c.charCodeAt(0); }); };
  var f = document.getElementById('f'), pw = document.getElementById('pw'),
      b = document.getElementById('b'), e = document.getElementById('e');
  f.addEventListener('submit', function (ev) {
    ev.preventDefault();
    e.textContent = ''; b.disabled = true; b.textContent = 'Abriendo…';
    (async function () {
      try {
        var enc = new TextEncoder();
        var km = await crypto.subtle.importKey('raw', enc.encode(pw.value), 'PBKDF2', false, ['deriveKey']);
        var key = await crypto.subtle.deriveKey(
          { name:'PBKDF2', salt:b64(SALT), iterations:ITER, hash:'SHA-256' },
          km, { name:'AES-GCM', length:256 }, false, ['decrypt']);
        var pt = await crypto.subtle.decrypt({ name:'AES-GCM', iv:b64(IV) }, key, b64(CT));
        var html = new TextDecoder().decode(pt);
        document.open(); document.write(html); document.close();
      } catch (err) {
        e.textContent = 'Clave incorrecta'; b.disabled = false; b.textContent = 'Acceder';
        pw.select();
      }
    })();
  });
})();
</script>
</body>
</html>`;

const out = gate
  .replace('__SALT__', b64(salt))
  .replace('__IV__', b64(iv))
  .replace('__CT__', b64(ct))
  .replace('__ITER__', String(ITER));

writeFileSync(outFile, out);
console.log('Wrote ' + outFile + ' (' + (out.length / 1024).toFixed(0) + ' KB) — password set.');
