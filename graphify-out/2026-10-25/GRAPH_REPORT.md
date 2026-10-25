# Graph Report - TradingAgents-fork  (2026-10-25)

## Corpus Check
- 197 files · ~126,860 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 5, .example 2)

## Summary
- 3591 nodes · 8325 edges · 169 communities (135 shown, 34 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 470 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5c7403eb`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_dataflows_config.py
- test_ohlcv_latest_bar.py
- test_cli_updates.py
- NoMarketDataError
- test_sec_edgar.py
- test_news_lookahead.py
- get_instrument_context_from_state
- prompts.py
- test_fundamentals_ask_a_new_ticker_after_a_rate_limit
- get_capabilities
- ohlcv.py
- test_backtest.py
- TradingMemoryLog
- TestDeferredReflection
- test_chatgpt_provider.py
- select_openrouter_model
- test_cli_headless.py
- make_log
- fetch_returns
- test_cli_commands.py
- selections.py
- stocktwits.py
- ohlcv.py
- test_portfolio_context.py
- requests
- test_cli_memory_log.py
- .warn_if_unknown_model
- get_macro_data
- test_reddit_fallback.py
- test
- reddit.py
- test_yahoo_rate_limit.py
- GoogleClient
- OpenAIClient
- chatgpt_auth.py
- TradingAgentsGraph
- tools.py
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
- test_alpha_vantage_hardening.py
- test_api_key_env.py
- create_llm_client
- test_env_overrides.py
- _fetch_subreddit_rss
- tradingagents-ollama
- test_chatgpt_auth.py
- ConditionalLogic
- pytest
- test_tool_date_enforcement.py
- display.py
- re
- checkpointer.py
- test_fundamentals_lookahead.py
- build_llm_kwargs
- VendorRoutingTests
- AnthropicClient
- resolve_instrument_identity
- TradingAgents: Multi-Agents LLM Financial Trading Framework
- test_post_screen.py
- [0.4.0] — 2026-08-31
- StatsCallbackHandler
- test_cli_config_precedence.py
- test_memory_log.py
- test_llm_max_retries.py
- settle_pending
- test_model_validation.py
- get_global_news_yfinance
- test_cli_display.py
- conftest.py
- RouterHandlesBaseTypesTests
- analyze
- stocktwits.py
- _graph
- updates.py
- test_structured_agent_prompts.py
- yahoo/__init__.py
- attributes
- attributes
- AzureOpenAIClient
- test_checkpoint_lifecycle.py
- test_minimax.py
- sign_in
- Changelog
- test_llm_429_resilience.py
- [0.5.0] — 2026-09-18
- MessageBuffer
- test_deepseek_reasoning.py
- body
- test_a_report_that_was_never_produced_says_so
- test_graph_end_to_end.py
- safe_ticker_component
- TestStructuredOutputCapabilityDispatch
- [0.2.1] — 2026-03-15
- DeepSeekChatOpenAI
- test_fundamentals_units.py
- analyst_execution.py
- os
- [0.2.4] — 2026-04-25
- .save_reports
- run.py
- TestLegacyRemoval
- test_memory_pointintime.py
- AnalystWallTimeTracker
- backtest.py
- test_checkpoint_resume.py
- set_config
- Installation and CLI
- test_cli_env_skip.py
- test_cli_updates.py
- VendorError
- test_i18n_coverage.py
- TestOneRequestForAllSubreddits
- login
- [0.2.5] — 2026-05-11
- TestDeepSeekReasoningContent
- _analyst_graph
- test_layering.py
- NormalizedChatOpenAI
- test_opencode_session.py
- [0.5.1] — 2026-09-24
- run_analysis
- contact_links
- test_news_analyst_prompt.py
- LoopingModel
- [0.7.0] — 2026-10-16
- build_verified_market_snapshot
- test_chatgpt_auth.py
- TradingAgents Framework
- sign_out
- AGENTS.md
- _Callback
- coverage_gap
- locked
- test_a_settlement_failure_is_noted_and_the_run_goes_on
- FredRoutingTests
- tradingagents
- [0.2.0] — 2026-02-04
- TradingAgents Package
- _applies
- thread_id
- build_default_config
- _resolve_entry
- create_trader
- _extract_article_data
- TestProviderKwargsTemperature
- get_verified_market_snapshot
- [0.2.2] — 2026-03-22
- extract_content_string
- _strip_html
- test_news_lookup_normalizes_symbol
- test_unconfigured_providers_keep_sdk_defaults
- _coerce_timeout

## God Nodes (most connected - your core abstractions)
1. `TradingAgentsGraph` - 68 edges
2. `NoMarketDataError` - 60 edges
3. `set_config()` - 54 edges
4. `VendorUnavailableError` - 52 edges
5. `make_log()` - 49 edges
6. `TradingMemoryLog` - 48 edges
7. `get_instrument_context_from_state()` - 44 edges
8. `route_to_vendor()` - 43 edges
9. `get_language_instruction()` - 42 edges
10. `normalize_symbol()` - 39 edges

## Surprising Connections (you probably didn't know these)
- `Fixed` --references--> `get_indicators()`  [INFERRED]
  CHANGELOG.md → tradingagents/agents/tools.py
- `Evaluating decisions over time` --references--> `run_backtest()`  [INFERRED]
  README.md → tradingagents/backtest.py
- `Fixed` --references--> `set_config()`  [INFERRED]
  CHANGELOG.md → tradingagents/dataflows/config.py
- `Changed` --references--> `VendorError`  [INFERRED]
  CHANGELOG.md → tradingagents/dataflows/errors.py
- `Python Usage` --references--> `TradingAgentsGraph`  [INFERRED]
  README.md → tradingagents/graph/trading_graph.py

## Import Cycles
- None detected.

## Communities (169 total, 34 thin omitted)

### Community 0 - "test_dataflows_config.py"
Cohesion: 0.15
Nodes (13): _graph(), test_a_graph_built_earlier_still_runs_with_its_own_config(), test_a_run_config_missing_a_newer_key_still_reads_the_default(), test_a_run_reads_its_own_graphs_vendors_not_the_last_graph_built(), test_concurrent_runs_each_read_their_own_config(), _run(), test_settling_reads_the_graphs_own_config(), test_tools_inside_a_langgraph_run_see_the_run_config() (+5 more)

### Community 1 - "test_ohlcv_latest_bar.py"
Cohesion: 0.16
Nodes (15): _run_load(), _stamp(), test_clean_dataframe_keeps_nan_close_for_the_caller_to_inspect(), test_fill_price_gaps_drops_nan_close_rows(), test_no_settled_bar_at_all_is_still_no_data(), test_normalize_dates_handles_mixed_dst_offsets(), test_normalize_dates_keeps_positive_offset_local_date(), test_normalize_dates_leaves_naive_dates_at_midnight() (+7 more)

### Community 2 - "test_cli_updates.py"
Cohesion: 0.17
Nodes (16): due(), messages(), show(), test_a_cache_of_the_wrong_shape_is_no_news(), test_a_check_dated_in_the_future_is_due(), test_a_check_is_due_once_a_day(), test_a_newer_release_is_announced_once_in_the_notice(), test_a_notice_is_shown_as_plain_text_with_only_a_web_link() (+8 more)

### Community 3 - "NoMarketDataError"
Cohesion: 0.08
Nodes (11): TestLoadOhlcvNoPoison, TestRouteToVendorSentinel, raises_no_data(), raises_no_data(), TestNoMarketDataError, _frame(), StaleGuardPropagationTests, StaleGuardRoutingTests (+3 more)

### Community 4 - "test_sec_edgar.py"
Cohesion: 0.06
Nodes (38): _columns(), _fact(), _no_network_or_cache(), test_a_cash_flow_filed_year_to_date_is_served_with_its_span(), test_a_filer_with_no_usable_facts_reads_differently_from_a_non_filer(), test_a_line_the_filer_does_not_tag_is_named_unavailable(), test_a_non_filer_is_reported_as_such_not_as_missing_data(), test_a_per_share_figure_keeps_its_own_unit() (+30 more)

### Community 5 - "test_news_lookahead.py"
Cohesion: 0.20
Nodes (21): _tagged(), test_a_quote_feed_with_articles_is_not_searched(), test_a_search_with_articles_has_answered_even_without_listing_the_symbol(), test_a_search_yahoo_answers_with_not_found_is_an_outage(), test_a_symbol_yahoo_has_no_articles_for_is_left_to_the_next_vendor(), test_an_empty_quote_feed_falls_back_to_the_articles_search_tags_with_the_symbol(), test_news_neither_yahoo_source_answers_is_a_vendor_outage(), test_offset_aware_timestamp_is_converted_not_truncated() (+13 more)

### Community 6 - "get_instrument_context_from_state"
Cohesion: 0.11
Nodes (33): _capturing_llm(), _investment_state(), _risk_state(), test_helper_marks_empty_and_passes_through(), test_researcher_opening_has_no_phantom_opponent(), test_researcher_passes_real_opponent_argument(), test_risk_opening_has_no_phantom_opponent(), test_risk_passes_real_opponent_arguments() (+25 more)

### Community 7 - "prompts.py"
Cohesion: 0.10
Nodes (17): backtest(), AnalystType, AssetType, detect_asset_type(), filter_analysts_for_asset_type(), is_valid_ticker_input(), normalize_ticker_symbol(), parse_analysts() (+9 more)

### Community 9 - "get_capabilities"
Cohesion: 0.07
Nodes (8): test_capabilities_dataclass_is_frozen(), TestDefault, TestExactIdMatches, TestMinimaxExactMatches, TestOpenRouterDeepSeekNamespace, TestPatternMatches, get_capabilities(), ModelCapabilities

### Community 10 - "ohlcv.py"
Cohesion: 0.06
Nodes (22): _yahoo_calls(), _answered_empty(), raise_for_empty(), yf_retry(), get_balance_sheet(), get_company_profile(), get_fundamentals(), _statement() (+14 more)

### Community 11 - "test_backtest.py"
Cohesion: 0.12
Nodes (28): _config(), _fake_graph(), _log_with(), _scored(), test_a_bearish_call_that_fell_counts_as_right(), test_a_bearish_call_that_rose_counts_as_wrong(), test_a_bullish_call_is_scored_the_same_way_as_before(), test_a_cell_already_in_the_log_is_not_run_again() (+20 more)

### Community 12 - "TradingMemoryLog"
Cohesion: 0.08
Nodes (8): _FakeGraph, test_the_window_reported_is_the_one_the_outcomes_used(), test_concurrent_writers_keep_every_decision_and_outcome(), work(), test_an_unscored_decision_is_left_out_of_the_backtest_figures(), test_the_memory_log_records_review_rather_than_a_tradeable_hold(), test_the_signal_and_the_log_agree_on_the_same_decision(), TradingMemoryLog

### Community 13 - "TestDeferredReflection"
Cohesion: 0.07
Nodes (3): TestDeferredReflection, Reflector, resolve_benchmark()

### Community 14 - "test_chatgpt_provider.py"
Cohesion: 0.08
Nodes (30): ensure_api_key(), ensure_signed_in(), select_llm_provider(), _check_tier_providers(), _expired(), refuse(), _llm(), _menu() (+22 more)

### Community 15 - "select_openrouter_model"
Cohesion: 0.08
Nodes (19): ask_output_language(), _fetch_openrouter_models(), _matching_choice(), _prompt_custom_model_id(), _require_text(), select_chatgpt_model(), _select_listed_model(), _select_model() (+11 more)

### Community 16 - "test_cli_headless.py"
Cohesion: 0.10
Nodes (28): _offer_reports(), unattended_gaps(), _answer(), _Browser, _report_graph(), _selections_with_env(), test_a_closed_stdin_counts_as_no_terminal(), test_a_missing_key_without_a_terminal_names_the_variable() (+20 more)

### Community 17 - "make_log"
Cohesion: 0.06
Nodes (5): make_log(), _seed_completed(), test_a_run_does_not_wait_on_another_settlement_pass(), other_pass(), TestTradingMemoryLogCore

### Community 18 - "fetch_returns"
Cohesion: 0.07
Nodes (13): _closes(), _price_df(), test_a_close_that_is_not_a_price_is_skipped_not_scored(), test_a_longer_window_asks_for_enough_price_history(), test_the_reflection_states_the_window_it_judges(), _make_ticker(), _make_ticker(), _make_ticker() (+5 more)

### Community 19 - "test_cli_commands.py"
Cohesion: 0.08
Nodes (25): _Result, runner(), _Summary, test_a_failed_login_exits_with_the_reason(), refuse(), test_a_failure_message_with_brackets_is_printed_as_text(), refuse(), test_backtest_can_continue_an_interrupted_sweep() (+17 more)

### Community 20 - "selections.py"
Cohesion: 0.09
Nodes (18): ask_anthropic_effort(), ask_gemini_thinking_config(), ask_glm_region(), ask_minimax_region(), ask_openai_reasoning_effort(), ask_qwen_region(), get_ticker(), parse_analysis_date() (+10 more)

### Community 21 - "stocktwits.py"
Cohesion: 0.11
Nodes (7): _drop_spam(), _raise(), _stream(), test_html_entities_in_message_bodies_are_decoded(), TestStockTwitsCryptoSymbols, TestStockTwitsResilience, TestStockTwitsScreening

### Community 22 - "ohlcv.py"
Cohesion: 0.14
Nodes (11): _fake_msvcrt(), _recording_replace(), test_a_file_held_open_elsewhere_keeps_its_old_content(), test_a_replaced_file_keeps_the_usual_permissions(), test_on_windows_a_held_lock_is_reported_when_not_waiting(), test_on_windows_a_lock_that_cannot_be_taken_is_reported_not_retried_forever(), test_on_windows_the_lock_is_waited_for_while_another_writer_holds_it(), test_sec_edgar_writers_never_share_a_temp_file() (+3 more)

### Community 23 - "test_portfolio_context.py"
Cohesion: 0.09
Nodes (20): _bare_graph(), test_a_ticker_held_under_another_spelling_is_matched(), test_absent_context_is_reported_as_not_provided(), test_checkpoint_signature_changes_with_the_portfolio(), test_cli_passes_a_valid_portfolio_into_the_run(), test_cli_rejects_an_unusable_portfolio_file_before_running(), test_completed_run_clears_the_checkpoint_it_wrote(), test_create_run_state_renders_the_portfolio_once() (+12 more)

### Community 24 - "requests"
Cohesion: 0.21
Nodes (5): PolymarketFilterTests, PolymarketFormatTests, PolymarketResilienceTests, get_prediction_markets(), _request()

### Community 25 - "test_cli_memory_log.py"
Cohesion: 0.07
Nodes (11): _bare_graph(), _FakeBuffer, _FakeGraph, _NullLive, _run_cli(), test_a_run_without_checkpointing_says_nothing_about_resuming(), test_cli_run_uses_the_memory_log_like_propagate(), test_record_decision_appends_a_pending_entry() (+3 more)

### Community 27 - "get_macro_data"
Cohesion: 0.10
Nodes (8): FredConfigTests, FredFormattingTests, _capture(), FredResolutionTests, _request_stub(), _fred_today(), get_macro_data(), _resolve_series_id()

### Community 28 - "test_reddit_fallback.py"
Cohesion: 0.11
Nodes (13): _screen_out(), test_a_crypto_pair_is_fetched_from_its_communities_in_one_request(), test_a_crypto_ticker_is_searched_in_crypto_communities(), test_a_subreddit_emptied_by_screening_is_not_called_empty(), test_an_unavailable_screen_keeps_every_post_and_says_so(), test_each_subreddit_keeps_its_own_quota(), test_empty_subreddit_on_a_full_page_is_not_called_empty(), test_posts_from_an_unrequested_or_unnamed_subreddit_are_not_dropped() (+5 more)

### Community 29 - "test"
Cohesion: 0.07
Nodes (35): concurrency, cancel-in-progress, group, TZ, python-version, tz, jobs, lint (+27 more)

### Community 30 - "reddit.py"
Cohesion: 0.12
Nodes (7): _coverage_dates(), _jitter(), _posted_at(), _read_capped(), _retry_after_seconds(), _search_qs(), _within_window()

### Community 31 - "test_yahoo_rate_limit.py"
Cohesion: 0.07
Nodes (15): _rate_limited(), test_a_missing_time_zone_is_not_taken_for_an_answer(), test_a_price_request_that_fails_is_unavailable_even_when_yahoo_answers(), test_a_price_request_that_raises_is_unavailable_whether_or_not_yahoo_answers(), test_a_rate_limit_that_outlasts_the_retries_is_reported_as_one(), test_a_request_that_yfinance_would_swallow_is_unavailable(), test_a_snapshot_with_no_rows_is_reported_not_raised(), load() (+7 more)

### Community 32 - "GoogleClient"
Cohesion: 0.09
Nodes (13): TestGoogleApiKeyStandardization, _captured_kwargs(), test_a_gemini_call_times_out_like_the_other_providers(), test_flash_38_keeps_supported_levels(), test_flash_38_remaps_minimal_to_low(), test_flash_passes_thinking_level_through(), test_latest_alias_remaps_minimal_to_low(), test_no_thinking_level_is_omitted() (+5 more)

### Community 33 - "OpenAIClient"
Cohesion: 0.06
Nodes (20): _effort_on(), test_non_reasoning_model_drops_effort(), test_reasoning_model_receives_effort(), test_supports_reasoning_effort(), NativeBaseUrlTests, ResponsesApiSelectionTests, _Recorder, _signed_in_provider() (+12 more)

### Community 34 - "chatgpt_auth.py"
Cohesion: 0.14
Nodes (10): _b64url(), _b64url_decode(), ChatGPTAuthError, ChatGPTUnreachable, _due(), _oauth_error(), _refresh(), _signing_keys() (+2 more)

### Community 35 - "TradingAgentsGraph"
Cohesion: 0.06
Nodes (5): test_a_failed_reflection_leaves_the_entry_pending_and_lets_the_run_start(), test_the_holding_window_is_configurable(), run_config_context(), TradingAgentsGraph, _validate_trade_date()

### Community 36 - "tools.py"
Cohesion: 0.14
Nodes (11): get_balance_sheet(), get_cashflow(), get_fundamentals(), get_global_news(), get_income_statement(), get_indicators(), get_insider_transactions(), get_macro_indicators() (+3 more)

### Community 37 - "test_rating_integrity.py"
Cohesion: 0.05
Nodes (19): test_a_decision_prompt_states_the_shape_of_its_answer(), test_a_quoted_rating_in_a_list_table_or_quote_is_not_the_decision(), test_a_rating_argued_against_is_not_read_as_the_decision(), test_a_rating_someone_else_gave_does_not_become_the_decision(), test_a_rating_the_text_quotes_does_not_replace_the_decision(), test_a_rating_word_without_a_label_is_not_read_as_the_call(), test_a_refusal_has_no_rating_and_is_not_defaulted(), test_a_state_without_the_typed_rating_reads_it_from_the_decision() (+11 more)

### Community 38 - "test_ollama_base_url.py"
Cohesion: 0.10
Nodes (18): confirm_ollama_endpoint(), _base_url(), _client_module(), _console_out(), test_client_get_llm_picks_up_env(), test_confirm_endpoint_marks_env_origin(), test_confirm_endpoint_quiet_on_local_no_port(), test_confirm_endpoint_shows_default() (+10 more)

### Community 39 - "ResearchPlan"
Cohesion: 0.23
Nodes (8): _make_rm_state(), _structured_rm_llm(), TestRenderResearchPlan, TestResearchManagerAgent, create_research_manager(), research_manager_node(), render_research_plan(), ResearchPlan

### Community 40 - "VendorUnavailableError"
Cohesion: 0.06
Nodes (29): test_an_unreachable_yahoo_is_not_reported_as_a_symbol_without_insider_data(), _dates_after(), _insider_frame(), test_a_current_run_is_not_cluttered_with_a_vintage_note(), test_a_historical_run_gets_the_current_name_only_as_an_identifier(), test_a_historical_run_is_not_told_todays_date(), test_a_yfinance_failure_is_a_vendor_error_not_a_report(), test_a_yfinance_news_failure_is_a_vendor_error_not_a_report() (+21 more)

### Community 41 - "TraderProposal"
Cohesion: 0.09
Nodes (13): test_a_field_the_model_did_not_give_says_so(), test_a_price_that_is_a_number_survives(), test_a_price_written_as_a_range_drops_only_that_field(), test_conflict_alone_is_not_a_hold_trigger(), test_invoke_structured_falls_back_when_result_is_none(), test_the_trader_names_the_levels_it_did_not_give(), TestNullishFloatCoercion, TestRenderTraderProposal (+5 more)

### Community 42 - "fetch_reddit_posts"
Cohesion: 0.15
Nodes (19): _epoch(), _JsonResp, _msg(), test_in_window_bounds_and_exclusive_upper(), test_in_window_undated_excluded_in_backtest_kept_live(), test_reddit_covered_but_empty_window_is_a_real_absence(), test_reddit_empty_feed_for_an_old_window_is_unavailable(), test_reddit_full_page_does_not_vouch_for_older_days() (+11 more)

### Community 43 - "BaseLLMClient"
Cohesion: 0.24
Nodes (10): _captured(), _config(), test_a_tier_on_another_provider_gets_that_provider_s_settings_and_not_the_main_url(), test_a_tier_url_is_used_for_that_tier_only(), test_a_tier_without_its_own_provider_uses_the_run_s(), test_the_run_settings_and_report_name_each_tier_s_provider(), test_the_tier_settings_are_read_from_the_environment(), create_tier_client() (+2 more)

### Community 44 - "build"
Cohesion: 0.07
Nodes (29): env, name, permissions, runs-on, steps, concurrency, cancel-in-progress, group (+21 more)

### Community 45 - "create_sentiment_analyst"
Cohesion: 0.11
Nodes (11): _make_sentiment_state(), _structured_sentiment_llm(), TestRenderSentimentReport, TestSentimentAnalystAgent, _build_system_message(), create_sentiment_analyst(), sentiment_analyst_node(), _seven_days_back() (+3 more)

### Community 46 - "openai_client.py"
Cohesion: 0.11
Nodes (8): test_legacy_ids_stay_valid_without_being_offered(), BaseLLMClient, normalize_content(), _bedrock_class(), invoke(), BedrockClient, get_known_models(), validate_model()

### Community 47 - "test_cli_prefs.py"
Cohesion: 0.11
Nodes (19): load_last_run(), sanitize(), save_last_run(), _llm_provider_table(), get_user_selections(), _answer_every_prompt(), test_a_corrupt_file_degrades_to_no_memory(), test_a_custom_language_is_remembered_without_breaking_the_next_run() (+11 more)

### Community 48 - "Propagator"
Cohesion: 0.15
Nodes (4): TestPortfolioManagerInjection, InvestDebateState, RiskDebateState, Propagator

### Community 49 - "normalize_symbol"
Cohesion: 0.13
Nodes (5): TestCryptoBase, TestNormalizeSymbol, crypto_base(), _normalize_crypto(), normalize_symbol()

### Community 50 - "test_alpha_vantage_hardening.py"
Cohesion: 0.06
Nodes (33): _FakeResponse, _patched_get(), fake_get(), test_a_rejected_request_is_unavailable_not_data(), test_an_indicator_this_vendor_lacks_lets_the_next_one_serve_it(), test_empty_body_still_passes_through(), test_fundamentals_no_curr_date_passes_through(), test_global_news_omitted_optionals_use_the_configured_defaults() (+25 more)

### Community 51 - "test_api_key_env.py"
Cohesion: 0.10
Nodes (13): _prompt_key(), test_case_insensitive_lookup(), test_ensure_api_key_prompts_and_writes_to_env(), test_ensure_api_key_updates_existing_env_file(), test_ensure_api_key_user_cancels_returns_none(), test_every_select_llm_provider_choice_has_an_entry(), test_existing_key_file_is_tightened_before_writing(), test_known_providers_resolve() (+5 more)

### Community 52 - "create_llm_client"
Cohesion: 0.09
Nodes (19): resolve_backend_url(), _capture_kwargs(), test_bearer_token_passed_as_api_key(), test_bedrock_any_model_and_no_key_env(), test_construction_when_extra_installed(), test_factory_routes_bedrock(), test_helpful_error_when_langchain_aws_absent(), test_no_bearer_token_omits_api_key() (+11 more)

### Community 53 - "test_env_overrides.py"
Cohesion: 0.14
Nodes (11): _config_with_env(), test_bool_coercion(), test_empty_env_value_is_passthrough(), test_empty_path_value_keeps_the_default_path(), test_int_coercion(), test_invalid_bool_raises(), test_no_env_uses_built_in_defaults(), test_reasoning_effort_defaults_to_none() (+3 more)

### Community 54 - "_fetch_subreddit_rss"
Cohesion: 0.14
Nodes (7): _atom_resp(), _raise(), _resp(), TestChunkedTransferErrorsHandled, TestRss429Backoff, TestRssParsing, _fetch_subreddit_rss()

### Community 55 - "tradingagents-ollama"
Cohesion: 0.08
Nodes (23): image, profiles, volumes, services, ollama, tradingagents, tradingagents-ollama, build (+15 more)

### Community 56 - "test_chatgpt_auth.py"
Cohesion: 0.23
Nodes (17): _renewal(), _signed_in(), test_a_fresh_token_is_used_without_asking_openai(), test_a_refused_renewal_asks_to_sign_in_again_and_keeps_the_file(), test_a_renewal_for_another_account_is_refused(), test_a_temporary_failure_after_expiry_says_to_try_again_not_to_sign_in(), test_a_temporary_failure_keeps_a_token_that_still_works(), test_a_token_near_expiry_is_renewed_with_the_stored_refresh_token() (+9 more)

### Community 57 - "ConditionalLogic"
Cohesion: 0.13
Nodes (10): _debate_state(), _state(), test_debate_path_map_covers_full_router_range(), test_debate_router_return_always_routable(), test_path_map_covers_full_router_range(), test_router_return_always_routable(), test_router_terminates_at_round_limit(), AgentState (+2 more)

### Community 58 - "pytest"
Cohesion: 0.08
Nodes (10): test_get_yfin_requests_inclusive_end(), test_load_ohlcv_requests_inclusive_end(), test_error_without_the_key_in_its_message_still_drops_the_request(), test_a_current_run_is_still_served_yahoo_statements(), test_alpha_vantage_withholds_insider_trades_from_a_past_run_without_asking(), test_alpha_vantage_withholds_statements_from_a_past_run_without_asking(), test_statements_come_from_sec_edgar_first_by_default(), test_yahoo_withholds_insider_trades_from_a_past_run_without_asking() (+2 more)

### Community 59 - "test_tool_date_enforcement.py"
Cohesion: 0.16
Nodes (17): _run(), _State, test_a_start_date_that_is_not_a_date_is_sent_back_to_the_model(), test_a_tool_serves_the_run_instrument_whatever_the_model_passes(), test_a_window_whose_start_is_not_a_date_is_refused(), test_as_of_takes_the_earlier_date(), test_as_of_window(), test_as_of_without_a_trade_date_passes_the_request_through() (+9 more)

### Community 60 - "display.py"
Cohesion: 0.13
Nodes (3): format_tokens(), format_tool_args(), update_display()

### Community 61 - "re"
Cohesion: 0.05
Nodes (50): _fail_download(), _load(), _stamp(), test_a_download_from_an_earlier_day_is_not_fresh(), test_current_day_cache_past_ttl_is_not_fresh(), test_historical_request_uses_todays_cache_past_the_ttl(), test_load_ohlcv_refetches_stale_same_day_cache(), test_load_ohlcv_reuses_fresh_same_day_cache() (+42 more)

### Community 62 - "checkpointer.py"
Cohesion: 0.16
Nodes (5): checkpoint_step(), clear_all_checkpoints(), clear_checkpoint(), _db_path(), get_checkpointer()

### Community 63 - "test_fundamentals_lookahead.py"
Cohesion: 0.15
Nodes (6): _av(), TestAlphaVantageHistoricalRun, TestLiveRunUnchanged, TestNoUsableFieldsStillRaises, TestYFinanceHistoricalRun, _yf()

### Community 64 - "build_llm_kwargs"
Cohesion: 0.20
Nodes (15): _config_with_env(), test_coerce_accepts_positive_ints_and_numeric_strings(), test_coerce_rejects_booleans(), test_coerce_rejects_non_integers(), test_coerce_rejects_non_positive(), test_default_is_none(), test_env_override_sets_config(), test_env_string_is_coerced() (+7 more)

### Community 65 - "VendorRoutingTests"
Cohesion: 0.20
Nodes (7): _no_data(), _raises(), _reset_config(), _returns(), impl(), VendorRoutingTests, route_to_vendor()

### Community 66 - "AnthropicClient"
Cohesion: 0.18
Nodes (3): _capture_kwargs(), TestEffortGate, AnthropicClient

### Community 67 - "resolve_instrument_identity"
Cohesion: 0.06
Nodes (14): [0.5.2] — 2026-09-29, Added, Contributors, Fixed, Models, Upgrading from 0.5.1, BuildInstrumentContextTests, GetInstrumentContextFromStateTests (+6 more)

### Community 68 - "TradingAgents: Multi-Agents LLM Financial Trading Framework"
Cohesion: 0.18
Nodes (9): Checkpoint resume, Citation, Contributing, Evaluating decisions over time, Memory log, News, Persistence and Recovery, Reproducibility (+1 more)

### Community 69 - "test_post_screen.py"
Cohesion: 0.07
Nodes (37): _Calls, jev(), _ok(), post(), _post_answers(), fake_post(), _Response, test_a_base_url_without_a_key_does_not_turn_screening_on() (+29 more)

### Community 70 - "[0.4.0] — 2026-08-31"
Cohesion: 0.50
Nodes (4): [0.4.0] — 2026-08-31, Added, Contributors, Fixed

### Community 72 - "test_cli_config_precedence.py"
Cohesion: 0.18
Nodes (9): _build_run_config(), test_a_half_set_round_count_says_which_value_won(), test_a_tier_s_thinking_setting_survives_a_main_provider_that_has_none(), test_checkpoint_flag_overrides_env(), test_checkpoint_none_preserves_env_default(), test_env_round_counts_win_over_selection(), test_glm_resolves_to_the_endpoint_its_key_belongs_to(), test_partial_env_only_overrides_that_count() (+1 more)

### Community 73 - "test_memory_log.py"
Cohesion: 0.10
Nodes (9): prompt(), _make_pm_state(), _structured_pm_llm(), create_portfolio_manager(), portfolio_manager_node(), render_pm_decision(), bind_structured(), invoke_structured() (+1 more)

### Community 74 - "test_llm_max_retries.py"
Cohesion: 0.24
Nodes (12): _config_with_env(), test_coerce_accepts_non_negative_ints_and_numeric_strings(), test_coerce_rejects_booleans(), test_coerce_rejects_negative(), test_coerce_rejects_non_integers(), test_default_is_none(), test_env_override_sets_config(), test_forwarded_across_providers() (+4 more)

### Community 75 - "settle_pending"
Cohesion: 0.09
Nodes (6): test_any_failure_to_price_a_decision_is_reported(), TestSettleAll, TestSettlementOnceAndDurably, down(), settle_all_pending(), settle_pending()

### Community 76 - "test_model_validation.py"
Cohesion: 0.20
Nodes (5): DummyLLMClient, ModelValidationTests, test_a_retired_model_id_still_runs_without_a_warning(), test_an_explicit_alias_of_a_listed_model_is_known(), test_every_provider_lets_you_name_your_own_model()

### Community 77 - "get_global_news_yfinance"
Cohesion: 0.14
Nodes (9): _epoch(), test_global_news_does_not_infer_coverage_from_a_stale_search_hit(), test_global_news_empty_after_filter_is_informative(), test_global_news_empty_feed_for_a_past_window_is_unavailable(), test_global_news_future_flat_article_excluded(), test_out_of_window_articles_do_not_consume_the_article_budget(), test_the_article_limit_still_caps_what_is_returned(), _format_articles() (+1 more)

### Community 78 - "test_cli_display.py"
Cohesion: 0.18
Nodes (9): update_analyst_statuses(), _bare_graph(), _state(), test_a_message_that_reads_like_a_python_value_is_still_text(), test_every_selected_analyst_is_in_progress_until_its_report_lands(), test_the_live_display_does_not_scroll_the_terminal(), test_the_other_shapes_are_unchanged(), test_the_state_log_keeps_non_ascii_readable() (+1 more)

### Community 79 - "conftest.py"
Cohesion: 0.08
Nodes (11): _at_a_terminal(), _blank_settings_overlay(), _dummy_api_keys(), _isolate_config(), _no_network(), _own_cli_prefs(), _own_file_locations(), test_a_test_cannot_reach_the_network() (+3 more)

### Community 80 - "RouterHandlesBaseTypesTests"
Cohesion: 0.15
Nodes (6): RouterHandlesBaseTypesTests, not_covered(), throttled(), _unconfigured(), _throttled(), _unconfigured()

### Community 82 - "stocktwits.py"
Cohesion: 0.21
Nodes (5): _body(), _created_at(), fetch_stocktwits_messages(), _stocktwits_symbol(), _within_window()

### Community 83 - "_graph"
Cohesion: 0.15
Nodes (12): _graph(), ScriptedModel, test_a_debug_run_prints_the_analysts_work_and_reaches_the_same_decision(), test_a_full_run_reaches_a_logged_decision(), test_a_graph_reused_across_runs_keeps_no_run_state(), test_a_streamed_run_reads_its_own_graph_config(), test_a_tool_limit_the_recursion_limit_cannot_hold_is_refused(), test_an_interrupted_run_resumes_from_its_checkpoint() (+4 more)

### Community 84 - "updates.py"
Cohesion: 0.12
Nodes (10): enabled(), _get_json(), parse_notices(), _plain(), read_cache(), refresh(), start_background_refresh(), summary_of() (+2 more)

### Community 85 - "test_structured_agent_prompts.py"
Cohesion: 0.19
Nodes (12): _capturing_llm(), _prompt_text(), test_constraint_text_is_unambiguous(), test_portfolio_manager_prompt_states_constraint(), test_research_manager_prompt_states_constraint(), test_sentiment_prompt_states_constraint(), test_the_sentiment_prompt_names_the_subreddits_searched(), test_tool_using_analysts_keep_their_date_guidance() (+4 more)

### Community 86 - "yahoo/__init__.py"
Cohesion: 0.16
Nodes (4): _ohlcv(), test_cleaning_a_frame_with_undated_rows_writes_to_its_own_copy(), TestCleanDataframeAcrossVersions, TestEnsureDateColumn

### Community 87 - "attributes"
Cohesion: 0.12
Nodes (15): description, label, options, placeholder, render, value, body, attributes (+7 more)

### Community 88 - "attributes"
Cohesion: 0.12
Nodes (15): description, label, multiple, options, placeholder, value, body, attributes (+7 more)

### Community 90 - "test_checkpoint_lifecycle.py"
Cohesion: 0.23
Nodes (10): _bare_graph(), _node_a(), _node_b(), _State, test_begin_returns_thread_id_and_recompiles(), test_checkpoint_input_is_none_only_when_resuming(), test_clearing_removes_the_database_sidecars(), test_cli_style_usage_saves_then_resumes() (+2 more)

### Community 91 - "test_minimax.py"
Cohesion: 0.20
Nodes (4): _client(), TestMinimaxReasoningSplit, TestMinimaxStructuredOutputDispatch, _Pick

### Community 92 - "sign_in"
Cohesion: 0.27
Nodes (14): _id_token(), _nonce_of(), _paster(), read_line(), test_a_network_failure_while_signing_in_is_reported_not_raised_raw(), test_a_sign_in_without_plan_usage_is_refused(), test_an_answer_for_another_sign_in_attempt_is_ignored(), test_another_account_cannot_replace_the_signed_in_one() (+6 more)

### Community 93 - "Changelog"
Cohesion: 0.15
Nodes (13): [0.1.0] — 2025-06-05, [0.1.1] — 2025-06-07, [0.2.3] — 2026-03-29, [0.3.1] — 2026-07-05, Added, Added, Added, Changed (+5 more)

### Community 94 - "test_llm_429_resilience.py"
Cohesion: 0.20
Nodes (6): _chat(), test_every_429_fails_after_the_retry_cap_with_a_clear_message(), test_one_429_with_retry_after_then_200_succeeds(), test_the_clear_message_never_carries_the_api_key(), _transport(), LLMCapacityError

### Community 95 - "[0.5.0] — 2026-09-18"
Cohesion: 0.25
Nodes (8): [0.5.0] — 2026-09-18, Changed, CLI, Contributors, Data sources, Decisions and evaluation, Models, Point-in-time and honest attribution

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

### Community 103 - "[0.2.1] — 2026-03-15"
Cohesion: 0.33
Nodes (6): [0.2.1] — 2026-03-15, Added, Contributors, Fixed, Removed, Security

### Community 104 - "DeepSeekChatOpenAI"
Cohesion: 0.20
Nodes (4): TestDeepSeekLiveStructuredOutput, _Pick, _Sample, DeepSeekChatOpenAI

### Community 105 - "test_fundamentals_units.py"
Cohesion: 0.33
Nodes (7): _fundamentals(), test_a_figure_with_no_stated_currency_is_printed_bare(), test_an_absent_percent_field_is_left_out(), test_an_adr_quotes_in_dollars_and_reports_in_its_home_currency(), test_each_money_figure_carries_the_currency_it_is_in(), test_income_figures_without_a_stated_reporting_currency_are_printed_bare(), test_percent_fields_carry_their_unit_and_fractions_are_unchanged()

### Community 107 - "os"
Cohesion: 0.11
Nodes (10): TestKeyKeptOutOfErrors, _call(), _response(), test_a_passthrough_status_is_returned_for_the_caller(), test_nothing_that_holds_the_url_travels_with_the_error(), test_the_key_is_masked_in_the_error(), get_scrubbed(), FredNotConfiguredError (+2 more)

### Community 108 - "[0.2.4] — 2026-04-25"
Cohesion: 0.33
Nodes (6): [0.2.4] — 2026-04-25, Added, Changed, Contributors, Fixed, Removed

### Community 109 - ".save_reports"
Cohesion: 0.10
Nodes (14): [0.3.0] — 2026-06-22, [0.6.0] — 2026-10-03, Added, Added, Changed, Contributors, Contributors, Fixed (+6 more)

### Community 110 - "run.py"
Cohesion: 0.13
Nodes (6): display_complete_report(), _graphical_browser(), _open_page(), _run_directory(), _yes(), test_the_run_directory_cannot_escape_the_results_directory()

### Community 112 - "test_memory_pointintime.py"
Cohesion: 0.33
Nodes (8): _log(), _resolve(), test_as_of_excludes_lessons_resolved_after_the_run_date(), test_cross_ticker_lessons_are_also_gated(), test_legacy_entry_without_resolution_date_excluded_in_backtest(), test_memory_as_of_gates_historical_but_not_live(), test_no_as_of_is_unfiltered_live_behavior(), test_resolution_date_is_stored_and_parsed()

### Community 113 - "AnalystWallTimeTracker"
Cohesion: 0.38
Nodes (4): AnalystWallTimeTracker, sync_analyst_tracker_from_chunk(), AnalystWallTimeTrackerTests, AnalystExecutionPlan

### Community 114 - "backtest.py"
Cohesion: 0.15
Nodes (10): Highlights, Upgrading from 0.5.0, test_a_backtest_result_is_summarized_directly(), test_a_result_whose_cells_all_failed_summarizes_as_empty(), _alpha(), BacktestResult, BacktestSummary, _canonical() (+2 more)

### Community 115 - "test_checkpoint_resume.py"
Cohesion: 0.17
Nodes (5): _build_graph(), _node_a(), _node_b(), _SimpleState, TestCheckpointResume

### Community 116 - "set_config"
Cohesion: 0.19
Nodes (6): DataflowsConfigIsolationTests, test_a_yahoo_news_outage_moves_to_the_next_configured_vendor(), get_config(), initialize_config(), _merge(), set_config()

### Community 117 - "Installation and CLI"
Cohesion: 0.29
Nodes (7): CLI Usage, Docker, Installation, Installation and CLI, Markets and tickers, Rate-limited endpoints (429), Required APIs

### Community 118 - "test_cli_env_skip.py"
Cohesion: 0.19
Nodes (5): provider_default_url(), TestCliSkipsPromptsFromEnv, TestProviderDefaultUrl, TestReasoningEffortSkippedFromEnv, TestResearchDepthSkippedFromEnv

### Community 119 - "test_cli_updates.py"
Cohesion: 0.16
Nodes (13): upgrade_command(), _dist(), _response(), test_a_check_records_the_latest_release_and_notices(), get(), test_a_failed_check_keeps_what_was_known_and_waits_a_day(), test_a_uv_git_install_is_upgraded_with_uv(), test_an_unattended_run_contacts_no_server() (+5 more)

### Community 120 - "VendorError"
Cohesion: 0.18
Nodes (6): test_an_indicator_that_could_not_be_read_is_not_shown_as_a_blank_value(), HierarchyTests, VendorError, VendorNotConfiguredError, get_stock_stats_indicators_window(), get_stockstats_indicator()

### Community 124 - "[0.2.5] — 2026-05-11"
Cohesion: 0.40
Nodes (5): [0.2.5] — 2026-05-11, Added, Changed, Fixed, Security

### Community 126 - "_analyst_graph"
Cohesion: 0.28
Nodes (7): handler(), _analyst_graph(), calls(), more_or_wrap_up(), rounds(), wrap_up(), _tools_or_done()

### Community 129 - "test_opencode_session.py"
Cohesion: 0.19
Nodes (9): test_get_llm_attaches_headers_for_opencode(), test_get_llm_no_headers_elsewhere(), test_headers_only_for_opencode(), test_opencode_endpoint_detection(), test_session_id_env_override(), test_session_id_stable_within_process(), is_opencode_endpoint(), request_headers() (+1 more)

### Community 130 - "[0.5.1] — 2026-09-24"
Cohesion: 0.40
Nodes (5): [0.5.1] — 2026-09-24, Added, Contributors, Fixed, Models

### Community 131 - "run_analysis"
Cohesion: 0.20
Nodes (8): create_layout(), update_research_team_status(), _announce_checkpoint_state(), run_analysis(), save_message_decorator(), wrapper(), save_report_section_decorator(), save_tool_call_decorator()

### Community 132 - "contact_links"
Cohesion: 0.33
Nodes (5): blank_issues_enabled, contact_links, about, name, url

### Community 133 - "test_news_analyst_prompt.py"
Cohesion: 0.32
Nodes (3): test_get_news_takes_the_window_not_a_query(), test_news_prompt_matches_get_news_signature(), get_news()

### Community 134 - "LoopingModel"
Cohesion: 0.33
Nodes (3): LoopingModel, test_an_analyst_that_keeps_calling_tools_writes_its_report_at_the_limit(), test_the_last_turn_is_offered_no_tools_and_reads_its_tool_results_as_text()

### Community 135 - "[0.7.0] — 2026-10-16"
Cohesion: 0.40
Nodes (5): [0.7.0] — 2026-10-16, Added, Contributors, Fixed, Upgrading from 0.6.0

### Community 136 - "build_verified_market_snapshot"
Cohesion: 0.26
Nodes (4): _sample_ohlcv(), TestTool, TestVerifiedSnapshot, build_verified_market_snapshot()

### Community 137 - "test_chatgpt_auth.py"
Cohesion: 0.12
Nodes (12): _b64(), FakeOpenAI, home(), _jwks(), openai(), _Response, _status(), test_a_genuine_id_token_is_accepted() (+4 more)

### Community 138 - "TradingAgents Framework"
Cohesion: 0.40
Nodes (5): Analyst Team, Researcher Team, Risk Management and Portfolio Manager, Trader Agent, TradingAgents Framework

### Community 140 - "sign_out"
Cohesion: 0.20
Nodes (9): test_signing_out_revokes_the_sign_in_and_keeps_only_the_host_id(), test_signing_out_while_openai_is_unreachable_still_forgets_the_sign_in(), credential(), _host_id(), _read(), _revoke(), sign_out(), signed_in_as() (+1 more)

### Community 143 - "coverage_gap"
Cohesion: 0.29
Nodes (4): test_coverage_gap_future_window_is_unavailable(), coverage_gap(), _parse(), to_utc()

### Community 144 - "locked"
Cohesion: 0.40
Nodes (3): test_a_lock_held_elsewhere_is_reported_when_not_waiting(), holder(), locked()

### Community 146 - "FredRoutingTests"
Cohesion: 0.17
Nodes (4): FredRoutingTests, _unconfigured(), PolymarketRoutingTests, get_category_for_method()

### Community 153 - "[0.2.0] — 2026-02-04"
Cohesion: 0.40
Nodes (5): [0.2.0] — 2026-02-04, Added, Changed, Contributors, Fixed

### Community 154 - "TradingAgents Package"
Cohesion: 0.40
Nodes (5): Current holdings, Fundamentals as filed, Implementation Details, Python Usage, TradingAgents Package

### Community 155 - "_applies"
Cohesion: 0.40
Nodes (3): _applies(), _version(), test_a_notice_shows_through_its_bounds_and_date_and_hides_when_they_cannot_be_read()

### Community 157 - "build_default_config"
Cohesion: 0.20
Nodes (5): test_invalid_int_raises(), test_dependency_wiring_goes_the_same_route(), _apply_env_overrides(), build_default_config(), _coerce()

### Community 159 - "create_trader"
Cohesion: 0.44
Nodes (4): _make_trader_state(), _structured_trader_llm(), TestTraderAgent, create_trader()

### Community 160 - "_extract_article_data"
Cohesion: 0.29
Nodes (5): test_a_flat_article_with_a_null_field_is_read_with_its_default(), test_an_article_with_a_null_field_is_read_with_its_default(), test_coverage_gap_boundaries(), test_flat_article_publish_time_is_parsed(), _extract_article_data()

### Community 162 - "get_verified_market_snapshot"
Cohesion: 0.29
Nodes (3): get_verified_market_snapshot(), no_data_available(), vendor_unavailable()

### Community 163 - "[0.2.2] — 2026-03-22"
Cohesion: 0.40
Nodes (5): [0.2.2] — 2026-03-22, Added, Changed, Contributors, Fixed

## Knowledge Gaps
- **1 isolated node(s):** `tradingagents`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1298 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **34 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `TradingAgentsGraph` connect `TradingAgentsGraph` to `test_dataflows_config.py`, `run_analysis`, `test_backtest.py`, `TestDeferredReflection`, `test_cli_headless.py`, `test_portfolio_context.py`, `test_cli_memory_log.py`, `TradingAgents Package`, `thread_id`, `BaseLLMClient`, `Propagator`, `ConditionalLogic`, `test_tool_date_enforcement.py`, `re`, `checkpointer.py`, `resolve_instrument_identity`, `test_cli_display.py`, `_graph`, `test_checkpoint_lifecycle.py`, `.save_reports`, `run.py`, `TestLegacyRemoval`, `test_memory_pointintime.py`, `backtest.py`, `test_checkpoint_resume.py`?**
  _High betweenness centrality (0.046) - this node is a cross-community bridge._
- **Are the 26 inferred relationships involving `TradingAgentsGraph` (e.g. with `Python Usage` and `_bare_graph()`) actually correct?**
  _`TradingAgentsGraph` has 26 INFERRED edges - model-reasoned connections that need verification._
- **What connects `tradingagents` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `NoMarketDataError` be split into smaller, more focused modules?**
  _Cohesion score 0.0773109243697479 - nodes in this community are weakly interconnected._
- **Why does `TradingMemoryLog` connect `TradingMemoryLog` to `TradingAgentsGraph`, `test_rating_integrity.py`, `test_backtest.py`, `Propagator`, `make_log`, `backtest.py`, `test_memory_pointintime.py`, `locked`, `test_portfolio_context.py`, `test_cli_memory_log.py`, `ConditionalLogic`?**
  _High betweenness centrality (0.043) - this node is a cross-community bridge._
- **Are the 22 inferred relationships involving `NoMarketDataError` (e.g. with `TestNoUsableFieldsStillRaises` and `TestLoadOhlcvNoPoison`) actually correct?**
  _`NoMarketDataError` has 22 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_sec_edgar.py` be split into smaller, more focused modules?**
  _Cohesion score 0.055900621118012424 - nodes in this community are weakly interconnected._