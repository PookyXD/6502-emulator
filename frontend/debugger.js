const OPCODES = {
  0xA9:'LDA',0xA5:'LDA',0xB5:'LDA',0xAD:'LDA',0xBD:'LDA',0xB9:'LDA',0xA1:'LDA',0xB1:'LDA',
  0xA2:'LDX',0xA6:'LDX',0xB6:'LDX',0xAE:'LDX',0xBE:'LDX',
  0xA0:'LDY',0xA4:'LDY',0xB4:'LDY',0xAC:'LDY',0xBC:'LDY',
  0x85:'STA',0x95:'STA',0x8D:'STA',0x9D:'STA',0x99:'STA',0x81:'STA',0x91:'STA',
  0x86:'STX',0x96:'STX',0x8E:'STX',
  0x84:'STY',0x94:'STY',0x8C:'STY',
  0x69:'ADC',0x65:'ADC',0x75:'ADC',0x6D:'ADC',0x7D:'ADC',0x79:'ADC',0x61:'ADC',0x71:'ADC',
  0xE9:'SBC',0xE5:'SBC',0xF5:'SBC',0xED:'SBC',0xFD:'SBC',0xF9:'SBC',0xE1:'SBC',0xF1:'SBC',
  0x29:'AND',0x25:'AND',0x35:'AND',0x2D:'AND',0x3D:'AND',0x39:'AND',0x21:'AND',0x31:'AND',
  0x09:'ORA',0x05:'ORA',0x15:'ORA',0x0D:'ORA',0x1D:'ORA',0x19:'ORA',0x01:'ORA',0x11:'ORA',
  0x49:'EOR',0x45:'EOR',0x55:'EOR',0x4D:'EOR',0x5D:'EOR',0x59:'EOR',0x41:'EOR',0x51:'EOR',
  0x0A:'ASL',0x06:'ASL',0x16:'ASL',0x0E:'ASL',0x1E:'ASL',
  0x4A:'LSR',0x46:'LSR',0x56:'LSR',0x4E:'LSR',0x5E:'LSR',
  0x2A:'ROL',0x26:'ROL',0x36:'ROL',0x2E:'ROL',0x3E:'ROL',
  0x6A:'ROR',0x66:'ROR',0x76:'ROR',0x6E:'ROR',0x7E:'ROR',
  0xC9:'CMP',0xC5:'CMP',0xD5:'CMP',0xCD:'CMP',0xDD:'CMP',0xD9:'CMP',0xC1:'CMP',0xD1:'CMP',
  0xE0:'CPX',0xE4:'CPX',0xEC:'CPX',
  0xC0:'CPY',0xC4:'CPY',0xCC:'CPY',
  0x24:'BIT',0x2C:'BIT',
  0x90:'BCC',0xB0:'BCS',0xF0:'BEQ',0xD0:'BNE',0x30:'BMI',0x10:'BPL',0x50:'BVC',0x70:'BVS',
  0x4C:'JMP',0x6C:'JMP',0x20:'JSR',0x60:'RTS',
  0x48:'PHA',0x68:'PLA',0x08:'PHP',0x28:'PLP',
  0xAA:'TAX',0xA8:'TAY',0x8A:'TXA',0x98:'TYA',0xBA:'TSX',0x9A:'TXS',
  0xE6:'INC',0xF6:'INC',0xEE:'INC',0xFE:'INC',
  0xC6:'DEC',0xD6:'DEC',0xCE:'DEC',0xDE:'DEC',
  0xE8:'INX',0xC8:'INY',0xCA:'DEX',0x88:'DEY',
  0x18:'CLC',0x38:'SEC',0x58:'CLI',0x78:'SEI',0xB8:'CLV',0xD8:'CLD',0xF8:'SED',
  0xEA:'NOP',0x00:'BRK',
};

const ADDR_MODES = {
  0xA9:'#imm', 0xA5:'zp', 0xB5:'zp,x', 0xAD:'abs', 0xBD:'abs,x', 0xB9:'abs,y',
  0xA1:'(ind,x)', 0xB1:'(ind),y',
  0xA2:'#imm', 0xA6:'zp', 0xB6:'zp,y', 0xAE:'abs', 0xBE:'abs,y',
  0xA0:'#imm', 0xA4:'zp', 0xB4:'zp,x', 0xAC:'abs', 0xBC:'abs,x',
  0x85:'zp', 0x95:'zp,x', 0x8D:'abs', 0x9D:'abs,x', 0x99:'abs,y', 0x81:'(ind,x)', 0x91:'(ind),y',
  0x86:'zp', 0x96:'zp,y', 0x8E:'abs',
  0x84:'zp', 0x94:'zp,x', 0x8C:'abs',
  0x69:'#imm', 0x65:'zp', 0x75:'zp,x', 0x6D:'abs', 0x7D:'abs,x', 0x79:'abs,y', 0x61:'(ind,x)', 0x71:'(ind),y',
  0xE9:'#imm', 0xE5:'zp', 0xF5:'zp,x', 0xED:'abs', 0xFD:'abs,x', 0xF9:'abs,y', 0xE1:'(ind,x)', 0xF1:'(ind),y',
  0x29:'#imm', 0x25:'zp', 0x35:'zp,x', 0x2D:'abs', 0x3D:'abs,x', 0x39:'abs,y', 0x21:'(ind,x)', 0x31:'(ind),y',
  0x09:'#imm', 0x05:'zp', 0x15:'zp,x', 0x0D:'abs', 0x1D:'abs,x', 0x19:'abs,y', 0x01:'(ind,x)', 0x11:'(ind),y',
  0x49:'#imm', 0x45:'zp', 0x55:'zp,x', 0x4D:'abs', 0x5D:'abs,x', 0x59:'abs,y', 0x41:'(ind,x)', 0x51:'(ind),y',
  0x0A:'acc', 0x06:'zp', 0x16:'zp,x', 0x0E:'abs', 0x1E:'abs,x',
  0x4A:'acc', 0x46:'zp', 0x56:'zp,x', 0x4E:'abs', 0x5E:'abs,x',
  0x2A:'acc', 0x26:'zp', 0x36:'zp,x', 0x2E:'abs', 0x3E:'abs,x',
  0x6A:'acc', 0x66:'zp', 0x76:'zp,x', 0x6E:'abs', 0x7E:'abs,x',
  0xC9:'#imm', 0xC5:'zp', 0xD5:'zp,x', 0xCD:'abs', 0xDD:'abs,x', 0xD9:'abs,y', 0xC1:'(ind,x)', 0xD1:'(ind),y',
  0xE0:'#imm', 0xE4:'zp', 0xEC:'abs',
  0xC0:'#imm', 0xC4:'zp', 0xCC:'abs',
  0x24:'zp', 0x2C:'abs',
  0x90:'rel', 0xB0:'rel', 0xF0:'rel', 0xD0:'rel', 0x30:'rel', 0x10:'rel', 0x50:'rel', 0x70:'rel',
  0x4C:'abs', 0x6C:'(ind)', 0x20:'abs', 0x60:'impl',
  0x48:'impl', 0x68:'impl', 0x08:'impl', 0x28:'impl',
  0xAA:'impl', 0xA8:'impl', 0x8A:'impl', 0x98:'impl', 0xBA:'impl', 0x9A:'impl',
  0xE6:'zp', 0xF6:'zp,x', 0xEE:'abs', 0xFE:'abs,x',
  0xC6:'zp', 0xD6:'zp,x', 0xCE:'abs', 0xDE:'abs,x',
  0xE8:'impl', 0xC8:'impl', 0xCA:'impl', 0x88:'impl',
  0x18:'impl', 0x38:'impl', 0x58:'impl', 0x78:'impl', 0xB8:'impl', 0xD8:'impl', 0xF8:'impl',
  0xEA:'impl', 0x00:'impl',
};

const INSTR_LEN = {
  '#imm': 2, 'zp': 2, 'zp,x': 2, 'zp,y': 2, 'abs': 3, 'abs,x': 3, 'abs,y': 3,
  '(ind,x)': 2, '(ind),y': 2, '(ind)': 3, 'rel': 2, 'acc': 1, 'impl': 1,
};

const SAMPLE_PROGRAM = 'A9 05 AA E8 8D 00 02 00';

const LOAD_ADDRESS = 0x0600;
const MEM_VIEW_LEN = 256;
const MAP_SEGMENTS = 16;

let ws = null;
let prevState = null;
let prevMemCache = {};
let memCache = {};
let loadedRanges = new Set();
let stepCount = 0;
let halted = false;
let nextMnem = '---';
let nextAddr = LOAD_ADDRESS;
let memViewStart = LOAD_ADDRESS;
let running = false;
let wasHalted = false;
let toastTimer = null;

function $(id) { return document.getElementById(id); }

function hex(val, width) {
  return '$' + val.toString(16).toUpperCase().padStart(width, '0');
}

function connect() {
  ws = new WebSocket('ws://127.0.0.1:8000/ws');
  ws.onopen = () => {
    setStatus(true);
    showToast('Connected to emulator');
  };
  ws.onclose = () => {
    setStatus(false);
    setTimeout(connect, 2200);
  };
  ws.onerror = () => setStatus(false);
  ws.onmessage = (e) => {
    const msg = JSON.parse(e.data);
    if (msg.type === 'state') onState(msg.data);
    else if (msg.type === 'loaded') {
      pushLog(null, `LOAD ${msg.bytes_loaded}B`, null, true);
      showToast(`Loaded ${msg.bytes_loaded} bytes at ${hex(LOAD_ADDRESS, 4)}`);
      markLoadedRange(LOAD_ADDRESS, msg.bytes_loaded);
    } else if (msg.type === 'run_complete') {
      running = false;
      if (msg.halted) setCpuState('halted');
      else setCpuState('idle');
      pushLog(null, `RUN ×${msg.steps_executed}`, null);
      showToast(msg.halted ? 'Program halted — inspect state below' : `Ran ${msg.steps_executed} steps`);
    } else if (msg.type === 'error') {
      showToast(msg.message, true);
    }
  };
}

function setCpuState(state) {
  halted = state === 'halted';
  const cpuEl = $('cpu-state');
  cpuEl.className = 'cpu-state ' + state;
  $('cpu-state-lbl').textContent = state.toUpperCase();

  const sbCpu = $('sb-cpu');
  sbCpu.textContent = state.toUpperCase();
  sbCpu.className = 'val'
    + (state === 'halted' ? ' halted' : '')
    + (state === 'running' ? ' running' : '');

  $('cur-inst').classList.toggle('halted-state', state === 'halted');
  const badge = $('halt-badge');
  badge.hidden = state !== 'halted';
  $('halt-hint').hidden = state !== 'halted';
  if (state === 'halted' && prevState) {
    badge.innerHTML = `<span class="halt-badge-icon">■</span> HALTED @ ${hex(prevState.PC, 4)}`;
  }

  const connected = ws && ws.readyState === 1;
  $('btn-step').disabled = !connected || state === 'halted' || running;
  updateRunButton();
}

function setStatus(on) {
  $('sdot').classList.toggle('off', !on);
  $('slbl').textContent = on ? 'CONNECTED' : 'OFFLINE';
  $('sb-conn').textContent = on ? 'ONLINE' : 'OFFLINE';
  document.querySelectorAll('.cbtn[data-action]').forEach(btn => {
    if (btn.id !== 'btn-step') btn.disabled = !on;
  });
  if (on) setCpuState(halted ? 'halted' : running ? 'running' : 'idle');
  else $('btn-step').disabled = true;
}

function onState(s) {
  updateRegs(s);
  updateFlags(s.flags);
  updateStack(s.SP);
  $('cy-val').textContent = String(s.cycles).padStart(8, '0');
  $('sb-cycles').textContent = String(s.cycles);
  $('sb-pc').textContent = hex(s.PC, 4);

  if (prevState !== null) {
    pushLog(prevState.PC, nextMnem, s.cycles);
  }
  $('sb-steps').textContent = String(stepCount);

  if (s.halted) {
    if (!wasHalted) {
      const panel = $('cur-inst');
      panel.classList.remove('halt-flash');
      void panel.offsetWidth;
      panel.classList.add('halt-flash');
      pushLog(s.PC, 'HALT', s.cycles, false, true);
    }
    wasHalted = true;
    running = false;
    setCpuState('halted');
  } else {
    wasHalted = false;
    setCpuState(running ? 'running' : 'idle');
  }

  prevState = s;
  memViewStart = Math.max(0, (s.PC - 64) & 0xFFF0);
  fetchMem(s.PC, s.halted);
  updateMemMap(s.PC);
}

function updateRegs(s) {
  const map = { PC: s.PC, SP: s.SP, A: s.A, X: s.X, Y: s.Y, P: s.P };
  for (const [k, v] of Object.entries(map)) {
    const el = $('rv-' + k);
    const row = $('row-' + k);
    if (!el) continue;
    const wide = k === 'PC';
    const formatted = hex(v, wide ? 4 : 2);
    const changed = prevState && prevState[k] !== v;
    el.textContent = formatted;
    if (changed && k !== 'PC') {
      row.classList.remove('flash');
      void row.offsetWidth;
      row.classList.add('flash');
    }
  }
}

function updateFlags(flags) {
  for (const n of ['N', 'V', 'B', 'D', 'I', 'Z', 'C']) {
    const box = $('fb-' + n);
    if (!box) continue;
    const bit = box.querySelector('.flag-bit');
    bit.textContent = flags[n];
    box.classList.toggle('on', flags[n] === 1);
  }
}

async function updateStack(sp) {
  const stackBase = 0x0100;
  const rows = [];
  for (let i = 0; i < 6; i++) {
    const addr = stackBase + sp + 1 + i;
    if (addr > 0x01FF) break;
    rows.push({ addr, isTop: i === 0 });
  }

  const container = $('stack-viz');
  if (!container) return;

  const values = await Promise.all(
    rows.map(async ({ addr }) => {
      if (memCache[addr] !== undefined) return memCache[addr];
      try {
        const r = await fetch(`http://127.0.0.1:8000/memory?start=${addr}&length=1`);
        const d = await r.json();
        const v = parseInt(d.bytes[0], 16);
        memCache[addr] = v;
        return v;
      } catch {
        return 0;
      }
    })
  );

  container.innerHTML = '';
  rows.forEach(({ addr, isTop }, i) => {
    const row = document.createElement('div');
    row.className = 'stack-row pixel-border' + (isTop ? ' active' : '');
    row.innerHTML =
      `<span class="stack-addr">${hex(addr, 4)}</span>` +
      `<span>${isTop ? '▲ TOP' : 'stack'}</span>` +
      `<span class="stack-val">${hex(values[i], 2)}</span>`;
    container.appendChild(row);
  });
}

function markLoadedRange(start, length) {
  for (let i = start; i < start + length; i++) {
    loadedRanges.add(i);
  }
}

function updateMemMap(pc) {
  const bar = $('mem-map-bar');
  if (!bar) return;
  bar.innerHTML = '';
  const segSize = 65536 / MAP_SEGMENTS;

  for (let i = 0; i < MAP_SEGMENTS; i++) {
    const segStart = i * segSize;
    const segEnd = segStart + segSize;
    const cell = document.createElement('div');
    cell.className = 'mem-map-cell';
    cell.title = `${hex(Math.floor(segStart), 4)} – ${hex(Math.floor(segEnd - 1), 4)}`;

    for (const addr of loadedRanges) {
      if (addr >= segStart && addr < segEnd) {
        cell.classList.add('has-code');
        break;
      }
    }
    if (pc >= segStart && pc < segEnd) cell.classList.add('is-pc');
    cell.addEventListener('click', () => {
      memViewStart = Math.floor(segStart) & 0xFFF0;
      fetchMem(prevState ? prevState.PC : LOAD_ADDRESS, halted);
      showToast(`Viewing ${hex(memViewStart, 4)}`);
    });
    bar.appendChild(cell);
  }
}

async function fetchMem(pc, isHalted = false) {
  const start = memViewStart;
  try {
    const r = await fetch(`http://127.0.0.1:8000/memory?start=${start}&length=${MEM_VIEW_LEN}`);
    const d = await r.json();
    const bytes = d.bytes.map(b => parseInt(b, 16));
    prevMemCache = { ...memCache };
    bytes.forEach((v, i) => { memCache[start + i] = v; });
    renderMem(start, bytes, pc, isHalted);
    const opcode = memCache[pc];
    nextMnem = OPCODES[opcode] || '???';
    nextAddr = pc;
    updateCurInst(pc, opcode, bytes, pc - start);
    renderDisasm(pc);
  } catch (e) {
    showToast('Failed to fetch memory', true);
  }
}

function updateCurInst(pc, opcode, bytes, offsetInView) {
  $('ci-addr').textContent = hex(pc, 4);
  $('ci-mnem').textContent = OPCODES[opcode] || '???';
  $('ci-mode').textContent = ADDR_MODES[opcode] || '';

  const mode = ADDR_MODES[opcode] || 'impl';
  const len = INSTR_LEN[mode] || 1;
  const instrBytes = [];
  for (let i = 0; i < len && offsetInView + i < bytes.length; i++) {
    instrBytes.push(bytes[offsetInView + i]);
  }

  const bytesEl = $('ci-bytes');
  bytesEl.innerHTML = '';
  instrBytes.forEach((b, i) => {
    const el = document.createElement('span');
    el.className = 'ci-byte pixel-border' + (i === 0 ? ' op' : '');
    el.textContent = b.toString(16).toUpperCase().padStart(2, '0');
    bytesEl.appendChild(el);
  });

  let operand = '';
  if (len === 2 && instrBytes[1] !== undefined) {
    operand = hex(instrBytes[1], 2);
  } else if (len === 3 && instrBytes[1] !== undefined) {
    const lo = instrBytes[1];
    const hi = instrBytes[2] ?? 0;
    operand = hex((hi << 8) | lo, 4);
  }
  $('ci-oper').textContent = operand;
}

function disasmAt(addr) {
  const op = memCache[addr];
  if (op === undefined) return null;
  const mode = ADDR_MODES[op] || 'impl';
  const len = INSTR_LEN[mode] || 1;
  const bytes = [];
  for (let i = 0; i < len; i++) {
    if (memCache[addr + i] === undefined) return null;
    bytes.push(memCache[addr + i]);
  }
  let operand = '';
  if (len === 2) operand = hex(bytes[1], 2);
  else if (len === 3) operand = hex((bytes[2] << 8) | bytes[1], 4);
  return { addr, mnem: OPCODES[op] || '???', len, bytes, operand, mode };
}

function renderDisasm(pc) {
  const strip = $('disasm-strip');
  if (!strip) return;

  const curOp = memCache[pc];
  const curMode = ADDR_MODES[curOp] || 'impl';
  const curLen = INSTR_LEN[curMode] || 1;
  let addr = pc + curLen;
  const rows = [];

  for (let i = 0; i < 6 && rows.length < 4; i++) {
    const d = disasmAt(addr);
    if (!d) break;
    rows.push(d);
    addr += d.len;
  }

  if (!rows.length) {
    strip.innerHTML = '';
    return;
  }

  strip.innerHTML =
    '<div class="disasm-label">NEXT · 次の命令</div>' +
    '<div class="disasm-rows">' +
    rows.map(d =>
      `<div class="disasm-row pixel-border">` +
      `<span class="d-addr">${hex(d.addr, 4)}</span>` +
      `<span class="d-bytes">${d.bytes.map(b => b.toString(16).toUpperCase().padStart(2, '0')).join(' ')}</span>` +
      `<span class="d-mn">${d.mnem}</span>` +
      `<span class="d-op">${d.operand}</span>` +
      `<span class="d-op">${d.mode}</span>` +
      `</div>`
    ).join('') +
    '</div>';
}

function renderMem(startAddr, bytes, pc, isHalted = false) {
  const grid = $('mem-grid');
  grid.innerHTML = '';
  const COLS = 16;
  const rows = Math.ceil(bytes.length / COLS);

  for (let r = 0; r < rows; r++) {
    const addr = startAddr + r * COLS;
    const rowEl = document.createElement('div');
    rowEl.className = 'mem-row';

    const addrEl = document.createElement('span');
    addrEl.className = 'mem-addr';
    addrEl.textContent = hex(addr, 4);
    rowEl.appendChild(addrEl);

    const bytesDiv = document.createElement('div');
    bytesDiv.className = 'mem-bytes';
    const asciiDiv = document.createElement('div');
    asciiDiv.className = 'mem-ascii';

    for (let c = 0; c < COLS; c++) {
      const idx = r * COLS + c;
      const val = bytes[idx] ?? 0;
      const abs = addr + c;
      const changed = prevMemCache[abs] !== undefined && prevMemCache[abs] !== val;

      const bEl = document.createElement('span');
      bEl.className = 'mbyte pixel-border'
        + (abs === pc ? ' cur' : '')
        + (changed ? ' changed' : '')
        + (isHalted && abs === pc ? ' halt-byte' : '');
      bEl.textContent = val.toString(16).toUpperCase().padStart(2, '0');
      bEl.title = `${hex(abs, 4)} = ${val} (${val >= 32 && val < 127 ? String.fromCharCode(val) : 'non-printable'})`;
      bytesDiv.appendChild(bEl);

      const cEl = document.createElement('span');
      cEl.className = 'mchar';
      cEl.textContent = (val >= 32 && val < 127) ? String.fromCharCode(val) : '·';
      asciiDiv.appendChild(cEl);
    }

    const sep = document.createElement('div');
    sep.className = 'mem-vsep';

    rowEl.appendChild(bytesDiv);
    rowEl.appendChild(sep);
    rowEl.appendChild(asciiDiv);
    grid.appendChild(rowEl);
  }
}

function pushLog(addr, mnem, cycles, isLoad = false, isHalt = false) {
  const isMeta = mnem.startsWith('LOAD') || mnem.startsWith('RUN') || isHalt;
  if (!isMeta) stepCount++;
  $('sb-steps').textContent = String(stepCount);

  const log = $('exec-log');
  const empty = log.querySelector('.log-empty');
  if (empty) empty.remove();

  const entry = document.createElement('div');
  entry.className = 'log-entry'
    + (isLoad ? ' load-entry' : '')
    + (isHalt ? ' halt-entry' : '');
  const addrStr = addr !== null ? hex(addr, 4) : '----';
  const numStr = isMeta ? '···' : String(stepCount).padStart(3, '0');
  entry.innerHTML =
    `<span class="log-n">${numStr}</span>` +
    `<span class="log-addr">${addrStr}</span>` +
    `<span class="log-mn">${mnem}</span>` +
    (cycles !== null ? `<span class="log-cy">${cycles}cy</span>` : '');
  log.insertBefore(entry, log.firstChild);
  while (log.children.length > 80) log.removeChild(log.lastChild);
}

function parseHexInput(raw) {
  return raw.split(/[\s,]+/)
    .filter(s => s.length > 0)
    .map(s => parseInt(s.replace(/^0x/i, ''), 16))
    .filter(n => !isNaN(n) && n >= 0 && n <= 255);
}

function updateByteCount() {
  const raw = $('load-ta').value.trim();
  const bytes = parseHexInput(raw);
  const el = $('load-byte-count');
  const errEl = $('load-error');

  if (!raw) {
    el.textContent = '0 bytes';
    el.classList.remove('valid');
    errEl.classList.remove('show');
    return [];
  }

  const tokens = raw.split(/[\s,]+/).filter(s => s.length > 0);
  const invalid = tokens.filter(t => {
    const n = parseInt(t.replace(/^0x/i, ''), 16);
    return isNaN(n) || n < 0 || n > 255;
  });

  if (invalid.length) {
    el.textContent = `${bytes.length} bytes`;
    el.classList.remove('valid');
    errEl.textContent = `Invalid hex: ${invalid.slice(0, 3).join(', ')}`;
    errEl.classList.add('show');
    return bytes;
  }

  el.textContent = `${bytes.length} byte${bytes.length !== 1 ? 's' : ''}`;
  el.classList.toggle('valid', bytes.length > 0);
  errEl.classList.remove('show');
  return bytes;
}

function doStep() {
  if (!ws || ws.readyState !== 1 || halted) return;
  ws.send(JSON.stringify({ command: 'step' }));
}

function doRun() {
  if (!ws || ws.readyState !== 1 || halted) return;
  if (running) return;
  wasHalted = false;
  running = true;
  setCpuState('running');
  ws.send(JSON.stringify({ command: 'run', max_steps: 10000 }));
}

function updateRunButton() {
  const btn = $('btn-run');
  if (!btn) return;
  btn.querySelector('span').textContent = running ? 'RUNNING…' : 'RUN';
  const connected = ws && ws.readyState === 1;
  btn.disabled = running || halted || !connected;
}

function doReset() {
  if (!ws || ws.readyState !== 1) return;
  halted = false;
  wasHalted = false;
  running = false;
  stepCount = 0;
  prevState = null;
  prevMemCache = {};
  loadedRanges.clear();
  $('exec-log').innerHTML = '<div class="log-empty">Step or run a program to see execution history</div>';
  $('ci-mnem').textContent = '---';
  $('ci-oper').textContent = '';
  $('ci-mode').textContent = '';
  $('ci-bytes').innerHTML = '';
  $('disasm-strip').innerHTML = '';
  $('sb-steps').textContent = '0';
  setCpuState('idle');
  ws.send(JSON.stringify({ command: 'reset' }));
  showToast('CPU reset');
}

function clearLog() {
  stepCount = 0;
  $('sb-steps').textContent = '0';
  $('exec-log').innerHTML = '<div class="log-empty">Step or run a program to see execution history</div>';
}

function doLoad() {
  if (!ws || ws.readyState !== 1) return;
  const bytes = updateByteCount();
  if (!bytes.length) {
    $('load-error').textContent = 'Enter hex bytes to load (e.g. A9 05 AA)';
    $('load-error').classList.add('show');
    return;
  }
  doReset();
  setTimeout(() => {
    ws.send(JSON.stringify({ command: 'load', program: bytes, start_address: LOAD_ADDRESS }));
    $('load-ta').value = $('load-ta').value;
    updateByteCount();
  }, 120);
}

function jumpMemView() {
  const input = $('mem-jump-input');
  const raw = input.value.trim().replace(/^\$/, '');
  const addr = parseInt(raw, 16);
  if (isNaN(addr) || addr < 0 || addr > 0xFFFF) {
    showToast('Invalid address', true);
    return;
  }
  memViewStart = addr & 0xFFF0;
  fetchMem(prevState ? prevState.PC : LOAD_ADDRESS, halted);
  showToast(`Viewing ${hex(memViewStart, 4)}`);
}

function loadSample() {
  $('load-ta').value = SAMPLE_PROGRAM;
  $('load-ta').focus();
  updateByteCount();
}

function showToast(msg, isError = false) {
  const t = $('toast');
  t.textContent = msg;
  t.classList.toggle('error', isError);
  t.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => t.classList.remove('show'), 2800);
}

function initCircuitBg() {
  const svg = $('bg-circuit');
  if (!svg) return;
  const w = window.innerWidth;
  const h = window.innerHeight;
  svg.setAttribute('viewBox', `0 0 ${w} ${h}`);

  const nodes = [
    [w * 0.12, h * 0.25], [w * 0.88, h * 0.35], [w * 0.55, h * 0.82],
  ];
  const paths = [
    `M0,${h * 0.4} L${w * 0.3},${h * 0.4} L${w * 0.3},${h * 0.15} L${w * 0.7},${h * 0.15}`,
    `M${w},${h * 0.6} L${w * 0.65},${h * 0.6} L${w * 0.65},${h * 0.85} L${w * 0.2},${h * 0.85}`,
    `M${w * 0.5},0 L${w * 0.5},${h * 0.3} M${w * 0.5},${h * 0.7} L${w * 0.5},${h}`,
  ];

  svg.innerHTML = paths.map(d =>
    `<path d="${d}" stroke="rgba(0,54,123,0.1)" fill="none" stroke-width="1"/>`
  ).join('') + nodes.map(([cx, cy]) =>
    `<circle class="pulse-node" cx="${cx}" cy="${cy}" r="3"/>`
  ).join('');
}

function bindEvents() {
  document.querySelectorAll('[data-action]').forEach(btn => {
    btn.addEventListener('click', () => {
      const action = btn.dataset.action;
      if (action === 'step') doStep();
      else if (action === 'run') doRun();
      else if (action === 'reset') doReset();
      else if (action === 'load') doLoad();
    });
  });

  $('load-ta').addEventListener('input', updateByteCount);
  $('load-sample').addEventListener('click', loadSample);
  $('log-clear').addEventListener('click', clearLog);
  $('mem-jump-btn').addEventListener('click', jumpMemView);
  $('mem-jump-input').addEventListener('keydown', e => {
    if (e.key === 'Enter') jumpMemView();
  });

  document.addEventListener('keydown', e => {
    const tag = document.activeElement.tagName;
    if (tag === 'TEXTAREA' || tag === 'INPUT') return;
    if (e.code === 'Space' || e.code === 'KeyS') { e.preventDefault(); doStep(); }
    else if (e.code === 'KeyR' && !e.shiftKey) doReset();
    else if (e.code === 'KeyG') doRun();
    else if (e.code === 'KeyL') { $('load-ta').focus(); }
  });

  window.addEventListener('resize', initCircuitBg);
}

document.addEventListener('DOMContentLoaded', () => {
  initCircuitBg();
  bindEvents();
  updateByteCount();
  setCpuState('idle');
  connect();
});
