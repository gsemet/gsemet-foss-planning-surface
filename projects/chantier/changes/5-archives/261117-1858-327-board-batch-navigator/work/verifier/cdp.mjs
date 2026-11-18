// Minimal Chrome DevTools Protocol driver (headless Chrome), used to check the board in a browser.
import { spawn } from 'node:child_process';
import fs from 'node:fs';
export async function launch(profile, port = 9333) {
  const p = spawn('C:/Program Files/Google/Chrome/Application/chrome.exe', [
    '--headless=new', `--remote-debugging-port=${port}`, `--user-data-dir=${profile}`,
    '--no-first-run', '--window-size=1280,1000', 'about:blank'], { stdio: 'ignore' });
  let v;
  for (let i = 0; i < 50; i++) {
    try { v = await (await fetch(`http://127.0.0.1:${port}/json/version`)).json(); break; }
    catch { await new Promise(r => setTimeout(r, 200)); }
  }
  const ws = new WebSocket(v.webSocketDebuggerUrl);
  await new Promise(r => ws.addEventListener('open', r));
  let id = 0; const pend = new Map(); const events = [];
  ws.addEventListener('message', m => {
    const d = JSON.parse(m.data);
    if (d.id && pend.has(d.id)) { pend.get(d.id)(d); pend.delete(d.id); } else events.push(d);
  });
  const send = (method, params = {}, sessionId) => new Promise(res => {
    const i = ++id; pend.set(i, res); ws.send(JSON.stringify({ id: i, method, params, sessionId }));
  });
  return { proc: p, send, events, ws, port };
}
export async function page(b, url, w = 1280, h = 1000) {
  const { result } = (await b.send('Target.createTarget', { url: 'about:blank' }));
  const t = result.targetId;
  const { result: a } = await b.send('Target.attachToTarget', { targetId: t, flatten: true });
  const sid = a.sessionId;
  const s = (m, p) => b.send(m, p, sid);
  await s('Page.enable'); await s('Runtime.enable');
  await s('Emulation.setDeviceMetricsOverride', { width: w, height: h, deviceScaleFactor: 1, mobile: false });
  const api = {
    sid, t,
    async goto(u) { await s('Page.navigate', { url: u }); await new Promise(r => setTimeout(r, 1500)); },
    async ev(expr) {
      const r = await s('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true, userGesture: true });
      if (r.result.exceptionDetails) return { error: JSON.stringify(r.result.exceptionDetails.exception || r.result.exceptionDetails).slice(0, 400) };
      return r.result.result.value;
    },
    async wait(ms = 800) { await new Promise(r => setTimeout(r, ms)); },
    async shot(file) {
      const r = await s('Page.captureScreenshot', { format: 'png' });
      fs.writeFileSync(file, Buffer.from(r.result.data, 'base64'));
    },
    s,
  };
  if (url) await api.goto(url);
  return api;
}
