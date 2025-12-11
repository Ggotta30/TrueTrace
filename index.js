// index.js — TrueTrace v1 (anchoring + local ledger)
// Run with: node index.js

const express = require('express');
const fs = require('fs').promises;
const path = require('path');
const crypto = require('crypto');

const app = express();
app.use(express.json());

const LEDGER_PATH = path.join(__dirname, 'ledger.json');

// ---- Canonical JSON (stable deterministic ordering) ----
function canonicalize(obj) {
  if (Array.isArray(obj)) return `[${obj.map(canonicalize).join(',')}]`;
  if (obj && typeof obj === 'object') {
    const keys = Object.keys(obj).sort();
    return `{${keys.map(k => JSON.stringify(k) + ':' + canonicalize(obj[k])).join(',')}}`;
  }
  return JSON.stringify(obj);
}

// ---- Hash utility ----
function sha256hex(data) {
  return crypto.createHash('sha256').update(data).digest('hex');
}

// ---- Ensure ledger exists ----
async function ensureLedger() {
  try {
    await fs.access(LEDGER_PATH);
  } catch {
    await fs.writeFile(LEDGER_PATH, JSON.stringify([], null, 2), 'utf8');
  }
}

// ---- Append entry to ledger ----
async function appendToLedger(entry) {
  const raw = await fs.readFile(LEDGER_PATH, 'utf8');
  const arr = JSON.parse(raw || '[]');
  arr.push(entry);
  await fs.writeFile(LEDGER_PATH, JSON.stringify(arr, null, 2), 'utf8');
}

// -----------------------------------------------------------
// POST /anchor  — create signed anchoring event
// -----------------------------------------------------------
app.post('/anchor', async (req, res) => {
  try {
    const payload = req.body || {};

    if (!payload.source) {
      return res.status(400).json({ error: "Missing required field: source" });
    }

    // Load Ed25519 keys
    const privateKey = await fs.readFile(path.join(__dirname, "truetrace_ed25519"), "utf8");
    const publicKey = await fs.readFile(path.join(__dirname, "truetrace_ed25519.pub"), "utf8");

    const anchorId = crypto.randomUUID();
    const receivedAt = new Date().toISOString();

    const anchorObj = {
      anchor_id: anchorId,
      received_at: receivedAt,
      source: payload.source,
      data: payload.data ?? null
    };

    // Canonical form + hash
    const canonical = canonicalize(anchorObj);
    const bundleHash = sha256hex(canonical);

    // Digital signature (Ed25519)
    const signature = crypto.sign(null, Buffer.from(bundleHash), privateKey).toString("base64");

    // Ledger entry
    const ledgerEntry = {
      anchor_id: anchorId,
      received_at: receivedAt,
      source: payload.source,
      bundle_hash: bundleHash,
      canonical_blob: canonical,
      signature,
      public_key: publicKey
    };

    // Save to ledger
    await ensureLedger();
    await appendToLedger(ledgerEntry);

    return res.json({
      status: "ok",
      message: "Anchor created & signed",
      anchor: {
        anchor_id: anchorId,
        received_at: receivedAt,
        source: payload.source,
        bundle_hash: bundleHash,
        signature,
        public_key: publicKey,
        ledger_path: "/ledger"
      }
    });

  } catch (err) {
    console.error("Anchor error:", err);
    return res.status(500).json({ error: "internal_error", detail: err.message });
  }
});

// -----------------------------------------------------------
// GET /ledger — return the entire local ledger
// -----------------------------------------------------------
app.get('/ledger', async (req, res) => {
  try {
    await ensureLedger();
    const raw = await fs.readFile(LEDGER_PATH, 'utf8');
    const arr = JSON.parse(raw || '[]');
    res.json(arr);
  } catch (err) {
    console.error("Ledger error:", err);
    res.status(500).json({ error: "internal_error", detail: err.message });
  }
});

// -----------------------------------------------------------
// START SERVER
// -----------------------------------------------------------
const PORT = 3000;

app.listen(PORT, () => {
  console.log(`TrueTrace engine running on http://localhost:${PORT}`);
});
