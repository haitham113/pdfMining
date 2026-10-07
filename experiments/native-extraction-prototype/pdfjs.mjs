// THROWAWAY: inspect PDF.js text items and visible-page transforms.
import fs from 'node:fs';
import path from 'node:path';
import { getDocument, version } from 'pdfjs-dist/legacy/build/pdf.mjs';

const root = path.resolve(import.meta.dirname, '../..');
const manifest = JSON.parse(fs.readFileSync(path.join(root, 'docs/evaluation/stage-05-corpus-manifest.json'), 'utf8'));
const rows = [];
for (const fixture of manifest.entries) {
  const file = path.join(root, fixture.file);
  const started = performance.now();
  const task = getDocument({ data: new Uint8Array(fs.readFileSync(file)), useSystemFonts: true });
  const doc = await task.promise;
  const pages = [];
  for (let number = 1; number <= doc.numPages; number++) {
    const page = await doc.getPage(number);
    const viewport = page.getViewport({ scale: 1 });
    const content = await page.getTextContent();
    pages.push({
      page: number,
      width: viewport.width,
      height: viewport.height,
      view: page.view,
      rotation: page.rotate,
      text: content.items.map(item => item.str).join(' '),
      items: content.items.filter(item => item.str).length,
      samples: content.items.filter(item => /97\.2|٢٣|٣٢|٢٠٢٥|٥٢٠٢|99 percent|71 percent/.test(item.str)).map(item => ({text: item.str, transform: item.transform, dir: item.dir})).slice(0, 12),
    });
  }
  rows.push({id: fixture.id, milliseconds: +(performance.now() - started).toFixed(2), pages});
  await task.destroy();
}
console.log(JSON.stringify({version, fixtures: rows}, null, 2));
