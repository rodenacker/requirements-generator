#!/usr/bin/env node
// Two-origin fixture for /design-system step-04 §4.A.3 (CORS fallback).
// :8701 serves the page; :8702 serves its stylesheet with no CORS headers, so
// the page's `document.styleSheets[n].cssRules` throws and step-04 records the
// sheet as corsBlocked. /old/brand.css 301-redirects to /brand.css.
// Run: node framework/tools/__fixtures__/cors-css/serve.cjs  (Ctrl+C to stop)
'use strict';
const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');

const file = (name) => fs.readFileSync(path.join(__dirname, name));

http.createServer((req, res) => {
  if (req.url !== '/' && req.url !== '/index.html') { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
  res.end(file('index.html'));
}).listen(8701, () => console.log('page   http://localhost:8701/'));

http.createServer((req, res) => {
  if (req.url === '/old/brand.css') { res.writeHead(301, { Location: '/brand.css' }); return res.end(); }
  if (req.url !== '/brand.css') { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'Content-Type': 'text/css; charset=utf-8' });
  res.end(file('brand.css'));
}).listen(8702, () => console.log('sheets http://localhost:8702/brand.css'));
