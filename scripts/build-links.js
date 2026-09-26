// Кнопки-ссылки для шапки профиля в стиле плиток стека
const si = require('simple-icons');
const fs = require('fs');

const H = 52, R = 14, PAD = 14, ICON = 22, GAP_ICON = 12;
const BG = '#161b22', STROKE = '#2a3038', TITLE = '#e6edf3', SUB = '#8b949e';
const SANS = "-apple-system,'Segoe UI','Helvetica Neue','DejaVu Sans',Arial,sans-serif";
const MONO = "ui-monospace,'SFMono-Regular','JetBrains Mono','DejaVu Sans Mono',Consolas,monospace";

// нейтральные значки для сайта и почты (не бренды), телеграм из simple-icons
const GLOBE = '<g fill="none" stroke="#58a6ff" stroke-width="1.8"><circle cx="12" cy="12" r="9.5"/><ellipse cx="12" cy="12" rx="4.2" ry="9.5"/><path d="M2.5 12h19M4 7h16M4 17h16"/></g>';
const MAIL = '<g fill="none" stroke="#f0883e" stroke-width="1.8" stroke-linejoin="round"><rect x="2.5" y="5" width="19" height="14" rx="2.5"/><path d="M3 6.5l9 6.5 9-6.5"/></g>';
const TG = `<path d="${si.siTelegram.path}" fill="#${si.siTelegram.hex}"/>`;

const LINKS = [
  { file: 'site', icon: GLOBE, title: 'Сайт-визитка', sub: 'gregory-bondarenko.ru' },
  { file: 'telegram', icon: TG, title: 'Telegram', sub: '@Bondarenko_Gregory' },
  { file: 'channel', icon: TG, title: 'ТГ-канал', sub: '@logovo_data' },
  { file: 'mail', icon: MAIL, title: 'Почта', sub: 'grisha.bondarenko76@gmail.com' },
];

fs.mkdirSync('assets/links', { recursive: true });
for (const l of LINKS) {
  // ширина по самой длинной строке: подпись моноширинная 11 px, заголовок 13.5 px
  const textW = Math.max(l.sub.length * 11 * 0.61, l.title.length * 13.5 * 0.6);
  const W = Math.ceil(PAD + ICON + GAP_ICON + textW + PAD + 4);
  const tx = PAD + ICON + GAP_ICON;
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="${l.title}: ${l.sub}">
<title>${l.title}: ${l.sub}</title>
<rect x="0.5" y="0.5" width="${W - 1}" height="${H - 1}" rx="${R}" fill="${BG}" stroke="${STROKE}"/>
<g transform="translate(${PAD} ${(H - ICON) / 2}) scale(${ICON / 24})">${l.icon}</g>
<text x="${tx}" y="22" fill="${TITLE}" font-family="${SANS}" font-size="13.5" font-weight="600">${l.title}</text>
<text x="${tx}" y="39" fill="${SUB}" font-family="${MONO}" font-size="11">${l.sub}</text>
</svg>
`;
  fs.writeFileSync(`assets/links/${l.file}.svg`, svg);
  console.log(`assets/links/${l.file}.svg`, W + 'x' + H);
}
