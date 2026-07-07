# 🛒 BPI Grocery Challenge

A simple, **fully offline** web tool for running a live "grocery challenge" game at an
event. A contestant grabs items off a shelf against a fixed budget; the operator tracks
their picks on a laptop while the audience watches a big, carnival-styled screen reveal
the running total and the final verdict — **Within Budget!**, **Overbudget!**, or
**Underbudget!**

No internet, no database, no build step. Just Python and a browser.

---

## Quick start

**On Windows, just double-click `Start Grocery Challenge.bat`.**

Or, from a terminal in this folder:

```bash
python server.py
```

Either way, the **Control** panel opens automatically in your browser at
`http://localhost:8000/`. To put the game on the big screen:

1. In the Control panel, click **“Open View Screen ↗”** (top right).
2. Drag that new window onto your external display / projector / TV.
3. Press **F11** for full screen.

Press **Ctrl+C** in the terminal to stop the server.

> **Requirements:** Python 3.7 or newer. Nothing else to install.

---

## The two screens

| Screen | URL | Who sees it | What it's for |
|--------|-----|-------------|---------------|
| **Control** | `http://localhost:8000/` | The operator (backstage) | Add items, set the budget, run the reveal |
| **View** | `http://localhost:8000/view.html` | The audience (big screen) | Budget reveal, live total, and the final verdict |

The Control panel includes a **live mini-view** in the top-right corner that mirrors the
big screen exactly, so the operator always knows what the audience is seeing.

---

## Running an event (operator guide)

1. **Prepare the shelf.** Edit `itemlist.txt` so it matches the real items and prices on
   the shelf (see [Configuring the items](#configuring-the-items)). Refresh the Control
   page.
2. **Set the budget.** Type the amount in the **Budget** box (bottom-left), then click
   **Show ↗** to reveal it dramatically on the big screen.
3. **Track the picks.** As the contestant grabs items, use the **−  /  +** buttons (or type
   a number) next to each item. The **Cart Total** in the footer always shows the current
   total to *you*, whether or not the audience can see it.
4. **Decide what the audience sees while shopping** using the **Live Total** toggle:
   - **On** → the big screen shows the running total (and a budget progress bar) updating
     in real time. Great for suspense.
   - **Off** → the total stays hidden from the audience until the big reveal.
5. **The reveal.** When shopping is done, hit **🎉 Calculate!** The big screen shows
   **Your Cart**, counts up from ₱0 to the total, then slams in the verdict.
6. **Next contestant.** Click **Reset** to clear the cart and return the screen to the
   welcome splash. Your budget is kept, so you can run the next round immediately.

---

## Configuring the items

All items come from **`itemlist.txt`** — a plain text file anyone can edit. One item per
line, in this exact format:

```
Item Name: price, "image-file.png"
```

- **price** is in pesos, numbers only — no `₱` sign, no thousands commas (e.g. `1500`, not `₱1,500`).
- **image-file.png** is the picture for that item, kept in the `img/` folder.
- Lines starting with `#` are comments and are ignored.

Example:

```
Fish: 300, "fish.png"
Instant Noodles: 25, "instant noodles.png"
Diaper: 375, "diaper.png"
```

After editing, just **refresh the Control page** — the new list loads instantly.

---

## Adding item images

Put the image files named in `itemlist.txt` into the **`img/`** folder
(e.g. `img/fish.png`).

If an image is missing, the item automatically shows a **food emoji** as a friendly
placeholder (🐟 🍜 🥚 🍗 …), so the tool still looks good even before you've added any
pictures. Square images (roughly 1:1) look best.

---

## The verdict thresholds

When **Calculate!** is pressed, the total is compared to the budget:

| Result | Condition | Meaning |
|--------|-----------|---------|
| **UNDERBUDGET!** | total is **less than 50%** of budget | Played it safe — money to spare |
| **WITHIN BUDGET!** | total is between **50% and 100%** of budget | Right on the money 🎉 |
| **OVERBUDGET!** | total is **more than** the budget | Time to put something back 😅 |

---

## How it works

Both pages are served from the **same address** (`http://localhost:8000`). Browsers let
pages on the same origin share a small storage area called `localStorage`, and they notify
each other the instant it changes. So:

1. The Control panel writes the current game state to `localStorage`.
2. The View screen (and the mini-view) are notified immediately and re-draw themselves.

No network requests, no polling, no server round-trips for updates — which is exactly why
it works with the internet completely off. (This is also why we run a tiny server instead
of just double-clicking the HTML files: opening files directly via `file://` does **not**
reliably share storage between windows.)

---

## Project files

```
bpi-grocery/
├── Start Grocery Challenge.bat   # Double-click to start (Windows)
├── server.py        # The tiny local web server (run this)
├── index.html       # CONTROL — the operator's panel  ← default page
├── view.html        # VIEW — the big-screen display
├── itemlist.txt     # The item/price/image config (edit this)
├── img/             # Item images go here (fish.png, etc.)
├── README.md        # This file
├── control.html     # (Original tech demo — not used by the game)
└── display.html     # (Original tech demo — not used by the game)
```

The game is **`index.html` + `view.html`**. The original `control.html` / `display.html`
demo files are left in place for reference but aren't part of the live tool.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| **Browser didn't open automatically** | Open `http://localhost:8000/` manually. |
| **“Address already in use” on start** | Another program is on port 8000 (maybe an old server still running). Close it, or change `PORT` near the top of `server.py`. |
| **Items don't show / list is empty** | Check `itemlist.txt` formatting — each line must be `Name: price, "image.png"`. |
| **Item edits don't appear** | Refresh the Control page after editing `itemlist.txt`. |
| **The View screen isn't updating** | Make sure it was opened from the **“Open View Screen ↗”** button (so it's on the same `http://localhost:8000` address), not from a saved file. |
| **`python` not found** | Try `python3 server.py`, or install Python 3 from [python.org](https://www.python.org). |

---

## Notes

- **100% offline** — safe to run on an isolated event laptop with no Wi-Fi.
- Your working state (quantities, budget, toggle) is remembered, so an accidental refresh
  of the Control page won't lose the round in progress.
- Currency is Philippine Pesos (₱); prices with commas are formatted automatically on screen.
