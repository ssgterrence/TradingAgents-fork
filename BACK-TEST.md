A. 冒烟测试（先跑这个，确认流程和成本）
tradingagents backtest GOOGL \
 --start 2026-09-01 \
 --end 2026-10-15 \
 --every 14 \
 --analysts market,news
→ 约 4 个日期 × 1 ticker = 4 个 cell。便宜、快，用来确认输出格式。
B. 正式一点（2 个 ticker，约 3 个月）
tradingagents backtest GOOGL,NVDA \
 --start 2026-07-01 \
 --end 2026-10-15 \
 --every 7 \
 --analysts market,news
→ 约 15 个日期 × 2 ticker = 约 30 个 cell。这是比较合理的第一次正式评估。
C. 更完整（3 个 ticker，约 6 个月，成本明显更高）
tradingagents backtest GOOGL,NVDA,AAPL \
 --start 2026-04-01 \
 --end 2026-10-15 \
 --every 7 \
 --analysts market,sentiment,news,fundamentals
→ 约 28 个日期 × 3 ticker = 约 84 个 cell。适合你已经确认流程没问题、愿意承担成本时再跑。
常用附加参数
--asset-type crypto # BTC-USD、ETH-USD；注意 crypto 不允许 fundamentals
--portfolio my_book.json # 所有 cell 复用同一份持仓（不是在时间上滚动）
--run-id my_sweep_01 # 中断后续跑；同名会跳过已完成的 cell
续跑：
tradingagents backtest GOOGL,NVDA \
 --start 2026-07-01 --end 2026-10-15 --every 7 \
 --analysts market,news --run-id my_sweep_01
怎么读结果
运行结束会打印类似：
Resolved cells: 24 · pending: 6

- Buy: n=10, called the direction 60%, mean alpha +1.2% vs the benchmark
- Hold: n=8, no direction claimed, mean alpha +0.1% vs the benchmark
- Sell: n=6, called the direction 67%, mean alpha +0.8% vs the benchmark
  重点看：
- n 是否足够大：n < 10 基本没有统计意义；n ≥ 20–30 才开始有参考价值。
- 命中率：方向判断是否稳定高于 50%。
- mean alpha：是否稳定为正，以及是否只是某几个 cell 拉高的。
- pending：如果很多，说明 --end 太近，过几天用同 --run-id 再跑一次即可结算。
  成本/时间提醒
- 每个 cell = 一次完整分析。按你平时单次运行的耗时/费用 × cell 数估算。
- 正式跑之前，先用 A 方案（4 个 cell）验证。
- backtest 用的是独立 memory log，不会污染你的日常 trading_memory.md。
- 结果“指示性”而非可复现：每个 cell 只采样一次模型，新闻/社交源也没有归档。
  一句话建议：先用 GOOGL 单票 + 2026-09-01 ~ 2026-10-15 + --every 14 跑 4 个 cell 验证；确认没问题后，再用 GOOGL,NVDA + 2026-07-01 ~ 2026-10-15 + --every 7 做约 30 个 cell 的正式评估。

6. 读结果时的判断标准

- n ≥ 20 才值得看命中率；n < 10 基本是噪声。
- mean alpha 要稳定为正，而且不是被 1–2 个 cell 拉高的（去看 memory log 的逐条 alpha）。
- Buy 和 Sell 应该方向相反：如果两者都为正，说明评级没有区分度。
- Hold 没有方向，它的 alpha 只是参考。
- pending 多 = --end 太近，过几天用同 --run-id 再跑一次结算。
- 和 SPY 对照比：如果个股 alpha 不如“直接持有 SPY”，这套系统在这个区间就没有增加价值。

---

3. 选 ticker 的标准（按重要性排序）
1. 流动性与规模

- 大盘股：市值 > ~$10B，日均成交量 > ~500 万股。
- 避开微盘股/仙股：没有新闻、没有社交讨论、点差大，Agent 拿不到材料。

2. 数据覆盖要全

- 美股 SEC 申报主体 → EDGAR 能出报表。
- 新闻/社交覆盖度高（这直接决定 news/sentiment 分析师有没有料）。

3. 行业要分散

- 不要 3 个都是大型科技股（GOOGL+AAPL+MSFT+NVDA 相关性极高，等于只测了一个故事）。
- 跨 2–3 个行业，才能看出泛化。

4. 风格要有差异

- 高 beta 成长股 vs 防御股 vs 周期股。
- 这样能看出系统在“上涨市/下跌市/震荡市”里表现是否不同。

5. 先统一市场

- 第一轮全用美股，基准都是 SPY，alpha 可直接横向比较。
- 港股/日股/加密以后单独跑（加密还不允许 fundamentals）。

6. 避开回测区间内的重大公司事件

- 并购、分拆、退市、改名——这些会让基本面数据断裂。

7. 可以加一个指数 ETF 做对照

- SPY 本身不是“选股”，但能回答一个关键问题：系统是否比“直接持有指数”更好。
- 注意 ETF 的基本面路径和普通公司不同，情绪/新闻也更偏宏观。

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX 4. 具体推荐组合
❌ 你举的例子里，不太推荐的

- GOOGL + INTC：都偏科技/半导体，相关性高，多样性不足。可以做冒烟测试，不适合正式评估。
- GOOGL + AAPL：更相似，都是超大盘科技，信息增量很小。
  ✅ 推荐的几个组合
  组合 A — “核心三只，跨三行业”（最推荐起步）
  GOOGL 科技/通信服务
  JPM 金融
  XOM 能源
  组合 B — “风格差异最大”
  NVDA 高 beta 成长
  JNJ 防御医疗
  CAT 工业周期
  组合 C — “带市场对照”
  SPY 指数对照
  GOOGL 科技
  JPM 金融
  组合 D — “你熟悉 + 一个对照”（最省事）
  GOOGL 你已经在用的
  SPY 市场基准对照

---

必须用不同的 --run-id
否则两次结果会写进同一个 memory log，混在一起。

# 模型 A

TRADINGAGENTS_QUICK_THINK_LLM=gpt-6-luna \
TRADINGAGENTS_DEEP_THINK_LLM=gpt-6-sol \
tradingagents backtest GOOGL,WMT \
 --start 2026-07-01 --end 2026-10-15 --every 7 \
 --analysts market,news --run-id model_a

# 模型 B

TRADINGAGENTS_QUICK_THINK_LLM=<另一个模型> \
TRADINGAGENTS_DEEP_THINK_LLM=<另一个模型> \
tradingagents backtest GOOGL,WMT \
 --start 2026-07-01 --end 2026-10-15 --every 7 \
 --analysts market,news --run-id model_b

!!!重要警告：别把噪声当成模型差异

- 同一个模型重复跑，结果也会不同（LLM 采样非确定）。
- 单次 A/B 的差异可能只是噪声。
- 要让结论可信：
- n 尽量 ≥ 30 个 cell；
- 或者每个模型跑 2 次，看差异是否稳定；
- 比较时看平均 alpha 和命中率，不要只看某一个 ticker。
- 推理模型大多忽略 temperature，所以“调温度”对它们帮助不大。
  怎么比较
  把两次的汇总并排看：
  模型 A：Buy n=12, 命中 58%, mean alpha +0.9%
  模型 B：Buy n=12, 命中 67%, mean alpha +1.6%
  如果 B 在两个指标上都稳定更好，且 n 足够，才值得换。
