stocktwist MCP on Macos (opencode use opncode mcp)
三、怎么用

1. 登录一次
   tradingagents stocktwits-login
   会打印一个授权地址并尝试打开浏览器。登录/授权后，token 自动保存。
   远程服务器 / Docker / SSH：
   tradingagents stocktwits-login --manual
   浏览器跳转后会显示“无法连接”，把地址栏里的完整 URL 粘贴回终端即可。
   只打印地址、不自动开浏览器：
   tradingagents stocktwits-login --no-browser
2. 查看状态
   tradingagents stocktwits-status
3. 登出
   tradingagents stocktwits-logout
4. 正常跑分析
   tradingagents --ticker GOOGL --date 2026-10-31 \
    --analysts market,sentiment,news,fundamentals \
    --save --no-show
