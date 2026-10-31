# TradingAgents Cheatsheet

Quick commands and reminders for this fork.

## 1. One-time setup

```bash
cd /Users/genshi/Documents/_Self/ai-workspace/TradingAgents-fork
# .env already holds keys (FRED, TypeSafe/Jev, SEC EDGAR user agent)
```

For unattended (no terminal / cron / CI) runs, set these in `.env`:

```dotenv
TRADINGAGENTS_LLM_PROVIDER=openai
TRADINGAGENTS_QUICK_THINK_LLM=gpt-6-luna
TRADINGAGENTS_DEEP_THINK_LLM=gpt-6-sol
TRADINGAGENTS_OUTPUT_LANGUAGE=English
TRADINGAGENTS_MAX_DEBATE_ROUNDS=1
TRADINGAGENTS_MAX_RISK_ROUNDS=1
```

## 2. Normal analysis

```bash
# minimal, asks questions
tradingagents

# fully specified, no prompts
tradingagents \
  --ticker GOOGL \
  --date 2026-10-31 \
  --analysts market,sentiment,news,fundamentals \
  --save --no-show
```

All four analysts: `market`, `sentiment`, `news`, `fundamentals`.

## 3. Useful flags

| Flag | Meaning |
|---|---|
| `--ticker SYM` | Ticker (e.g. `GOOGL`, `0700.HK`, `BTC-USD`) |
| `--date YYYY-MM-DD` | Analysis date; today or earlier only |
| `--analysts a,b,c` | `market,sentiment,news,fundamentals` |
| `--save / --no-save` | Save report tree |
| `--show / --no-show` | Print full report at end |
| `--html / --no-html` | One-page `complete_report.html` |
| `--portfolio FILE` | Size against your real book |
| `--checkpoint / --no-checkpoint` | Crash-resume on/off |
| `--clear-checkpoints` | Delete all checkpoints first |

## 4. Portfolio file

See `portfolio.example.json`. Schema:

```json
{
  "cash": 25000.0,
  "currency": "USD",
  "positions": [
    { "ticker": "GOOGL", "quantity": 40, "average_price": 185.5 }
  ]
}
```

- `quantity` is signed: negative = short.
- `average_price` is optional (use `null`).
- `positions: []` means a flat book.
- Omit `--portfolio` entirely = agents have no portfolio context.

## 5. Checkpoint / resume

```bash
tradingagents ... --checkpoint          # save state after each node
tradingagents ... --clear-checkpoints   # wipe checkpoints, start fresh
```

- Stored at `~/.tradingagents/cache/checkpoints/<TICKER>.db`.
- Use the **same ticker + date + settings** to resume.
- Cleared automatically after a successful run.
- `--clear-checkpoints` does **not** enable checkpointing; it only deletes.

## 6. Backtest (score many runs)

```bash
tradingagents backtest NVDA,AAPL \
  --start 2026-06-01 \
  --end   2026-08-01 \
  --every 7 \
  --analysts market,news \
  --asset-type stock
```

Resume an interrupted sweep:

```bash
tradingagents backtest NVDA,AAPL --start 2026-06-01 --end 2026-08-01 \
  --every 7 --run-id <run_id_from_last_output>
```

Outputs:

- Log: `~/.tradingagents/logs/backtest/<run_id>/trading_memory.md`
- State JSON per cell: `<run_dir>/<TICKER>/TradingAgentsStrategy_logs/full_states_log_<date>.json`
- Printed summary: per-rating count, hit rate, mean alpha vs benchmark.

## 7. Where things are written

| What | Path |
|---|---|
| Reports | `~/.tradingagents/logs/<TICKER>/<DATE>/reports/` |
| HTML report | `.../reports/complete_report.html` |
| Message log | `~/.tradingagents/logs/<TICKER>/<DATE>/message_tool.log` |
| State JSON | `~/.tradingagents/logs/<TICKER>/TradingAgentsStrategy_logs/` |
| Memory log | `~/.tradingagents/memory/trading_memory.md` |
| Checkpoints | `~/.tradingagents/cache/checkpoints/` |
| Last-run prefs | `~/.tradingagents/cli_prefs.json` |

Override roots with `TRADINGAGENTS_RESULTS_DIR`, `TRADINGAGENTS_CACHE_DIR`,
`TRADINGAGENTS_MEMORY_LOG_PATH`.

## 8. Data sources (already configured here)

```bash
# check FRED works
curl -s "https://api.stlouisfed.org/fred/series?series_id=CPIAUCSL&api_key=$FRED_API_KEY&file_type=json" | head -c 200

# check SEC EDGAR works
curl -s -H "User-Agent: $SEC_EDGAR_USER_AGENT" https://www.sec.gov/files/company_tickers.json | head -c 200
```

- **FRED** → used by the **news** analyst.
- **Jev** → used by the **sentiment** analyst only.
- **SEC EDGAR** → used by the **fundamentals** analyst for statements.

## 9. Reminders / gotchas

- `--date` must be **today or earlier**; future dates are rejected.
- `fundamentals` is not available for `--asset-type crypto`.
- With no terminal, every missing answer is reported **before** any model call; add flags or env vars.
- `.env` is found from the **current working directory**; run from the repo or export vars.
- A run dated today uses the latest available data. A **past** date triggers point-in-time guards: prices are bounded, SEC EDGAR/FRED use the historical vintage, but live-only feeds (Yahoo news/social, present-day profiles) may be **unavailable** rather than fabricated.
- Weekend/holiday: "today" still works, but the latest close is the previous trading day.
- Backtest numbers are indicative, not reproducible; one model sample per cell.
- The memory log does **not** execute trades; it only records decisions and lessons.
- Use `tradingagents <command> --help` for exact options.
