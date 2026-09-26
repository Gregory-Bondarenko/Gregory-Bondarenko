"""Карточка в виде ячеек Jupyter с выводом DataFrame для профиля GitHub."""
from html import escape

W = 820
PAD = 16
GUTTER = 58                  # колонка с номерами ячеек
X0 = PAD + GUTTER             # левый край содержимого ячейки
CW = W - X0 - PAD             # ширина содержимого

BG, STROKE = "#161b22", "#2a3038"
CODE_BG, CODE_STROKE = "#0d1117", "#30363d"
C_TEXT, C_DIM, C_HEAD = "#c9d1d9", "#8b949e", "#e6edf3"
ROW_ALT = "#1b2029"
SYN = {"kw": "#ff7b72", "str": "#a5d6ff", "fn": "#d2a8ff", "attr": "#79c0ff", "p": "#c9d1d9"}

MONO = "ui-monospace,'SFMono-Regular','JetBrains Mono','DejaVu Sans Mono',Consolas,monospace"
SANS = "-apple-system,'Segoe UI','Helvetica Neue','DejaVu Sans',Arial,sans-serif"

VAR = "Gregory_Bondarenko_CV"

CELLS = [
    {
        "code": [
            [("import", "kw"), (" json", "p")],
            [("import", "kw"), (" pandas ", "p"), ("as", "kw"), (" pd", "p")],
            [],
            [(VAR, "p"), (" = json.", "p"), ("load", "fn"), ("(", "p"), ("open", "fn"), ("(", "p"),
             ('"cv.json"', "str"), (", encoding=", "p"), ('"utf-8"', "str"), ("))", "p")],
            [],
            [("(pd.", "p"), ("json_normalize", "fn"), ("(", "p"), (VAR, "p"), ("[", "p"), ('"Общее"', "str"), ("]).T", "p")],
            [("    .", "p"), ("sort_index", "fn"), ("(key=", "p"), ("lambda", "kw"), (" i: ~i.str.", "p"), ("contains", "fn"),
             ("(", "p"), ('"."', "str"), (", regex=", "p"), ("False", "kw"), ("), kind=", "p"), ('"stable"', "str"), (")", "p")],
            [("    .", "p"), ("set_axis", "fn"), ("([", "p"), ('"Значение"', "str"), ("], axis=", "p"), ("1", "kw"), (")", "p")],
            [("    .", "p"), ("rename_axis", "fn"), ("(", "p"), ('"Ключ"', "str"), ("))", "p")],
        ],
        "idx": 1,
        "cols": [("", 214), ("Значение", 0)],
        "head2": ["Ключ", ""],
        # вложенные ключи json_normalize ставит в конец, sort_index поднимает их наверх
        "rows": [
            ["Образование.Бакалавриат", "РАНХиГС'27"],
            ["Образование.Магистратура", "-"],
            ["Профиль", "Анализ данных, Продуктовая аналитика, Data Science"],
            ["Страна", "Россия"],
            ["Город", "Москва"],
            ["Языки", "Русский, Английский (B1-B2), Турецкий (A1)"],
        ],
    },
    {
        "code": [
            [("(pd.", "p"), ("DataFrame", "fn"), ("(", "p"), (VAR, "p"), ("[", "p"), ('"Опыт"', "str"), ("])", "p")],
            [("    .", "p"), ("set_index", "fn"), ("([", "p"), ('"Тип"', "str"), (", ", "p"), ('"Год"', "str"), ("]))", "p")],
        ],
        "idx": 2,
        "groups": True,
        "cols": [("", 118), ("", 60), ("Описание", 0)],
        "head2": ["Тип", "Год", ""],
        "rows": [
            ["Работа", "2026", "МТС Web Services, аналитик данных в команде ML DSP"],
            ["", "2025", "Tomoru, аналитик в стартапе по разработке NLP-моделей"],
            ["Школы", "2026", "Кейс-Лаб ИТ КоР, Росатом"],
            ["", "2025", "Школа аналитики DWH, IT-холдинг Т1"],
            ["Хакатоны", "2026", "Финалист Changellenge Cup IT"],
        ],
    },
]

# ---------------------------------------------------------------------------
# тайминги и параметры анимации
T0, RUN, ROW_STEP, GAP = 0.5, 0.7, 0.11, 0.4
SHIFT = 0.45                 # плавный сдвиг ячеек вниз, когда появляется вывод
CHAR_W = 13 * 0.602
LINE_H, ROW_H, HEAD_H, HEAD2_H = 20, 23, 24, 18
CAP = 7                      # высота скруглённых «шапок» поля ввода
OUT_GAP, CELL_GAP = 10, 18

import random
rnd = random.Random(7)       # фиксированное зерно: карточка одинаковая при каждой сборке


def keystrokes(code):
    """Моменты нажатий с неровным темпом и паузами после точек и скобок."""
    times, t = [], 0.0
    for ch in code:
        t += rnd.uniform(0.022, 0.05)
        if ch in ".([":
            t += rnd.uniform(0.06, 0.12)
        times.append(t)
    return times


# ---------- проход 1: раскладка в финальном состоянии и таймлайн ----------
cells, events = [], []       # events: (источник, начало, длительность, сдвиг в px)
y, t = PAD + 4, T0
for n, cell in enumerate(CELLS, start=1):
    c = {"n": n, "cell": cell, "y": y, "lines": []}
    nl = len(cell["code"])
    c["box_h"] = nl * LINE_H + 14
    t_line = t
    for li, toks in enumerate(cell["code"]):
        if li > 0:           # Enter: поле ввода растёт на строку
            events.append((("box", n), t_line, 0.0, LINE_H))
        text = "".join(ch for ch, _ in toks)
        if not text:
            t_line += 0.25
            continue
        ks = keystrokes(text)
        dur = ks[-1] + 0.05
        last = li == nl - 1
        hide_at = t_line + dur + (0.35 if last else 0.12)
        c["lines"].append({"li": li, "toks": toks, "text": text, "ks": ks, "dur": dur, "t0": t_line, "hide": hide_at})
        t_line = hide_at + (0 if last else 0.1)
    c["t_run"] = t_line
    t = t_line + RUN
    c["t_out"] = t
    out_h = OUT_GAP + HEAD_H + len(cell["rows"]) * ROW_H
    c["out_h"] = out_h
    events.append((("out", n), t, SHIFT, out_h))
    t += (len(cell["rows"]) + 1) * ROW_STEP + GAP
    y += c["box_h"] + out_h + CELL_GAP
    cells.append(c)

H = int(y - CELL_GAP + PAD + 6)
TOTAL = t + 1.0


def pct(x):
    return f"{min(max(x, 0), TOTAL) / TOTAL * 100:.3f}%"


def offset_at(time, deps):
    """Насколько элемент ещё выше своего финального места в момент time."""
    off = 0.0
    for src, st, du, d in events:
        if src not in deps:
            continue
        if du == 0:
            done = 1.0 if time >= st else 0.0
        else:
            x = min(max((time - st) / du, 0), 1)
            done = 1 - (1 - x) ** 3      # ease-out
        off += d * (1 - done)
    return off


def shift_anim(name, deps):
    """Ключевые кадры translateY для группы, зависящей от роста источников deps."""
    pts = {0.0, TOTAL}
    for src, st, du, _ in events:
        if src in deps:
            if du == 0:
                pts |= {st - 0.001, st}
            else:
                pts |= {st + du * k / 8 for k in range(9)}
    frames = "".join(f"{pct(p)}{{transform:translateY({-offset_at(p, deps):.2f}px)}}" for p in sorted(pts))
    css.append(f"@keyframes {name}{{{frames}}}")
    return f'style="animation:{name} {TOTAL:.2f}s linear both"'


# ---------- проход 2: вывод SVG ----------
css = [
    f".m{{font-family:{MONO};font-size:13px;white-space:pre}}",
    f".s{{font-family:{SANS};font-size:12px}}",
    ".h{font-weight:600}",
    ".o{opacity:0;animation:show .55s cubic-bezier(.2,.7,.2,1) forwards}",
    ".x{animation:hide .01s linear forwards}",
    "@keyframes show{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:none}}@keyframes hide{to{opacity:0}}",
]
out = []
px = PAD + GUTTER - 10
tx = X0 + 12
above = set()                # источники роста выше текущей ячейки
for c in cells:
    n, cell, cy, box_h = c["n"], c["cell"], c["y"], c["box_h"]
    nl = len(cell["code"])
    own = {("box", n)}

    # --- ввод: номер, поле, код; всё сдвигается ростом ячеек выше ---
    out.append(f'<g {shift_anim(f"sh{n}i", set(above))}>')
    first_base = cy + 7 + LINE_H - 5.5
    # поле ввода из трёх частей: верхняя шапка, растущая середина, нижняя шапка
    out.append(f'<clipPath id="tc{n}"><rect x="{X0 - 2}" y="{cy - 2}" width="{CW + 4}" height="{CAP + 2}"/></clipPath>')
    out.append(f'<rect x="{X0}" y="{cy}" width="{CW}" height="{2 * CAP + 2}" rx="4" fill="{CODE_BG}" stroke="{CODE_STROKE}" clip-path="url(#tc{n})"/>')
    mid_h = box_h - 2 * CAP
    one_h = LINE_H + 14 - 2 * CAP
    steps_mid = []
    for L in range(1, nl + 1):
        steps_mid.append(((L * LINE_H + 14 - 2 * CAP) / mid_h))
    # масштаб середины по времени Enter
    enters = [st for src, st, du, d in events if src == ("box", n)]
    kf = [f"0%{{transform:scaleY({steps_mid[0]:.4f})}}"]
    for k, st in enumerate(enters, start=1):
        kf.append(f"{pct(st - 0.001)}{{transform:scaleY({steps_mid[k - 1]:.4f})}}{pct(st)}{{transform:scaleY({steps_mid[k]:.4f})}}")
    kf.append("100%{transform:scaleY(1)}")
    css.append(f"@keyframes gm{n}{{{''.join(kf)}}}")
    out.append(f'<g style="transform-box:fill-box;transform-origin:0 0;animation:gm{n} {TOTAL:.2f}s linear both">'
               f'<rect x="{X0}" y="{cy + CAP}" width="{CW}" height="{mid_h}" fill="{CODE_BG}"/>'
               f'<line x1="{X0 + .5}" y1="{cy + CAP}" x2="{X0 + .5}" y2="{cy + CAP + mid_h}" stroke="{CODE_STROKE}" vector-effect="non-scaling-stroke"/>'
               f'<line x1="{X0 + CW - .5}" y1="{cy + CAP}" x2="{X0 + CW - .5}" y2="{cy + CAP + mid_h}" stroke="{CODE_STROKE}" vector-effect="non-scaling-stroke"/></g>')
    # нижняя шапка едет вниз вместе с ростом
    out.append(f'<g {shift_anim(f"bc{n}", own)}>'
               f'<clipPath id="bcc{n}"><rect x="{X0 - 2}" y="{cy + box_h - CAP}" width="{CW + 4}" height="{CAP + 2}"/></clipPath>'
               f'<rect x="{X0}" y="{cy + box_h - 2 * CAP - 2}" width="{CW}" height="{2 * CAP + 2}" rx="4" fill="{CODE_BG}" stroke="{CODE_STROKE}" clip-path="url(#bcc{n})"/></g>')
    # номер ячейки: [ ] → [*] → [n]
    tr = c["t_run"]
    out.append(f'<text class="m x" style="animation-delay:{tr:.2f}s" x="{px}" y="{first_base}" fill="{C_DIM}" text-anchor="end">[ ]:</text>')
    out.append(f'<text class="m o" style="animation:show .01s {tr:.2f}s forwards,hide .01s {tr + RUN:.2f}s forwards" x="{px}" y="{first_base}" fill="{C_DIM}" text-anchor="end">[*]:</text>')
    out.append(f'<text class="m o" style="animation-delay:{tr + RUN:.2f}s" x="{px}" y="{first_base}" fill="{C_DIM}" text-anchor="end">[{n}]:</text>')
    # строки кода с печатью и кареткой
    for ln in c["lines"]:
        li, ks, dur, t0 = ln["li"], ln["ks"], ln["dur"], ln["t0"]
        base = first_base + li * LINE_H
        nch = len(ln["text"])
        lw = nch * CHAR_W
        lid = f"c{n}l{li}"
        clip_kf = ["0%{transform:scaleX(0)}"] + [f"{k / dur * 100:.2f}%{{transform:scaleX({(i + 1) / nch:.4f})}}" for i, k in enumerate(ks)] + ["100%{transform:scaleX(1)}"]
        car_kf = ["0%{transform:translateX(0)}"] + [f"{k / dur * 100:.2f}%{{transform:translateX({(i + 1) * CHAR_W:.2f}px)}}" for i, k in enumerate(ks)] + [f"100%{{transform:translateX({lw:.2f}px)}}"]
        css.append(f"@keyframes ty{lid}{{{''.join(clip_kf)}}}@keyframes mv{lid}{{{''.join(car_kf)}}}")
        out.append(f'<clipPath id="{lid}"><rect x="{tx}" y="{base - 15}" width="{lw:.2f}" height="{LINE_H}" '
                   f'style="transform-box:fill-box;transform-origin:left;animation:ty{lid} {dur:.2f}s steps(1,end) {t0:.2f}s both"/></clipPath>')
        spans = "".join(f'<tspan fill="{SYN[k]}">{escape(ch)}</tspan>' for ch, k in ln["toks"])
        # textLength фиксирует ширину строки, чтобы каретка не уезжала при другом шрифте
        out.append(f'<text class="m" x="{tx}" y="{base}" textLength="{lw:.2f}" lengthAdjust="spacing" clip-path="url(#{lid})">{spans}</text>')
        out.append(f'<g style="opacity:0;animation:show .01s {t0:.2f}s forwards,hide .01s {ln["hide"]:.2f}s forwards">'
                   f'<rect x="{tx}" y="{base - 13}" width="1.6" height="17" fill="{C_TEXT}" '
                   f'style="animation:mv{lid} {dur:.2f}s steps(1,end) {t0:.2f}s both"/></g>')
    out.append("</g>")

    # --- вывод: таблица; сдвигается ростом ячеек выше и своего поля ввода ---
    out.append(f'<g {shift_anim(f"sh{n}o", set(above) | own)}>')
    tt = c["t_out"]
    yy = cy + box_h + OUT_GAP
    xs, x = [], X0 + 4
    for _, w in cell["cols"]:
        xs.append(x)
        x += w
    g = [f'<g class="o" style="animation-delay:{tt:.2f}s">']
    for (name, _), cx in zip(cell["cols"], xs):
        g.append(f'<text class="s h" x="{cx + 6}" y="{yy + 17}" fill="{C_HEAD}">{escape(name)}</text>')
    hh = HEAD_H
    if cell.get("head2"):
        # имена уровней индекса в той же строке, что и названия колонок
        for name, cx in zip(cell["head2"], xs):
            if name:
                g.append(f'<text class="s h" x="{cx + 6}" y="{yy + 17}" fill="{C_HEAD}">{escape(name)}</text>')
    g.append(f'<line x1="{X0 + 4}" y1="{yy + hh}" x2="{X0 + CW}" y2="{yy + hh}" stroke="{CODE_STROKE}"/></g>')
    out += g
    yy += hh
    for r, row in enumerate(cell["rows"]):
        g = [f'<g class="o" style="animation-delay:{tt + (r + 1) * ROW_STEP:.2f}s">']
        if cell.get("groups"):
            if r > 0 and row[0]:
                g.append(f'<line x1="{X0 + 4}" y1="{yy}" x2="{X0 + CW}" y2="{yy}" stroke="{CODE_STROKE}"/>')
        elif r % 2 == 1:
            g.append(f'<rect x="{X0 + 4}" y="{yy}" width="{CW - 4}" height="{ROW_H}" fill="{ROW_ALT}"/>')
        for k, (val, cx) in enumerate(zip(row, xs)):
            is_idx = k < cell.get("idx", 1)
            g.append(f'<text class="{"s h" if is_idx else "s"}" x="{cx + 6}" y="{yy + 15.5}" fill="{C_DIM if is_idx else C_TEXT}">{escape(val)}</text>')
        g.append("</g>")
        out += g
        yy += ROW_H
    out.append("</g>")
    above |= own | {("out", n)}


GROW_CARD = False            # True: внешняя карточка растёт вместе с содержимым


def card():
    """Внешняя карточка: статичная или растущая вместе с содержимым."""
    if not GROW_CARD:
        return [f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="14" fill="{BG}" stroke="{STROKE}"/>']
    allsrc = {src for src, *_ in events}
    R = 14
    mid = H - 2 * R
    pts = {0.0, TOTAL}
    for src, st, du, _ in events:
        pts |= {st - 0.001, st} if du == 0 else {st + du * k / 8 for k in range(9)}
    kf = "".join(f"{pct(p)}{{transform:scaleY({(mid - offset_at(p, allsrc)) / mid:.5f})}}" for p in sorted(pts))
    css.append(f"@keyframes cardm{{{kf}}}")
    return [
        f'<clipPath id="cardt"><rect x="-1" y="-1" width="{W + 2}" height="{R + 1}"/></clipPath>',
        f'<rect x="0.5" y="0.5" width="{W - 1}" height="{2 * R + 2}" rx="{R}" fill="{BG}" stroke="{STROKE}" clip-path="url(#cardt)"/>',
        f'<g style="transform-box:fill-box;transform-origin:0 0;animation:cardm {TOTAL:.2f}s linear both">'
        f'<rect x="0.5" y="{R}" width="{W - 1}" height="{mid}" fill="{BG}"/>'
        f'<line x1="0.5" y1="{R}" x2="0.5" y2="{R + mid}" stroke="{STROKE}" vector-effect="non-scaling-stroke"/>'
        f'<line x1="{W - .5}" y1="{R}" x2="{W - .5}" y2="{R + mid}" stroke="{STROKE}" vector-effect="non-scaling-stroke"/></g>',
        f'<g {shift_anim("cardb", allsrc)}><clipPath id="cardbc"><rect x="-1" y="{H - R}" width="{W + 2}" height="{R + 1}"/></clipPath>'
        f'<rect x="0.5" y="{H - 2 * R - 2}" width="{W - 1}" height="{2 * R + 1.5}" rx="{R}" fill="{BG}" stroke="{STROKE}" clip-path="url(#cardbc)"/></g>',
    ]

card_parts = card()
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Общая информация, работа и достижения">',
       f"<style>{''.join(css)}</style>",
       *card_parts, *out, "</svg>"]
open("notebook.svg", "w", encoding="utf-8").write("\n".join(svg))
print("notebook.svg", W, "x", H, "анимация", round(TOTAL, 1), "с")
