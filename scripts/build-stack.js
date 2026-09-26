const si = require('simple-icons');
const fs = require('fs');

const TILE = 100, ICON = 40, GAP = 12, RADIUS = 16, LABEL_GAP = 28, ROW_GAP = 24;
const TILE_BG = '#161b22', TILE_STROKE = '#2a3038';
const GROUP_COLOR = '#8b949e', NAME_COLOR = '#c9d1d9';
const MONO = "'Fira Code','DejaVu Sans Mono',monospace";

// группы плиток: slug из simple-icons либо собственная текстовая плитка {t, hex, name}
const GROUPS = [
  {
    title: 'PYTHON И ML',
    items: [
      { i: 'jupyter', name: 'Jupyter' }, { i: 'python' }, { i: 'pandas' }, { i: 'numpy' },
      { i: 'scikitlearn', name: 'sklearn' },
      { t: 'CB', title: 'CatBoost', hex: 'FFCC00' },
    ],
  },
  {
    title: 'ВИЗУАЛИЗАЦИЯ И BI',
    items: [
      { t: 'MPL', title: 'Matplotlib', hex: '4C8EBF' },
      { t: 'SNS', title: 'Seaborn', hex: '6E9BD2' },
      { i: 'plotly' },
      { t: 'PBI', title: 'Power BI', hex: 'F2C811' },
      { i: 'apachesuperset', name: 'Superset' },
    ],
  },
  {
    title: 'ДАННЫЕ И ХРАНИЛИЩА',
    items: [
      { i: 'postgresql', name: 'Postgres' },
      { i: 'clickhouse', name: 'ClickHouse' },
      { i: 'apachespark', name: 'PySpark' },
      { i: 'apachehadoop', name: 'Hadoop' },
    ],
  },
  {
    title: 'ДРУГОЕ',
    items: [
      { i: 'git' },
      { t: 'A/B', title: 'A/B-тесты', hex: '58A6FF' },
      { i: 'googlesheets', name: 'Sheets' },
      { t: 'XLS', title: 'Excel', hex: '3FA96B' },
    ],
  },
];

// тёмные логотипы осветляем, чтобы не пропадали на тёмном фоне
function lift(hex) {
  const n = parseInt(hex, 16);
  const [r, g, b] = [(n >> 16) & 255, (n >> 8) & 255, n & 255];
  const lum = 0.2126 * r + 0.7152 * g + 0.0722 * b;
  if (lum >= 70) return '#' + hex;
  const k = 70 / Math.max(lum, 1);
  const cl = v => Math.min(255, Math.round(v * k + 40));
  return `rgb(${cl(r)},${cl(g)},${cl(b)})`;
}

function tile(item, x, y) {
  const icon = item.i ? si['si' + item.i.charAt(0).toUpperCase() + item.i.slice(1)] : null;
  if (item.i && !icon) throw new Error('нет иконки: ' + item.i);
  const name = item.name || (icon ? icon.title : item.title);
  const fill = icon ? lift(icon.hex) : lift(item.hex);

  const parts = [
    `<title>${name}</title>`,
    `<rect x="${x}" y="${y}" width="${TILE}" height="${TILE}" rx="${RADIUS}" fill="${TILE_BG}" stroke="${TILE_STROKE}" stroke-width="1"/>`,
  ];
  const cx = x + TILE / 2, iconTop = y + 20;
  if (icon) {
    const s = ICON / 24;
    parts.push(`<g transform="translate(${cx - ICON / 2} ${iconTop}) scale(${s})"><path d="${icon.path}" fill="${fill}"/></g>`);
  } else {
    parts.push(`<text x="${cx}" y="${iconTop + ICON / 2}" fill="${fill}" font-family="${MONO}" font-size="19" font-weight="700" text-anchor="middle" dominant-baseline="central">${item.t}</text>`);
  }
  parts.push(`<text x="${cx}" y="${y + TILE - 17}" fill="${NAME_COLOR}" font-family="${MONO}" font-size="12" text-anchor="middle" dominant-baseline="central">${name}</text>`);
  return `<g>${parts.join('')}</g>`;
}

const cols = Math.max(...GROUPS.map(g => g.items.length));
const w = cols * TILE + (cols - 1) * GAP;
const h = GROUPS.length * (LABEL_GAP + TILE) + (GROUPS.length - 1) * ROW_GAP;

let y = 0;
const body = GROUPS.map(g => {
  const label = `<text x="2" y="${y + 13}" fill="${GROUP_COLOR}" font-family="${MONO}" font-size="12.5" font-weight="600" letter-spacing="1.4">${g.title}</text>`;
  const tiles = g.items.map((item, c) => tile(item, c * (TILE + GAP), y + LABEL_GAP)).join('');
  y += LABEL_GAP + TILE + ROW_GAP;
  return label + tiles;
}).join('\n');

fs.writeFileSync('stack.svg', `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" role="img" aria-label="Стек">\n${body}\n</svg>\n`);
console.log('stack.svg', w + 'x' + h);
