# Graph Report - TradingAgents-fork  (2026-10-25)

## Corpus Check
- 197 files · ~126,860 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 8 file(s) not represented in the graph (top: (none) 5, .example 2, .lock 1)

## Summary
- 3594 nodes · 8315 edges · 155 communities (124 shown, 31 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 464 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `9aaf1462`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_dataflows_config.py
- test_ohlcv_latest_bar.py
- test_cli_updates.py
- test_yfinance_stale_ohlcv_guard.py
- test_sec_edgar.py
- test_news_lookahead.py
- get_instrument_context_from_state
- test_cli_symbol_handling.py
- test_alpha_vantage_hardening.py
- get_capabilities
- router.py
- unit
- TradingMemoryLog
- TestDeferredReflection
- test_chatgpt_provider.py
- test_backtest.py
- test_cli_headless.py
- make_log
- fetch_returns
- test_cli_commands.py
- prompts.py
- stocktwits.py
- ohlcv.py
- test_portfolio_context.py
- requests
- test_cli_memory_log.py
- sec_edgar.py
- get_macro_data
- test_reddit_fallback.py
- test
- reddit.py
- test_yahoo_rate_limit.py
- GoogleClient
- OpenAIClient
- chatgpt_auth.py
- TradingAgentsGraph
- NoMarketDataError
- test_rating_integrity.py
- test_ollama_base_url.py
- ResearchPlan
- VendorUnavailableError
- TraderProposal
- fetch_reddit_posts
- BaseLLMClient
- build
- create_sentiment_analyst
- openai_client.py
- test_cli_prefs.py
- Propagator
- normalize_symbol
- _make_api_request
- test_api_key_env.py
- create_llm_client
- test_env_overrides.py
- Settlement
- tradingagents-ollama
- test_chatgpt_auth.py
- ConditionalLogic
- test_statement_knowledge_time.py
- test_tool_date_enforcement.py
- run_analysis
- re
- safe_ticker_component
- test_fundamentals_lookahead.py
- build_llm_kwargs
- VendorRoutingTests
- AnthropicClient
- resolve_instrument_identity
- TradingAgents: Multi-Agents LLM Financial Trading Framework
- test_post_screen.py
- test_provider_registry.py
- StatsCallbackHandler
- unit
- test_memory_log.py
- test_llm_max_retries.py
- settle_pending
- test_model_validation.py
- _price_df
- test_google_thinking_level.py
- conftest.py
- RouterHandlesBaseTypesTests
- analyze
- stocktwits.py
- _graph
- updates.py
- test_structured_agent_prompts.py
- ohlcv.py
- attributes
- attributes
- AzureOpenAIClient
- test_suite_isolation.py
- test_minimax.py
- sign_in
- Changelog
- test_llm_429_resilience.py
- [0.5.0] — 2026-09-18
- _id_token
- test_deepseek_reasoning.py
- body
- test_a_report_that_was_never_produced_says_so
- test_graph_end_to_end.py
- [0.5.2] — 2026-09-29
- TestStructuredOutputCapabilityDispatch
- [0.2.1] — 2026-03-15
- DeepSeekChatOpenAI
- test_fundamentals_units.py
- test_an_unreachable_yahoo_is_not_reported_as_a_symbol_without_insider_data
- requests
- [0.2.4] — 2026-04-25
- .save_reports
- trading_graph.py
- TestLegacyRemoval
- test_memory_pointintime.py
- [0.2.3] — 2026-03-29
- backtest.py
- [0.3.0] — 2026-06-22
- test_a_throttle_lets_the_next_vendor_try
- Installation and CLI
- test_cli_env_skip.py
- test_it_works_unconfigured_and_takes_the_caller_s_own_contact
- unittest
- test_i18n_coverage.py
- test_the_default_identification_names_the_package_version
- login
- [0.2.5] — 2026-05-11
- TestDeepSeekReasoningContent
- test_the_quarter_is_not_confused_with_the_year_to_date
- test_layering.py
- NormalizedChatOpenAI
- test_opencode_session.py
- [0.5.1] — 2026-09-24
- contact_links
- test_news_analyst_prompt.py
- LoopingModel
- [0.7.0] — 2026-10-16
- build_verified_market_snapshot
- FakeOpenAI
- sign_out
- AGENTS.md
- _Callback
- test_a_settlement_failure_is_noted_and_the_run_goes_on
- tradingagents
- [0.2.0] — 2026-02-04
- test_temperature_config.py
- [0.2.2] — 2026-03-22
- test_news_lookup_normalizes_symbol

## God Nodes (most connected - your core abstractions)
1. `TradingAgentsGraph` - 65 edges
2. `NoMarketDataError` - 60 edges
3. `set_config()` - 54 edges
4. `VendorUnavailableError` - 52 edges
5. `make_log()` - 49 edges
6. `TradingMemoryLog` - 47 edges
7. `get_instrument_context_from_state()` - 44 edges
8. `route_to_vendor()` - 43 edges
9. `get_language_instruction()` - 42 edges
10. `normalize_symbol()` - 39 edges

## Surprising Connections (you probably didn't know these)
- `Python Usage` --references--> `TradingAgentsGraph`  [INFERRED]
  README.md → tradingagents/graph/trading_graph.py
- `Evaluating decisions over time` --references--> `run_backtest()`  [INFERRED]
  README.md → tradingagents/backtest.py
- `Changed` --references--> `VendorError`  [INFERRED]
  CHANGELOG.md → tradingagents/dataflows/errors.py
- `Fixed` --references--> `set_config()`  [INFERRED]
  CHANGELOG.md → tradingagents/dataflows/config.py
- `Fixed` --references--> `get_indicators()`  [INFERRED]
  CHANGELOG.md → tradingagents/agents/tools.py

## Import Cycles
- None detected.

## Communities (155 total, 31 thin omitted)

### Community 0 - "test_dataflows_config.py"
Cohesion: 0.09
Nodes (18): DataflowsConfigIsolationTests, _graph(), test_a_graph_built_earlier_still_runs_with_its_own_config(), test_a_run_config_missing_a_newer_key_still_reads_the_default(), test_a_run_reads_its_own_graphs_vendors_not_the_last_graph_built(), test_concurrent_runs_each_read_their_own_config(), test_settling_reads_the_graphs_own_config(), test_tools_inside_a_langgraph_run_see_the_run_config() (+10 more)

### Community 1 - "test_ohlcv_latest_bar.py"
Cohesion: 0.14
Nodes (16): _run_load(), _stamp(), test_clean_dataframe_keeps_nan_close_for_the_caller_to_inspect(), test_fill_price_gaps_drops_nan_close_rows(), test_no_settled_bar_at_all_is_still_no_data(), test_normalize_dates_handles_mixed_dst_offsets(), test_normalize_dates_keeps_positive_offset_local_date(), test_normalize_dates_leaves_naive_dates_at_midnight() (+8 more)

### Community 2 - "test_cli_updates.py"
Cohesion: 0.06
Nodes (47): _applies(), due(), messages(), _plain(), show(), upgrade_command(), _version(), _dist() (+39 more)

### Community 3 - "test_yfinance_stale_ohlcv_guard.py"
Cohesion: 0.17
Nodes (5): _frame(), StaleGuardPropagationTests, StaleGuardRoutingTests, StaleGuardUnitTests, _assert_ohlcv_not_stale()

### Community 4 - "test_sec_edgar.py"
Cohesion: 0.15
Nodes (12): _columns(), _fact(), _no_network_or_cache(), test_a_cash_flow_filed_year_to_date_is_served_with_its_span(), test_a_period_reported_under_two_tags_takes_the_preferred_one_not_both(), test_a_recast_outside_the_annual_report_still_counts_from_its_filing(), eps(), test_a_row_filed_only_year_to_date_keeps_its_figure_beside_a_row_filed_by_quarter() (+4 more)

### Community 5 - "test_news_lookahead.py"
Cohesion: 0.09
Nodes (37): _epoch(), _tagged(), test_a_flat_article_with_a_null_field_is_read_with_its_default(), test_a_quote_feed_with_articles_is_not_searched(), test_a_search_with_articles_has_answered_even_without_listing_the_symbol(), test_a_search_yahoo_answers_with_not_found_is_an_outage(), test_a_symbol_yahoo_has_no_articles_for_is_left_to_the_next_vendor(), test_a_yahoo_news_outage_moves_to_the_next_configured_vendor() (+29 more)

### Community 6 - "get_instrument_context_from_state"
Cohesion: 0.11
Nodes (33): _capturing_llm(), _investment_state(), _risk_state(), test_helper_marks_empty_and_passes_through(), test_researcher_opening_has_no_phantom_opponent(), test_researcher_passes_real_opponent_argument(), test_risk_opening_has_no_phantom_opponent(), test_risk_passes_real_opponent_arguments() (+25 more)

### Community 7 - "test_cli_symbol_handling.py"
Cohesion: 0.07
Nodes (12): detect_asset_type(), is_valid_ticker_input(), normalize_ticker_symbol(), parse_ticker(), _run_directory(), test_cli_normalize_delegates_to_data_layer(), test_detect_asset_type(), test_normalize_symbol_crypto_and_passthrough() (+4 more)

### Community 8 - "test_alpha_vantage_hardening.py"
Cohesion: 0.10
Nodes (18): _FakeResponse, _patched_get(), fake_get(), test_a_rejected_request_is_unavailable_not_data(), test_an_indicator_this_vendor_lacks_lets_the_next_one_serve_it(), test_empty_body_still_passes_through(), test_fundamentals_no_curr_date_passes_through(), test_global_news_omitted_optionals_use_the_configured_defaults() (+10 more)

### Community 9 - "get_capabilities"
Cohesion: 0.07
Nodes (8): test_capabilities_dataclass_is_frozen(), TestDefault, TestExactIdMatches, TestMinimaxExactMatches, TestOpenRouterDeepSeekNamespace, TestPatternMatches, get_capabilities(), ModelCapabilities

### Community 10 - "router.py"
Cohesion: 0.11
Nodes (15): _yahoo_calls(), vendor_reachable(), _answered_empty(), raise_for_empty(), yf_retry(), get_balance_sheet(), get_cashflow(), get_company_profile() (+7 more)

### Community 11 - "unit"
Cohesion: 0.21
Nodes (12): _config(), test_a_cell_already_in_the_log_is_not_run_again(), test_a_failed_cell_does_not_abort_the_sweep(), test_a_failed_settlement_does_not_lose_the_remaining_tickers(), test_a_resumed_sweep_reports_only_the_cells_it_runs(), test_a_run_id_cannot_escape_the_results_directory(), test_a_ticker_or_date_given_twice_runs_and_settles_once(), test_every_ticker_is_settled_after_the_grid() (+4 more)

### Community 12 - "TradingMemoryLog"
Cohesion: 0.10
Nodes (4): _resolve_entry(), test_concurrent_writers_keep_every_decision_and_outcome(), work(), TradingMemoryLog

### Community 13 - "TestDeferredReflection"
Cohesion: 0.06
Nodes (3): TestDeferredReflection, Reflector, resolve_benchmark()

### Community 14 - "test_chatgpt_provider.py"
Cohesion: 0.05
Nodes (38): _fetch_openrouter_models(), select_openrouter_model(), prompts(), _expired(), refuse(), _llm(), _menu(), signed_in() (+30 more)

### Community 15 - "test_backtest.py"
Cohesion: 0.14
Nodes (18): Highlights, _fake_graph(), _log_with(), _scored(), test_a_backtest_result_is_summarized_directly(), test_a_bearish_call_that_fell_counts_as_right(), test_a_bearish_call_that_rose_counts_as_wrong(), test_a_bullish_call_is_scored_the_same_way_as_before() (+10 more)

### Community 16 - "test_cli_headless.py"
Cohesion: 0.08
Nodes (32): display_complete_report(), _offer_reports(), unattended_gaps(), _answer(), _Browser, _report_graph(), _selections_with_env(), test_a_closed_stdin_counts_as_no_terminal() (+24 more)

### Community 17 - "make_log"
Cohesion: 0.08
Nodes (3): make_log(), _seed_completed(), TestTradingMemoryLogCore

### Community 18 - "fetch_returns"
Cohesion: 0.08
Nodes (10): _closes(), test_a_close_that_is_not_a_price_is_skipped_not_scored(), test_a_failed_reflection_leaves_the_entry_pending_and_lets_the_run_start(), test_a_longer_window_asks_for_enough_price_history(), test_the_holding_window_is_configurable(), test_the_reflection_states_the_window_it_judges(), TestSettlementWindow, test_fetch_returns_normalizes_symbol() (+2 more)

### Community 19 - "test_cli_commands.py"
Cohesion: 0.08
Nodes (25): _Result, runner(), _Summary, test_a_failed_login_exits_with_the_reason(), refuse(), test_a_failure_message_with_brackets_is_printed_as_text(), refuse(), test_backtest_can_continue_an_interrupted_sweep() (+17 more)

### Community 20 - "prompts.py"
Cohesion: 0.05
Nodes (40): backtest(), AnalystType, AssetType, ask_anthropic_effort(), ask_gemini_thinking_config(), ask_glm_region(), ask_minimax_region(), ask_openai_reasoning_effort() (+32 more)

### Community 21 - "stocktwits.py"
Cohesion: 0.10
Nodes (8): _drop_spam(), _raise(), _stream(), test_html_entities_in_message_bodies_are_decoded(), TestStockTwitsCryptoSymbols, TestStockTwitsResilience, TestStockTwitsScreening, _stocktwits_symbol()

### Community 22 - "ohlcv.py"
Cohesion: 0.17
Nodes (12): _fake_msvcrt(), _recording_replace(), test_a_file_held_open_elsewhere_keeps_its_old_content(), test_a_lock_held_elsewhere_is_reported_when_not_waiting(), holder(), test_a_replaced_file_keeps_the_usual_permissions(), test_on_windows_a_held_lock_is_reported_when_not_waiting(), test_on_windows_a_lock_that_cannot_be_taken_is_reported_not_retried_forever() (+4 more)

### Community 23 - "test_portfolio_context.py"
Cohesion: 0.09
Nodes (20): _bare_graph(), test_a_ticker_held_under_another_spelling_is_matched(), test_absent_context_is_reported_as_not_provided(), test_checkpoint_signature_changes_with_the_portfolio(), test_cli_passes_a_valid_portfolio_into_the_run(), test_cli_rejects_an_unusable_portfolio_file_before_running(), test_completed_run_clears_the_checkpoint_it_wrote(), test_create_run_state_renders_the_portfolio_once() (+12 more)

### Community 24 - "requests"
Cohesion: 0.13
Nodes (5): PolymarketFilterTests, PolymarketFormatTests, PolymarketResilienceTests, PolymarketRoutingTests, get_prediction_markets()

### Community 25 - "test_cli_memory_log.py"
Cohesion: 0.07
Nodes (11): _bare_graph(), _FakeBuffer, _FakeGraph, _NullLive, _run_cli(), test_a_run_without_checkpointing_says_nothing_about_resuming(), test_cli_run_uses_the_memory_log_like_propagate(), test_record_decision_appends_a_pending_entry() (+3 more)

### Community 26 - "sec_edgar.py"
Cohesion: 0.14
Nodes (11): test_a_per_share_figure_keeps_its_own_unit(), test_a_us_filer_resolves_to_its_cik(), _as_of(), _cached_json(), cik_for(), _fetch_json(), get_cashflow(), get_income_statement() (+3 more)

### Community 27 - "get_macro_data"
Cohesion: 0.08
Nodes (11): FredConfigTests, FredFormattingTests, _capture(), FredResolutionTests, FredRoutingTests, _request_stub(), test_error_without_the_key_in_its_message_still_drops_the_request(), TestKeyKeptOutOfErrors (+3 more)

### Community 28 - "test_reddit_fallback.py"
Cohesion: 0.07
Nodes (17): _raise(), _resp(), _screen_out(), test_a_crypto_pair_is_fetched_from_its_communities_in_one_request(), test_a_crypto_ticker_is_searched_in_crypto_communities(), test_a_subreddit_emptied_by_screening_is_not_called_empty(), test_an_unavailable_screen_keeps_every_post_and_says_so(), test_each_subreddit_keeps_its_own_quota() (+9 more)

### Community 29 - "test"
Cohesion: 0.07
Nodes (35): concurrency, cancel-in-progress, group, TZ, python-version, tz, jobs, lint (+27 more)

### Community 30 - "reddit.py"
Cohesion: 0.10
Nodes (11): _atom_resp(), TestRss429Backoff, TestRssParsing, _coverage_dates(), _fetch_subreddit_rss(), _jitter(), _posted_at(), _read_capped() (+3 more)

### Community 31 - "test_yahoo_rate_limit.py"
Cohesion: 0.07
Nodes (17): _rate_limited(), test_a_missing_time_zone_is_not_taken_for_an_answer(), test_a_price_request_that_fails_is_unavailable_even_when_yahoo_answers(), test_a_price_request_that_raises_is_unavailable_whether_or_not_yahoo_answers(), test_a_rate_limit_that_outlasts_the_retries_is_reported_as_one(), test_a_request_that_yfinance_would_swallow_is_unavailable(), test_a_snapshot_with_no_rows_is_reported_not_raised(), load() (+9 more)

### Community 32 - "GoogleClient"
Cohesion: 0.16
Nodes (3): TestGoogleApiKeyStandardization, _accepts_minimal_thinking(), GoogleClient

### Community 33 - "OpenAIClient"
Cohesion: 0.11
Nodes (9): _effort_on(), test_non_reasoning_model_drops_effort(), test_reasoning_model_receives_effort(), test_supports_reasoning_effort(), NativeBaseUrlTests, ResponsesApiSelectionTests, _is_native_openai_base_url(), OpenAIClient (+1 more)

### Community 34 - "chatgpt_auth.py"
Cohesion: 0.13
Nodes (10): _b64url_decode(), ChatGPTAuthError, ChatGPTUnreachable, _due(), _oauth_error(), _refresh(), _signing_keys(), _token_record() (+2 more)

### Community 36 - "NoMarketDataError"
Cohesion: 0.06
Nodes (27): TestRouteToVendorSentinel, raises_no_data(), raises_no_data(), not_covered(), throttled(), _stale(), get_balance_sheet(), get_cashflow() (+19 more)

### Community 37 - "test_rating_integrity.py"
Cohesion: 0.05
Nodes (21): _FakeGraph, test_a_decision_prompt_states_the_shape_of_its_answer(), test_a_quoted_rating_in_a_list_table_or_quote_is_not_the_decision(), test_a_rating_argued_against_is_not_read_as_the_decision(), test_a_rating_someone_else_gave_does_not_become_the_decision(), test_a_rating_the_text_quotes_does_not_replace_the_decision(), test_a_rating_word_without_a_label_is_not_read_as_the_call(), test_a_refusal_has_no_rating_and_is_not_defaulted() (+13 more)

### Community 38 - "test_ollama_base_url.py"
Cohesion: 0.10
Nodes (17): _base_url(), _client_module(), _console_out(), test_client_get_llm_picks_up_env(), test_confirm_endpoint_marks_env_origin(), test_confirm_endpoint_quiet_on_local_no_port(), test_confirm_endpoint_shows_default(), test_confirm_endpoint_warns_on_missing_scheme() (+9 more)

### Community 39 - "ResearchPlan"
Cohesion: 0.13
Nodes (12): prompt(), _make_rm_state(), _structured_rm_llm(), TestRenderResearchPlan, TestResearchManagerAgent, create_research_manager(), research_manager_node(), render_research_plan() (+4 more)

### Community 40 - "VendorUnavailableError"
Cohesion: 0.09
Nodes (24): Upgrading from 0.5.0, test_a_current_run_is_still_served_yahoo_statements(), test_yahoo_withholds_insider_trades_from_a_past_run_without_asking(), _dates_after(), _insider_frame(), test_a_current_run_is_not_cluttered_with_a_vintage_note(), test_a_historical_run_gets_the_current_name_only_as_an_identifier(), test_a_historical_run_is_not_told_todays_date() (+16 more)

### Community 41 - "TraderProposal"
Cohesion: 0.11
Nodes (14): _make_trader_state(), _structured_trader_llm(), test_a_price_that_is_a_number_survives(), test_a_price_written_as_a_range_drops_only_that_field(), test_conflict_alone_is_not_a_hold_trigger(), test_invoke_structured_falls_back_when_result_is_none(), test_the_trader_names_the_levels_it_did_not_give(), TestNullishFloatCoercion (+6 more)

### Community 42 - "fetch_reddit_posts"
Cohesion: 0.11
Nodes (19): TestOneRequestForAllSubreddits, _epoch(), _JsonResp, _msg(), test_reddit_covered_but_empty_window_is_a_real_absence(), test_reddit_empty_feed_for_an_old_window_is_unavailable(), test_reddit_full_page_does_not_vouch_for_older_days(), test_reddit_historical_window_excludes_recent() (+11 more)

### Community 43 - "BaseLLMClient"
Cohesion: 0.24
Nodes (10): _captured(), _config(), test_a_tier_on_another_provider_gets_that_provider_s_settings_and_not_the_main_url(), test_a_tier_url_is_used_for_that_tier_only(), test_a_tier_without_its_own_provider_uses_the_run_s(), test_the_run_settings_and_report_name_each_tier_s_provider(), test_the_tier_settings_are_read_from_the_environment(), create_tier_client() (+2 more)

### Community 44 - "build"
Cohesion: 0.07
Nodes (29): env, name, permissions, runs-on, steps, concurrency, cancel-in-progress, group (+21 more)

### Community 45 - "create_sentiment_analyst"
Cohesion: 0.12
Nodes (10): _make_sentiment_state(), _structured_sentiment_llm(), TestRenderSentimentReport, TestSentimentAnalystAgent, _build_system_message(), create_sentiment_analyst(), sentiment_analyst_node(), _seven_days_back() (+2 more)

### Community 46 - "openai_client.py"
Cohesion: 0.07
Nodes (8): NormalizedChatAnthropic, _supports_effort(), BaseLLMClient, normalize_content(), _bedrock_class(), invoke(), BedrockClient, NormalizedChatGoogleGenerativeAI

### Community 47 - "test_cli_prefs.py"
Cohesion: 0.14
Nodes (17): load_last_run(), sanitize(), save_last_run(), get_user_selections(), _answer_every_prompt(), test_a_corrupt_file_degrades_to_no_memory(), test_a_custom_language_is_remembered_without_breaking_the_next_run(), test_a_half_written_file_cannot_be_observed() (+9 more)

### Community 48 - "Propagator"
Cohesion: 0.08
Nodes (4): TestPortfolioManagerInjection, InvestDebateState, RiskDebateState, Propagator

### Community 49 - "normalize_symbol"
Cohesion: 0.10
Nodes (6): TestCryptoBase, TestNoMarketDataError, TestNormalizeSymbol, crypto_base(), _normalize_crypto(), normalize_symbol()

### Community 50 - "_make_api_request"
Cohesion: 0.10
Nodes (16): is_historical(), withhold_undated_statements(), withhold_undisclosed_trades(), AlphaVantageNotConfiguredError, AlphaVantageRateLimitError, _filter_csv_by_date_range(), format_datetime_for_api(), get_api_key() (+8 more)

### Community 51 - "test_api_key_env.py"
Cohesion: 0.07
Nodes (22): _build_run_config(), _prompt_key(), test_case_insensitive_lookup(), test_ensure_api_key_prompts_and_writes_to_env(), test_ensure_api_key_updates_existing_env_file(), test_ensure_api_key_user_cancels_returns_none(), test_every_select_llm_provider_choice_has_an_entry(), test_existing_key_file_is_tightened_before_writing() (+14 more)

### Community 52 - "create_llm_client"
Cohesion: 0.12
Nodes (18): _capture_kwargs(), test_bearer_token_passed_as_api_key(), test_bedrock_any_model_and_no_key_env(), test_construction_when_extra_installed(), test_factory_routes_bedrock(), test_helpful_error_when_langchain_aws_absent(), test_no_bearer_token_omits_api_key(), test_any_model_accepted_no_forced_key() (+10 more)

### Community 53 - "test_env_overrides.py"
Cohesion: 0.13
Nodes (12): _config_with_env(), test_bool_coercion(), test_empty_env_value_is_passthrough(), test_empty_path_value_keeps_the_default_path(), test_int_coercion(), test_invalid_bool_raises(), test_invalid_int_raises(), test_no_env_uses_built_in_defaults() (+4 more)

### Community 54 - "Settlement"
Cohesion: 0.12
Nodes (6): test_a_run_does_not_wait_on_another_settlement_pass(), other_pass(), test_the_graph_settles_every_ticker_under_its_own_config(), TestSettleAll, settle_all_pending(), Settlement

### Community 55 - "tradingagents-ollama"
Cohesion: 0.08
Nodes (23): image, profiles, volumes, services, ollama, tradingagents, tradingagents-ollama, build (+15 more)

### Community 56 - "test_chatgpt_auth.py"
Cohesion: 0.23
Nodes (17): _renewal(), _signed_in(), test_a_fresh_token_is_used_without_asking_openai(), test_a_refused_renewal_asks_to_sign_in_again_and_keeps_the_file(), test_a_renewal_for_another_account_is_refused(), test_a_temporary_failure_after_expiry_says_to_try_again_not_to_sign_in(), test_a_temporary_failure_keeps_a_token_that_still_works(), test_a_token_near_expiry_is_renewed_with_the_stored_refresh_token() (+9 more)

### Community 57 - "ConditionalLogic"
Cohesion: 0.09
Nodes (17): handler(), _debate_state(), _state(), test_debate_path_map_covers_full_router_range(), test_debate_router_return_always_routable(), test_path_map_covers_full_router_range(), test_router_return_always_routable(), test_router_terminates_at_round_limit() (+9 more)

### Community 58 - "test_statement_knowledge_time.py"
Cohesion: 0.36
Nodes (4): test_alpha_vantage_withholds_insider_trades_from_a_past_run_without_asking(), test_alpha_vantage_withholds_statements_from_a_past_run_without_asking(), test_statements_come_from_sec_edgar_first_by_default(), test_yahoo_withholds_statements_from_a_past_run_without_asking()

### Community 59 - "test_tool_date_enforcement.py"
Cohesion: 0.16
Nodes (16): _run(), _State, test_a_start_date_that_is_not_a_date_is_sent_back_to_the_model(), test_a_tool_serves_the_run_instrument_whatever_the_model_passes(), test_a_window_whose_start_is_not_a_date_is_refused(), test_as_of_takes_the_earlier_date(), test_as_of_window(), test_as_of_without_a_trade_date_passes_the_request_through() (+8 more)

### Community 60 - "run_analysis"
Cohesion: 0.05
Nodes (25): AnalystWallTimeTracker, classify_message_type(), create_layout(), extract_content_string(), format_tokens(), format_tool_args(), MessageBuffer, sync_analyst_tracker_from_chunk() (+17 more)

### Community 61 - "re"
Cohesion: 0.11
Nodes (30): _fields(), _html(), _state(), test_an_agent_s_own_headings_sit_below_its_heading(), test_header_values_are_escaped(), test_report_text_cannot_inject_markup_or_fetch_anything(), test_run_details_show_each_value_as_its_own_field(), test_the_contents_name_each_section_once_and_list_its_agents_beneath() (+22 more)

### Community 62 - "safe_ticker_component"
Cohesion: 0.05
Nodes (23): _bare_graph(), _node_a(), _node_b(), _State, test_begin_returns_thread_id_and_recompiles(), test_checkpoint_input_is_none_only_when_resuming(), test_clearing_removes_the_database_sidecars(), test_cli_style_usage_saves_then_resumes() (+15 more)

### Community 63 - "test_fundamentals_lookahead.py"
Cohesion: 0.13
Nodes (6): _av(), TestAlphaVantageHistoricalRun, TestLiveRunUnchanged, TestNoUsableFieldsStillRaises, TestYFinanceHistoricalRun, _yf()

### Community 64 - "build_llm_kwargs"
Cohesion: 0.17
Nodes (16): _config_with_env(), test_coerce_accepts_positive_ints_and_numeric_strings(), test_coerce_rejects_booleans(), test_coerce_rejects_non_integers(), test_coerce_rejects_non_positive(), test_default_is_none(), test_env_override_sets_config(), test_env_string_is_coerced() (+8 more)

### Community 65 - "VendorRoutingTests"
Cohesion: 0.19
Nodes (6): _no_data(), _raises(), _reset_config(), _returns(), impl(), VendorRoutingTests

### Community 66 - "AnthropicClient"
Cohesion: 0.18
Nodes (3): _capture_kwargs(), TestEffortGate, AnthropicClient

### Community 67 - "resolve_instrument_identity"
Cohesion: 0.09
Nodes (8): BuildInstrumentContextTests, GetInstrumentContextFromStateTests, ResolveInstrumentIdentityTests, test_identity_lookup_normalizes_symbol(), build_instrument_context(), _clean_identity_value(), _identity(), resolve_instrument_identity()

### Community 68 - "TradingAgents: Multi-Agents LLM Financial Trading Framework"
Cohesion: 0.10
Nodes (19): Analyst Team, Checkpoint resume, Citation, Contributing, Current holdings, Evaluating decisions over time, Fundamentals as filed, Implementation Details (+11 more)

### Community 69 - "test_post_screen.py"
Cohesion: 0.07
Nodes (37): _Calls, jev(), _ok(), post(), _post_answers(), fake_post(), _Response, test_a_base_url_without_a_key_does_not_turn_screening_on() (+29 more)

### Community 70 - "test_provider_registry.py"
Cohesion: 0.16
Nodes (10): _Recorder, _signed_in_provider(), test_a_missing_sign_in_fails_before_any_request(), test_a_signed_in_provider_refuses_another_endpoint_or_key(), test_a_signed_in_provider_sends_its_own_credential_never_an_api_key(), test_key_optionality(), test_registry_membership(), test_registry_spec() (+2 more)

### Community 72 - "unit"
Cohesion: 0.15
Nodes (11): test_a_filer_with_no_usable_facts_reads_differently_from_a_non_filer(), test_a_line_the_filer_does_not_tag_is_named_unavailable(), test_a_non_filer_is_reported_as_such_not_as_missing_data(), test_a_period_that_ended_but_was_not_filed_yet_is_not_served(), test_a_restated_figure_reads_as_it_did_at_the_time(), test_a_server_error_lets_the_next_vendor_try(), test_company_facts_are_fetched_once_per_company_not_once_per_date(), test_every_row_has_one_cell_per_period() (+3 more)

### Community 73 - "test_memory_log.py"
Cohesion: 0.11
Nodes (8): _make_pm_state(), _structured_pm_llm(), test_a_field_the_model_did_not_give_says_so(), create_portfolio_manager(), portfolio_manager_node(), _coerce_optional_float(), PortfolioDecision, render_pm_decision()

### Community 74 - "test_llm_max_retries.py"
Cohesion: 0.25
Nodes (12): _config_with_env(), test_coerce_accepts_non_negative_ints_and_numeric_strings(), test_coerce_rejects_booleans(), test_coerce_rejects_negative(), test_coerce_rejects_non_integers(), test_default_is_none(), test_env_override_sets_config(), test_forwarded_across_providers() (+4 more)

### Community 75 - "settle_pending"
Cohesion: 0.13
Nodes (4): test_any_failure_to_price_a_decision_is_reported(), TestSettlementOnceAndDurably, down(), settle_pending()

### Community 76 - "test_model_validation.py"
Cohesion: 0.18
Nodes (7): DummyLLMClient, ModelValidationTests, test_a_retired_model_id_still_runs_without_a_warning(), test_an_explicit_alias_of_a_listed_model_is_known(), test_every_provider_lets_you_name_your_own_model(), test_legacy_ids_stay_valid_without_being_offered(), get_known_models()

### Community 77 - "_price_df"
Cohesion: 0.16
Nodes (5): _price_df(), _make_ticker(), _make_ticker(), _make_ticker(), _make_ticker()

### Community 78 - "test_google_thinking_level.py"
Cohesion: 0.24
Nodes (9): _captured_kwargs(), test_a_gemini_call_times_out_like_the_other_providers(), test_flash_38_keeps_supported_levels(), test_flash_38_remaps_minimal_to_low(), test_flash_passes_thinking_level_through(), test_latest_alias_remaps_minimal_to_low(), test_no_thinking_level_is_omitted(), test_pro_keeps_high() (+1 more)

### Community 79 - "conftest.py"
Cohesion: 0.14
Nodes (7): _at_a_terminal(), _blank_settings_overlay(), _dummy_api_keys(), _isolate_config(), _no_network(), _own_cli_prefs(), _own_file_locations()

### Community 80 - "RouterHandlesBaseTypesTests"
Cohesion: 0.22
Nodes (4): RouterHandlesBaseTypesTests, _unconfigured(), _throttled(), _unconfigured()

### Community 82 - "stocktwits.py"
Cohesion: 0.11
Nodes (9): TestStripHtml, test_in_window_bounds_and_exclusive_upper(), test_in_window_undated_excluded_in_backtest_kept_live(), in_window(), to_utc(), _strip_html(), _body(), _created_at() (+1 more)

### Community 83 - "_graph"
Cohesion: 0.15
Nodes (12): _graph(), ScriptedModel, test_a_debug_run_prints_the_analysts_work_and_reaches_the_same_decision(), test_a_full_run_reaches_a_logged_decision(), test_a_graph_reused_across_runs_keeps_no_run_state(), test_a_streamed_run_reads_its_own_graph_config(), test_a_tool_limit_the_recursion_limit_cannot_hold_is_refused(), test_an_interrupted_run_resumes_from_its_checkpoint() (+4 more)

### Community 84 - "updates.py"
Cohesion: 0.13
Nodes (11): enabled(), _get_json(), parse_notices(), read_cache(), refresh(), start_background_refresh(), summary_of(), _bare_graph() (+3 more)

### Community 85 - "test_structured_agent_prompts.py"
Cohesion: 0.23
Nodes (11): _capturing_llm(), _prompt_text(), test_constraint_text_is_unambiguous(), test_portfolio_manager_prompt_states_constraint(), test_research_manager_prompt_states_constraint(), test_sentiment_prompt_states_constraint(), test_the_sentiment_prompt_names_the_subreddits_searched(), test_tool_using_analysts_keep_their_date_guidance() (+3 more)

### Community 86 - "ohlcv.py"
Cohesion: 0.07
Nodes (16): test_get_yfin_requests_inclusive_end(), test_load_ohlcv_requests_inclusive_end(), _ohlcv(), test_cleaning_a_frame_with_undated_rows_writes_to_its_own_copy(), TestCleanDataframeAcrossVersions, TestEnsureDateColumn, VendorError, get_stock_stats() (+8 more)

### Community 87 - "attributes"
Cohesion: 0.12
Nodes (15): description, label, options, placeholder, render, value, body, attributes (+7 more)

### Community 88 - "attributes"
Cohesion: 0.12
Nodes (15): description, label, multiple, options, placeholder, value, body, attributes (+7 more)

### Community 90 - "test_suite_isolation.py"
Cohesion: 0.21
Nodes (4): test_a_test_cannot_reach_the_network(), test_a_test_saves_cli_selections_to_its_own_directory(), test_the_suite_keeps_its_files_out_of_the_users_home(), test_yfinance_keeps_its_cache_out_of_the_users_home()

### Community 91 - "test_minimax.py"
Cohesion: 0.20
Nodes (4): _client(), TestMinimaxReasoningSplit, TestMinimaxStructuredOutputDispatch, _Pick

### Community 92 - "sign_in"
Cohesion: 0.18
Nodes (16): _nonce_of(), _paster(), read_line(), _status(), test_a_network_failure_while_signing_in_is_reported_not_raised_raw(), test_a_sign_in_without_plan_usage_is_refused(), test_an_answer_for_another_sign_in_attempt_is_ignored(), test_another_account_cannot_replace_the_signed_in_one() (+8 more)

### Community 93 - "Changelog"
Cohesion: 0.17
Nodes (12): [0.1.0] — 2025-06-05, [0.1.1] — 2025-06-07, [0.3.1] — 2026-07-05, [0.4.0] — 2026-08-31, Added, Added, Added, Changelog (+4 more)

### Community 94 - "test_llm_429_resilience.py"
Cohesion: 0.15
Nodes (8): _chat(), test_dependency_wiring_goes_the_same_route(), test_every_429_fails_after_the_retry_cap_with_a_clear_message(), test_one_429_with_retry_after_then_200_succeeds(), test_the_clear_message_never_carries_the_api_key(), test_unconfigured_providers_keep_sdk_defaults(), _transport(), LLMCapacityError

### Community 95 - "[0.5.0] — 2026-09-18"
Cohesion: 0.25
Nodes (8): [0.5.0] — 2026-09-18, Changed, CLI, Contributors, Data sources, Decisions and evaluation, Models, Point-in-time and honest attribution

### Community 96 - "_id_token"
Cohesion: 0.36
Nodes (8): _b64(), _id_token(), _jwks(), test_a_genuine_id_token_is_accepted(), test_an_id_token_for_another_sign_in_is_refused(), test_an_id_token_signed_by_another_key_is_refused(), test_signing_in_by_pasting_the_redirect_saves_a_private_sign_in(), token()

### Community 97 - "test_deepseek_reasoning.py"
Cohesion: 0.16
Nodes (3): TestBaseClassIsolation, TestInputToMessages, _input_to_messages()

### Community 98 - "body"
Cohesion: 0.15
Nodes (12): description, label, value, body, attributes, id, type, validations (+4 more)

### Community 99 - "test_a_report_that_was_never_produced_says_so"
Cohesion: 0.24
Nodes (3): test_a_report_that_was_never_produced_says_so(), test_an_analyst_brief_is_text_not_a_python_object(), test_an_analyst_is_not_asked_for_a_trade_call_nothing_reads()

### Community 100 - "test_graph_end_to_end.py"
Cohesion: 0.15
Nodes (4): _Client, offline(), test_past_decisions_settle_alongside_the_analysts(), TimedModel

### Community 101 - "[0.5.2] — 2026-09-29"
Cohesion: 0.33
Nodes (6): [0.5.2] — 2026-09-29, Added, Contributors, Fixed, Models, Upgrading from 0.5.1

### Community 103 - "[0.2.1] — 2026-03-15"
Cohesion: 0.33
Nodes (6): [0.2.1] — 2026-03-15, Added, Contributors, Fixed, Removed, Security

### Community 104 - "DeepSeekChatOpenAI"
Cohesion: 0.20
Nodes (4): TestDeepSeekLiveStructuredOutput, _Pick, _Sample, DeepSeekChatOpenAI

### Community 105 - "test_fundamentals_units.py"
Cohesion: 0.33
Nodes (7): _fundamentals(), test_a_figure_with_no_stated_currency_is_printed_bare(), test_an_absent_percent_field_is_left_out(), test_an_adr_quotes_in_dollars_and_reports_in_its_home_currency(), test_each_money_figure_carries_the_currency_it_is_in(), test_income_figures_without_a_stated_reporting_currency_are_printed_bare(), test_percent_fields_carry_their_unit_and_fractions_are_unchanged()

### Community 107 - "requests"
Cohesion: 0.15
Nodes (9): _call(), _response(), test_a_passthrough_status_is_returned_for_the_caller(), test_nothing_that_holds_the_url_travels_with_the_error(), test_the_key_is_masked_in_the_error(), get_scrubbed(), _is_forward_looking(), _parse_json_list() (+1 more)

### Community 108 - "[0.2.4] — 2026-04-25"
Cohesion: 0.33
Nodes (6): [0.2.4] — 2026-04-25, Added, Changed, Contributors, Fixed, Removed

### Community 109 - ".save_reports"
Cohesion: 0.18
Nodes (7): [0.6.0] — 2026-10-03, Added, Added, Contributors, Fixed, Models, Upgrading from 0.5.2

### Community 110 - "trading_graph.py"
Cohesion: 0.06
Nodes (17): _graphical_browser(), _open_page(), _yes(), is_review(), run_rating(), replace_file(), _apply_env_overrides(), build_default_config() (+9 more)

### Community 112 - "test_memory_pointintime.py"
Cohesion: 0.44
Nodes (8): _log(), _resolve(), test_as_of_excludes_lessons_resolved_after_the_run_date(), test_cross_ticker_lessons_are_also_gated(), test_legacy_entry_without_resolution_date_excluded_in_backtest(), test_memory_as_of_gates_historical_but_not_live(), test_no_as_of_is_unfiltered_live_behavior(), test_resolution_date_is_stored_and_parsed()

### Community 113 - "[0.2.3] — 2026-03-29"
Cohesion: 0.40
Nodes (5): [0.2.3] — 2026-03-29, Added, Changed, Contributors, Fixed

### Community 114 - "backtest.py"
Cohesion: 0.15
Nodes (8): test_grid_rejects_a_non_canonical_date(), test_grid_spacing_and_canonical_dates(), test_grid_stops_at_today(), _alpha(), BacktestSummary, _canonical(), iter_grid(), RatingScore

### Community 115 - "[0.3.0] — 2026-06-22"
Cohesion: 0.40
Nodes (5): [0.3.0] — 2026-06-22, Changed, Contributors, Fixed, Removed

### Community 117 - "Installation and CLI"
Cohesion: 0.29
Nodes (7): CLI Usage, Docker, Installation, Installation and CLI, Markets and tickers, Rate-limited endpoints (429), Required APIs

### Community 118 - "test_cli_env_skip.py"
Cohesion: 0.19
Nodes (5): provider_default_url(), TestCliSkipsPromptsFromEnv, TestProviderDefaultUrl, TestReasoningEffortSkippedFromEnv, TestResearchDepthSkippedFromEnv

### Community 120 - "unittest"
Cohesion: 0.12
Nodes (6): _unconfigured(), HierarchyTests, VendorNotConfiguredError, _fred_today(), FredNotConfiguredError, get_api_key()

### Community 124 - "[0.2.5] — 2026-05-11"
Cohesion: 0.40
Nodes (5): [0.2.5] — 2026-05-11, Added, Changed, Fixed, Security

### Community 129 - "test_opencode_session.py"
Cohesion: 0.19
Nodes (9): test_get_llm_attaches_headers_for_opencode(), test_get_llm_no_headers_elsewhere(), test_headers_only_for_opencode(), test_opencode_endpoint_detection(), test_session_id_env_override(), test_session_id_stable_within_process(), is_opencode_endpoint(), request_headers() (+1 more)

### Community 130 - "[0.5.1] — 2026-09-24"
Cohesion: 0.40
Nodes (5): [0.5.1] — 2026-09-24, Added, Contributors, Fixed, Models

### Community 132 - "contact_links"
Cohesion: 0.33
Nodes (5): blank_issues_enabled, contact_links, about, name, url

### Community 134 - "LoopingModel"
Cohesion: 0.33
Nodes (3): LoopingModel, test_an_analyst_that_keeps_calling_tools_writes_its_report_at_the_limit(), test_the_last_turn_is_offered_no_tools_and_reads_its_tool_results_as_text()

### Community 135 - "[0.7.0] — 2026-10-16"
Cohesion: 0.40
Nodes (5): [0.7.0] — 2026-10-16, Added, Contributors, Fixed, Upgrading from 0.6.0

### Community 136 - "build_verified_market_snapshot"
Cohesion: 0.18
Nodes (6): _sample_ohlcv(), TestTool, TestVerifiedSnapshot, build_verified_market_snapshot(), _fmt(), _verified_rows()

### Community 137 - "FakeOpenAI"
Cohesion: 0.20
Nodes (4): FakeOpenAI, home(), openai(), _Response

### Community 140 - "sign_out"
Cohesion: 0.18
Nodes (7): test_signing_out_revokes_the_sign_in_and_keeps_only_the_host_id(), test_signing_out_while_openai_is_unreachable_still_forgets_the_sign_in(), locked(), _read(), sign_out(), signed_in_as(), _write()

### Community 153 - "[0.2.0] — 2026-02-04"
Cohesion: 0.40
Nodes (5): [0.2.0] — 2026-02-04, Added, Changed, Contributors, Fixed

### Community 161 - "test_temperature_config.py"
Cohesion: 0.16
Nodes (3): TestProviderKwargsTemperature, TestTemperatureEnvOverlay, TestTemperatureForwarding

### Community 163 - "[0.2.2] — 2026-03-22"
Cohesion: 0.40
Nodes (5): [0.2.2] — 2026-03-22, Added, Changed, Contributors, Fixed

## Knowledge Gaps
- **1 isolated node(s):** `tradingagents`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1301 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **31 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `TradingAgentsGraph` connect `TradingAgentsGraph` to `test_dataflows_config.py`, `unit`, `test_cli_headless.py`, `fetch_returns`, `test_portfolio_context.py`, `test_cli_memory_log.py`, `BaseLLMClient`, `Propagator`, `Settlement`, `ConditionalLogic`, `test_tool_date_enforcement.py`, `run_analysis`, `re`, `safe_ticker_component`, `TradingAgents: Multi-Agents LLM Financial Trading Framework`, `_graph`, `updates.py`, `.save_reports`, `trading_graph.py`, `TestLegacyRemoval`, `test_memory_pointintime.py`, `backtest.py`?**
  _High betweenness centrality (0.059) - this node is a cross-community bridge._
- **Are the 23 inferred relationships involving `TradingAgentsGraph` (e.g. with `Python Usage` and `_bare_graph()`) actually correct?**
  _`TradingAgentsGraph` has 23 INFERRED edges - model-reasoned connections that need verification._
- **What connects `tradingagents` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `test_dataflows_config.py` be split into smaller, more focused modules?**
  _Cohesion score 0.09390243902439024 - nodes in this community are weakly interconnected._
- **Why does `TradingMemoryLog` connect `TradingMemoryLog` to `test_rating_integrity.py`, `VendorUnavailableError`, `sign_out`, `trading_graph.py`, `test_backtest.py`, `Propagator`, `make_log`, `fetch_returns`, `TestLegacyRemoval`, `test_memory_pointintime.py`, `backtest.py`, `test_portfolio_context.py`, `test_cli_memory_log.py`, `ConditionalLogic`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Are the 22 inferred relationships involving `NoMarketDataError` (e.g. with `TestNoUsableFieldsStillRaises` and `TestLoadOhlcvNoPoison`) actually correct?**
  _`NoMarketDataError` has 22 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_ohlcv_latest_bar.py` be split into smaller, more focused modules?**
  _Cohesion score 0.14153846153846153 - nodes in this community are weakly interconnected._