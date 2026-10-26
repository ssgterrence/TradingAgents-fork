# Graph Report - TradingAgents-fork  (2026-10-26)

## Corpus Check
- 199 files · ~129,981 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 6, .example 2, .lock 1)

## Summary
- 3611 nodes · 8339 edges · 166 communities (134 shown, 32 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 460 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ddda10e6`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- set_config
- test_ohlcv_latest_bar.py
- test_cli_updates.py
- rating.py
- test_sec_edgar.py
- test_news_lookahead.py
- get_instrument_context_from_state
- test_cli_symbol_handling.py
- test_alpha_vantage_hardening.py
- get_capabilities
- router.py
- select_openrouter_model
- TradingMemoryLog
- TestDeferredReflection
- test_chatgpt_provider.py
- backtest.py
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
- _resp
- get_macro_data
- test_reddit_fallback.py
- test
- reddit.py
- sign_in
- GoogleClient
- OpenAIClient
- chatgpt_auth.py
- TradingAgentsGraph
- test_tool_date_enforcement.py
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
- sentiment_analyst.py
- test_api_key_env.py
- create_llm_client
- test_env_overrides.py
- Settlement
- tradingagents-ollama
- test_chatgpt_auth.py
- ConditionalLogic
- test_tool_date_enforcement.py
- parse_rating
- run_analysis
- re
- checkpointer.py
- test_fundamentals_lookahead.py
- build_llm_kwargs
- HierarchyTests
- AnthropicClient
- build_instrument_context
- TradingAgents: Multi-Agents LLM Financial Trading Framework
- test_post_screen.py
- test_provider_registry.py
- StatsCallbackHandler
- test_cli_config_precedence.py
- test_checkpoint_resume.py
- test_llm_max_retries.py
- settle_pending
- test_model_validation.py
- os
- test_cli_symbol_handling.py
- conftest.py
- test_dataflows_config.py
- run.py
- stocktwits.py
- _graph
- test_ohlcv_date_column.py
- test_structured_agent_prompts.py
- NoMarketDataError
- attributes
- attributes
- .warn_if_unknown_model
- test_suite_isolation.py
- test_minimax.py
- run_backtest
- Changelog
- test_llm_429_resilience.py
- [0.5.0] — 2026-09-18
- locked
- test_deepseek_reasoning.py
- body
- test_a_report_that_was_never_produced_says_so
- test_graph_end_to_end.py
- AnalystWallTimeTracker
- safe_ticker_component
- [0.2.1] — 2026-03-15
- test_checkpoint_lifecycle.py
- test_fundamentals_units.py
- Build with TypeSafe
- pytest
- [0.2.4] — 2026-04-25
- .save_reports
- display.py
- TestLegacyRemoval
- test_memory_pointintime.py
- [0.2.3] — 2026-03-29
- run_analysis
- [0.3.0] — 2026-06-22
- test_debate_opening.py
- Installation and CLI
- MessageBuffer
- write_report_tree
- os
- test_i18n_coverage.py
- test_the_cli_says_when_a_run_produced_no_usable_rating
- login
- [0.2.5] — 2026-05-11
- _analyst_graph
- os
- test_layering.py
- TestStructuredOutputCapabilityDispatch
- test_opencode_session.py
- _fact
- DeepSeekChatOpenAI
- contact_links
- test_news_analyst_prompt.py
- LoopingModel
- [0.7.0] — 2026-10-16
- thread_id
- FakeOpenAI
- NormalizedChatOpenAI
- StaleGuardRoutingTests
- AGENTS.md
- _Callback
- build_default_config
- _validated_claims
- test_a_settlement_failure_is_noted_and_the_run_goes_on
- TestDeepSeekReasoningContent
- tradingagents
- [0.2.0] — 2026-02-04
- TestCryptoSearchTerm
- crypto_base
- TradingAgents Package
- _FakeGraph
- build_analyst_execution_plan
- _Unreachable
- test_get_yfin_requests_inclusive_end
- test_temperature_config.py
- extract_content_string
- [0.2.2] — 2026-03-22
- _identity
- _fake_graph

## God Nodes (most connected - your core abstractions)
1. `TradingAgentsGraph` - 68 edges
2. `NoMarketDataError` - 59 edges
3. `set_config()` - 54 edges
4. `make_log()` - 49 edges
5. `TradingMemoryLog` - 47 edges
6. `VendorUnavailableError` - 47 edges
7. `get_instrument_context_from_state()` - 44 edges
8. `route_to_vendor()` - 43 edges
9. `get_language_instruction()` - 42 edges
10. `normalize_symbol()` - 39 edges

## Surprising Connections (you probably didn't know these)
- `Python Usage` --references--> `TradingAgentsGraph`  [INFERRED]
  README.md → tradingagents/graph/trading_graph.py
- `Changed` --references--> `VendorError`  [INFERRED]
  CHANGELOG.md → tradingagents/dataflows/errors.py
- `Fixed` --references--> `get_indicators()`  [INFERRED]
  CHANGELOG.md → tradingagents/agents/tools.py
- `Fixed` --references--> `set_config()`  [INFERRED]
  CHANGELOG.md → tradingagents/dataflows/config.py
- `Evaluating decisions over time` --references--> `run_backtest()`  [INFERRED]
  README.md → tradingagents/backtest.py

## Import Cycles
- None detected.

## Communities (166 total, 32 thin omitted)

### Community 0 - "set_config"
Cohesion: 0.08
Nodes (11): DataflowsConfigIsolationTests, _no_data(), _raises(), _reset_config(), _returns(), impl(), VendorRoutingTests, get_config() (+3 more)

### Community 1 - "test_ohlcv_latest_bar.py"
Cohesion: 0.06
Nodes (32): _fail_download(), _load(), _stamp(), test_a_download_from_an_earlier_day_is_not_fresh(), test_current_day_cache_past_ttl_is_not_fresh(), test_historical_request_uses_todays_cache_past_the_ttl(), test_load_ohlcv_refetches_stale_same_day_cache(), test_load_ohlcv_reuses_fresh_same_day_cache() (+24 more)

### Community 2 - "test_cli_updates.py"
Cohesion: 0.07
Nodes (42): _applies(), due(), enabled(), _get_json(), messages(), parse_notices(), _plain(), read_cache() (+34 more)

### Community 3 - "rating.py"
Cohesion: 0.11
Nodes (11): is_review(), run_rating(), _chain(), _fields(), _group(), _markdown(), _render_agent_text(), render_report() (+3 more)

### Community 4 - "test_sec_edgar.py"
Cohesion: 0.11
Nodes (16): _no_network_or_cache(), test_a_filer_with_no_usable_facts_reads_differently_from_a_non_filer(), test_a_line_the_filer_does_not_tag_is_named_unavailable(), test_a_non_filer_is_reported_as_such_not_as_missing_data(), test_a_per_share_figure_keeps_its_own_unit(), test_a_period_that_ended_but_was_not_filed_yet_is_not_served(), test_a_restated_figure_reads_as_it_did_at_the_time(), test_a_server_error_lets_the_next_vendor_try() (+8 more)

### Community 5 - "test_news_lookahead.py"
Cohesion: 0.07
Nodes (41): _epoch(), _tagged(), test_a_flat_article_with_a_null_field_is_read_with_its_default(), test_a_quote_feed_with_articles_is_not_searched(), test_a_search_with_articles_has_answered_even_without_listing_the_symbol(), test_a_search_yahoo_answers_with_not_found_is_an_outage(), test_a_symbol_yahoo_has_no_articles_for_is_left_to_the_next_vendor(), test_a_yahoo_news_outage_moves_to_the_next_configured_vendor() (+33 more)

### Community 6 - "get_instrument_context_from_state"
Cohesion: 0.13
Nodes (26): test_helper_marks_empty_and_passes_through(), create_fundamentals_analyst(), fundamentals_analyst_node(), create_market_analyst(), market_analyst_node(), create_news_analyst(), news_analyst_node(), _as_text() (+18 more)

### Community 7 - "test_cli_symbol_handling.py"
Cohesion: 0.08
Nodes (18): backtest(), AnalystType, AssetType, ask_gemini_thinking_config(), ask_glm_region(), filter_analysts_for_asset_type(), _llm_provider_table(), _matching_choice() (+10 more)

### Community 8 - "test_alpha_vantage_hardening.py"
Cohesion: 0.05
Nodes (40): _FakeResponse, _patched_get(), fake_get(), test_a_rejected_request_is_unavailable_not_data(), test_an_indicator_this_vendor_lacks_lets_the_next_one_serve_it(), test_empty_body_still_passes_through(), test_fundamentals_no_curr_date_passes_through(), test_global_news_omitted_optionals_use_the_configured_defaults() (+32 more)

### Community 9 - "get_capabilities"
Cohesion: 0.07
Nodes (8): test_capabilities_dataclass_is_frozen(), TestDefault, TestExactIdMatches, TestMinimaxExactMatches, TestOpenRouterDeepSeekNamespace, TestPatternMatches, get_capabilities(), ModelCapabilities

### Community 10 - "router.py"
Cohesion: 0.08
Nodes (18): test_a_missing_time_zone_is_not_taken_for_an_answer(), _yahoo_calls(), VendorUnavailableError, get_scrubbed(), vendor_reachable(), _answered_empty(), raise_for_empty(), yf_retry() (+10 more)

### Community 11 - "select_openrouter_model"
Cohesion: 0.09
Nodes (16): ask_output_language(), _fetch_openrouter_models(), _prompt_custom_model_id(), select_chatgpt_model(), _select_listed_model(), select_openrouter_model(), prompts(), _asks() (+8 more)

### Community 12 - "TradingMemoryLog"
Cohesion: 0.09
Nodes (5): test_the_window_reported_is_the_one_the_outcomes_used(), _resolve_entry(), test_concurrent_writers_keep_every_decision_and_outcome(), work(), TradingMemoryLog

### Community 13 - "TestDeferredReflection"
Cohesion: 0.06
Nodes (3): TestDeferredReflection, Reflector, resolve_benchmark()

### Community 14 - "test_chatgpt_provider.py"
Cohesion: 0.09
Nodes (27): ensure_signed_in(), select_llm_provider(), _check_tier_providers(), _expired(), _llm(), _menu(), signed_in(), test_a_chatgpt_tier_beside_an_openai_tier_keeps_each_credential() (+19 more)

### Community 15 - "backtest.py"
Cohesion: 0.12
Nodes (15): Highlights, Upgrading from 0.5.0, _log_with(), test_a_backtest_result_is_summarized_directly(), test_a_result_whose_cells_all_failed_summarizes_as_empty(), test_pending_note_appears_only_when_something_is_pending(), test_summary_scores_resolved_cells_and_keeps_pending_out_of_the_average(), test_summary_states_what_it_cannot_prove() (+7 more)

### Community 16 - "test_cli_headless.py"
Cohesion: 0.10
Nodes (28): unattended_gaps(), _answer(), _Browser, _report_graph(), _selections_with_env(), test_a_closed_stdin_counts_as_no_terminal(), test_a_missing_key_without_a_terminal_names_the_variable(), test_a_page_is_opened_only_in_a_browser_window_on_this_machine() (+20 more)

### Community 17 - "make_log"
Cohesion: 0.08
Nodes (3): make_log(), _seed_completed(), TestTradingMemoryLogCore

### Community 18 - "fetch_returns"
Cohesion: 0.06
Nodes (14): _closes(), _price_df(), test_a_close_that_is_not_a_price_is_skipped_not_scored(), test_a_longer_window_asks_for_enough_price_history(), test_the_holding_window_is_configurable(), test_the_reflection_states_the_window_it_judges(), _make_ticker(), _make_ticker() (+6 more)

### Community 19 - "test_cli_commands.py"
Cohesion: 0.08
Nodes (25): _Result, runner(), _Summary, test_a_failed_login_exits_with_the_reason(), refuse(), test_a_failure_message_with_brackets_is_printed_as_text(), refuse(), test_backtest_can_continue_an_interrupted_sweep() (+17 more)

### Community 20 - "selections.py"
Cohesion: 0.10
Nodes (13): ask_anthropic_effort(), ask_minimax_region(), ask_openai_reasoning_effort(), ask_qwen_region(), parse_analysis_date(), prompt_openai_compatible_url(), depth_from_env(), _from_flag() (+5 more)

### Community 21 - "stocktwits.py"
Cohesion: 0.11
Nodes (7): _drop_spam(), _raise(), _stream(), test_html_entities_in_message_bodies_are_decoded(), TestStockTwitsCryptoSymbols, TestStockTwitsResilience, TestStockTwitsScreening

### Community 22 - "ohlcv.py"
Cohesion: 0.18
Nodes (11): _fake_msvcrt(), _recording_replace(), test_a_file_held_open_elsewhere_keeps_its_old_content(), test_a_lock_held_elsewhere_is_reported_when_not_waiting(), holder(), test_on_windows_a_held_lock_is_reported_when_not_waiting(), test_on_windows_a_lock_that_cannot_be_taken_is_reported_not_retried_forever(), test_on_windows_the_lock_is_waited_for_while_another_writer_holds_it() (+3 more)

### Community 23 - "test_portfolio_context.py"
Cohesion: 0.09
Nodes (20): _bare_graph(), test_a_ticker_held_under_another_spelling_is_matched(), test_absent_context_is_reported_as_not_provided(), test_checkpoint_signature_changes_with_the_portfolio(), test_cli_passes_a_valid_portfolio_into_the_run(), test_cli_rejects_an_unusable_portfolio_file_before_running(), test_completed_run_clears_the_checkpoint_it_wrote(), test_create_run_state_renders_the_portfolio_once() (+12 more)

### Community 24 - "requests"
Cohesion: 0.12
Nodes (8): PolymarketFilterTests, PolymarketFormatTests, PolymarketResilienceTests, PolymarketRoutingTests, get_prediction_markets(), _is_forward_looking(), _parse_json_list(), _request()

### Community 25 - "test_cli_memory_log.py"
Cohesion: 0.07
Nodes (11): _bare_graph(), _FakeBuffer, _FakeGraph, _NullLive, _run_cli(), test_a_run_without_checkpointing_says_nothing_about_resuming(), test_cli_run_uses_the_memory_log_like_propagate(), test_record_decision_appends_a_pending_entry() (+3 more)

### Community 26 - "_resp"
Cohesion: 0.20
Nodes (3): _raise(), _resp(), TestChunkedTransferErrorsHandled

### Community 27 - "get_macro_data"
Cohesion: 0.12
Nodes (7): FredFormattingTests, _capture(), FredResolutionTests, _request_stub(), _fred_today(), get_macro_data(), _resolve_series_id()

### Community 28 - "test_reddit_fallback.py"
Cohesion: 0.11
Nodes (14): _screen_out(), test_a_crypto_pair_is_fetched_from_its_communities_in_one_request(), test_a_crypto_ticker_is_searched_in_crypto_communities(), test_a_subreddit_emptied_by_screening_is_not_called_empty(), test_an_unavailable_screen_keeps_every_post_and_says_so(), test_each_subreddit_keeps_its_own_quota(), test_empty_subreddit_on_a_full_page_is_not_called_empty(), test_posts_from_an_unrequested_or_unnamed_subreddit_are_not_dropped() (+6 more)

### Community 29 - "test"
Cohesion: 0.07
Nodes (35): concurrency, cancel-in-progress, group, TZ, python-version, tz, jobs, lint (+27 more)

### Community 30 - "reddit.py"
Cohesion: 0.09
Nodes (11): _atom_resp(), TestRss429Backoff, TestRssParsing, _coverage_dates(), _fetch_subreddit_rss(), _jitter(), _posted_at(), _read_capped() (+3 more)

### Community 31 - "sign_in"
Cohesion: 0.22
Nodes (16): _id_token(), _nonce_of(), _paster(), read_line(), _status(), test_a_network_failure_while_signing_in_is_reported_not_raised_raw(), test_a_sign_in_without_plan_usage_is_refused(), test_an_answer_for_another_sign_in_attempt_is_ignored() (+8 more)

### Community 32 - "GoogleClient"
Cohesion: 0.08
Nodes (13): TestGoogleApiKeyStandardization, _captured_kwargs(), test_a_gemini_call_times_out_like_the_other_providers(), test_flash_38_keeps_supported_levels(), test_flash_38_remaps_minimal_to_low(), test_flash_passes_thinking_level_through(), test_latest_alias_remaps_minimal_to_low(), test_no_thinking_level_is_omitted() (+5 more)

### Community 33 - "OpenAIClient"
Cohesion: 0.11
Nodes (9): _effort_on(), test_non_reasoning_model_drops_effort(), test_reasoning_model_receives_effort(), test_supports_reasoning_effort(), NativeBaseUrlTests, ResponsesApiSelectionTests, _is_native_openai_base_url(), OpenAIClient (+1 more)

### Community 34 - "chatgpt_auth.py"
Cohesion: 0.09
Nodes (18): refuse(), unreachable(), _b64url(), ChatGPTAuthError, ChatGPTUnreachable, credential(), _due(), _host_id() (+10 more)

### Community 35 - "TradingAgentsGraph"
Cohesion: 0.05
Nodes (5): test_a_failed_reflection_leaves_the_entry_pending_and_lets_the_run_start(), run_config_context(), GraphSetup, TradingAgentsGraph, _validate_trade_date()

### Community 36 - "test_tool_date_enforcement.py"
Cohesion: 0.09
Nodes (19): get_balance_sheet(), get_cashflow(), get_fundamentals(), get_global_news(), get_income_statement(), get_indicators(), get_insider_transactions(), get_macro_indicators() (+11 more)

### Community 37 - "test_rating_integrity.py"
Cohesion: 0.12
Nodes (17): test_a_bare_rating_opening_line_is_the_decision(), test_a_decision_prompt_states_the_shape_of_its_answer(), test_a_quoted_rating_in_a_list_table_or_quote_is_not_the_decision(), test_a_rating_argued_against_is_not_read_as_the_decision(), test_a_rating_someone_else_gave_does_not_become_the_decision(), test_a_rating_the_text_quotes_does_not_replace_the_decision(), test_a_rating_word_without_a_label_is_not_read_as_the_call(), test_a_refusal_has_no_rating_and_is_not_defaulted() (+9 more)

### Community 38 - "test_ollama_base_url.py"
Cohesion: 0.10
Nodes (18): confirm_ollama_endpoint(), _base_url(), _client_module(), _console_out(), test_client_get_llm_picks_up_env(), test_confirm_endpoint_marks_env_origin(), test_confirm_endpoint_quiet_on_local_no_port(), test_confirm_endpoint_shows_default() (+10 more)

### Community 39 - "ResearchPlan"
Cohesion: 0.22
Nodes (6): _make_rm_state(), _structured_rm_llm(), TestRenderResearchPlan, TestResearchManagerAgent, render_research_plan(), ResearchPlan

### Community 40 - "VendorUnavailableError"
Cohesion: 0.10
Nodes (21): _dates_after(), _insider_frame(), test_a_current_run_is_not_cluttered_with_a_vintage_note(), test_a_historical_run_gets_the_current_name_only_as_an_identifier(), test_a_historical_run_is_not_told_todays_date(), test_a_yfinance_failure_is_a_vendor_error_not_a_report(), test_a_yfinance_news_failure_is_a_vendor_error_not_a_report(), test_an_indicator_that_could_not_be_read_is_not_shown_as_a_blank_value() (+13 more)

### Community 41 - "TraderProposal"
Cohesion: 0.08
Nodes (17): _make_trader_state(), _structured_trader_llm(), test_a_field_the_model_did_not_give_says_so(), test_a_price_that_is_a_number_survives(), test_a_price_written_as_a_range_drops_only_that_field(), test_conflict_alone_is_not_a_hold_trigger(), test_invoke_structured_falls_back_when_result_is_none(), test_the_trader_names_the_levels_it_did_not_give() (+9 more)

### Community 42 - "fetch_reddit_posts"
Cohesion: 0.15
Nodes (19): _epoch(), _JsonResp, _msg(), test_in_window_bounds_and_exclusive_upper(), test_in_window_undated_excluded_in_backtest_kept_live(), test_reddit_covered_but_empty_window_is_a_real_absence(), test_reddit_empty_feed_for_an_old_window_is_unavailable(), test_reddit_full_page_does_not_vouch_for_older_days() (+11 more)

### Community 43 - "BaseLLMClient"
Cohesion: 0.35
Nodes (8): _captured(), _config(), test_a_tier_on_another_provider_gets_that_provider_s_settings_and_not_the_main_url(), test_a_tier_url_is_used_for_that_tier_only(), test_a_tier_without_its_own_provider_uses_the_run_s(), test_the_run_settings_and_report_name_each_tier_s_provider(), test_the_tier_settings_are_read_from_the_environment(), _header()

### Community 44 - "build"
Cohesion: 0.07
Nodes (29): env, name, permissions, runs-on, steps, concurrency, cancel-in-progress, group (+21 more)

### Community 45 - "create_sentiment_analyst"
Cohesion: 0.12
Nodes (11): _make_sentiment_state(), _structured_sentiment_llm(), TestRenderSentimentReport, TestSentimentAnalystAgent, _build_system_message(), create_sentiment_analyst(), sentiment_analyst_node(), _seven_days_back() (+3 more)

### Community 46 - "openai_client.py"
Cohesion: 0.09
Nodes (10): test_legacy_ids_stay_valid_without_being_offered(), AzureOpenAIClient, BaseLLMClient, normalize_content(), _bedrock_class(), invoke(), BedrockClient, create_tier_client() (+2 more)

### Community 47 - "test_cli_prefs.py"
Cohesion: 0.09
Nodes (22): load_last_run(), sanitize(), save_last_run(), provider_default_url(), get_user_selections(), TestCliSkipsPromptsFromEnv, TestProviderDefaultUrl, TestReasoningEffortSkippedFromEnv (+14 more)

### Community 48 - "Propagator"
Cohesion: 0.10
Nodes (4): TestPortfolioManagerInjection, InvestDebateState, RiskDebateState, Propagator

### Community 49 - "normalize_symbol"
Cohesion: 0.19
Nodes (3): TestNormalizeSymbol, _normalize_crypto(), normalize_symbol()

### Community 50 - "sentiment_analyst.py"
Cohesion: 0.11
Nodes (10): _make_pm_state(), _structured_pm_llm(), create_portfolio_manager(), portfolio_manager_node(), create_research_manager(), research_manager_node(), render_pm_decision(), bind_structured() (+2 more)

### Community 51 - "test_api_key_env.py"
Cohesion: 0.10
Nodes (13): _prompt_key(), test_case_insensitive_lookup(), test_ensure_api_key_prompts_and_writes_to_env(), test_ensure_api_key_updates_existing_env_file(), test_ensure_api_key_user_cancels_returns_none(), test_every_select_llm_provider_choice_has_an_entry(), test_existing_key_file_is_tightened_before_writing(), test_known_providers_resolve() (+5 more)

### Community 52 - "create_llm_client"
Cohesion: 0.15
Nodes (16): resolve_backend_url(), _capture_kwargs(), test_bearer_token_passed_as_api_key(), test_bedrock_any_model_and_no_key_env(), test_construction_when_extra_installed(), test_factory_routes_bedrock(), test_helpful_error_when_langchain_aws_absent(), test_no_bearer_token_omits_api_key() (+8 more)

### Community 53 - "test_env_overrides.py"
Cohesion: 0.14
Nodes (11): _config_with_env(), test_bool_coercion(), test_empty_env_value_is_passthrough(), test_empty_path_value_keeps_the_default_path(), test_int_coercion(), test_invalid_bool_raises(), test_no_env_uses_built_in_defaults(), test_reasoning_effort_defaults_to_none() (+3 more)

### Community 54 - "Settlement"
Cohesion: 0.20
Nodes (4): test_a_run_does_not_wait_on_another_settlement_pass(), other_pass(), TestSettleAll, settle_all_pending()

### Community 55 - "tradingagents-ollama"
Cohesion: 0.08
Nodes (23): image, profiles, volumes, services, ollama, tradingagents, tradingagents-ollama, build (+15 more)

### Community 56 - "test_chatgpt_auth.py"
Cohesion: 0.25
Nodes (18): _renewal(), _signed_in(), test_a_fresh_token_is_used_without_asking_openai(), test_a_refused_renewal_asks_to_sign_in_again_and_keeps_the_file(), test_a_renewal_for_another_account_is_refused(), test_a_temporary_failure_after_expiry_says_to_try_again_not_to_sign_in(), test_a_temporary_failure_keeps_a_token_that_still_works(), test_a_token_near_expiry_is_renewed_with_the_stored_refresh_token() (+10 more)

### Community 57 - "ConditionalLogic"
Cohesion: 0.17
Nodes (9): _debate_state(), _state(), test_debate_path_map_covers_full_router_range(), test_debate_router_return_always_routable(), test_path_map_covers_full_router_range(), test_router_return_always_routable(), test_router_terminates_at_round_limit(), AgentState (+1 more)

### Community 58 - "test_tool_date_enforcement.py"
Cohesion: 0.16
Nodes (16): _run(), _State, test_a_start_date_that_is_not_a_date_is_sent_back_to_the_model(), test_a_tool_serves_the_run_instrument_whatever_the_model_passes(), test_a_window_whose_start_is_not_a_date_is_refused(), test_as_of_takes_the_earlier_date(), test_as_of_window(), test_as_of_without_a_trade_date_passes_the_request_through() (+8 more)

### Community 59 - "parse_rating"
Cohesion: 0.16
Nodes (3): TestExtractRating, TestParseRating, parse_rating()

### Community 60 - "run_analysis"
Cohesion: 0.18
Nodes (9): update_analyst_statuses(), _bare_graph(), _state(), test_a_message_that_reads_like_a_python_value_is_still_text(), test_every_selected_analyst_is_in_progress_until_its_report_lands(), test_the_live_display_does_not_scroll_the_terminal(), test_the_other_shapes_are_unchanged(), test_the_state_log_keeps_non_ascii_readable() (+1 more)

### Community 61 - "re"
Cohesion: 0.19
Nodes (18): _fields(), _html(), _state(), test_an_agent_s_own_headings_sit_below_its_heading(), test_header_values_are_escaped(), test_report_text_cannot_inject_markup_or_fetch_anything(), test_run_details_show_each_value_as_its_own_field(), test_the_contents_name_each_section_once_and_list_its_agents_beneath() (+10 more)

### Community 62 - "checkpointer.py"
Cohesion: 0.16
Nodes (5): checkpoint_step(), clear_all_checkpoints(), clear_checkpoint(), _db_path(), get_checkpointer()

### Community 63 - "test_fundamentals_lookahead.py"
Cohesion: 0.15
Nodes (6): _av(), TestAlphaVantageHistoricalRun, TestLiveRunUnchanged, TestNoUsableFieldsStillRaises, TestYFinanceHistoricalRun, _yf()

### Community 64 - "build_llm_kwargs"
Cohesion: 0.22
Nodes (14): _config_with_env(), test_coerce_accepts_positive_ints_and_numeric_strings(), test_coerce_rejects_booleans(), test_coerce_rejects_non_integers(), test_coerce_rejects_non_positive(), test_default_is_none(), test_env_override_sets_config(), test_env_string_is_coerced() (+6 more)

### Community 65 - "HierarchyTests"
Cohesion: 0.12
Nodes (9): HierarchyTests, RouterHandlesBaseTypesTests, not_covered(), throttled(), _unconfigured(), _throttled(), _unconfigured(), AlphaVantageNotConfiguredError (+1 more)

### Community 66 - "AnthropicClient"
Cohesion: 0.21
Nodes (3): _capture_kwargs(), TestEffortGate, AnthropicClient

### Community 67 - "build_instrument_context"
Cohesion: 0.08
Nodes (12): [0.5.2] — 2026-09-29, Added, Contributors, Fixed, Models, Upgrading from 0.5.1, BuildInstrumentContextTests, GetInstrumentContextFromStateTests (+4 more)

### Community 68 - "TradingAgents: Multi-Agents LLM Financial Trading Framework"
Cohesion: 0.12
Nodes (14): Analyst Team, Checkpoint resume, Citation, Contributing, Evaluating decisions over time, Memory log, News, Persistence and Recovery (+6 more)

### Community 69 - "test_post_screen.py"
Cohesion: 0.07
Nodes (37): _Calls, jev(), _ok(), post(), _post_answers(), fake_post(), _Response, test_a_base_url_without_a_key_does_not_turn_screening_on() (+29 more)

### Community 70 - "test_provider_registry.py"
Cohesion: 0.16
Nodes (10): _Recorder, _signed_in_provider(), test_a_missing_sign_in_fails_before_any_request(), test_a_signed_in_provider_refuses_another_endpoint_or_key(), test_a_signed_in_provider_sends_its_own_credential_never_an_api_key(), test_key_optionality(), test_registry_membership(), test_registry_spec() (+2 more)

### Community 72 - "test_cli_config_precedence.py"
Cohesion: 0.18
Nodes (9): _build_run_config(), test_a_half_set_round_count_says_which_value_won(), test_a_tier_s_thinking_setting_survives_a_main_provider_that_has_none(), test_checkpoint_flag_overrides_env(), test_checkpoint_none_preserves_env_default(), test_env_round_counts_win_over_selection(), test_glm_resolves_to_the_endpoint_its_key_belongs_to(), test_partial_env_only_overrides_that_count() (+1 more)

### Community 73 - "test_checkpoint_resume.py"
Cohesion: 0.17
Nodes (5): _build_graph(), _node_a(), _node_b(), _SimpleState, TestCheckpointResume

### Community 74 - "test_llm_max_retries.py"
Cohesion: 0.17
Nodes (15): test_unconfigured_providers_keep_sdk_defaults(), _config_with_env(), test_coerce_accepts_non_negative_ints_and_numeric_strings(), test_coerce_rejects_booleans(), test_coerce_rejects_negative(), test_coerce_rejects_non_integers(), test_default_is_none(), test_env_override_sets_config() (+7 more)

### Community 75 - "settle_pending"
Cohesion: 0.11
Nodes (6): test_any_failure_to_price_a_decision_is_reported(), test_the_graph_settles_every_ticker_under_its_own_config(), TestSettlementOnceAndDurably, down(), settle_pending(), Settlement

### Community 76 - "test_model_validation.py"
Cohesion: 0.11
Nodes (6): DummyLLMClient, ModelValidationTests, test_a_retired_model_id_still_runs_without_a_warning(), test_an_explicit_alias_of_a_listed_model_is_known(), test_every_provider_lets_you_name_your_own_model(), get_known_models()

### Community 77 - "os"
Cohesion: 0.15
Nodes (5): test_a_replaced_file_keeps_the_usual_permissions(), test_it_works_unconfigured_and_takes_the_caller_s_own_contact(), test_the_default_identification_names_the_package_version(), replace_file(), _user_agent()

### Community 78 - "test_cli_symbol_handling.py"
Cohesion: 0.10
Nodes (11): detect_asset_type(), get_ticker(), is_valid_ticker_input(), normalize_ticker_symbol(), parse_ticker(), test_cli_normalize_delegates_to_data_layer(), test_detect_asset_type(), test_normalize_symbol_crypto_and_passthrough() (+3 more)

### Community 79 - "conftest.py"
Cohesion: 0.14
Nodes (7): _at_a_terminal(), _blank_settings_overlay(), _dummy_api_keys(), _isolate_config(), _no_network(), _own_cli_prefs(), _own_file_locations()

### Community 80 - "test_dataflows_config.py"
Cohesion: 0.15
Nodes (13): _graph(), test_a_graph_built_earlier_still_runs_with_its_own_config(), test_a_run_config_missing_a_newer_key_still_reads_the_default(), test_a_run_reads_its_own_graphs_vendors_not_the_last_graph_built(), test_concurrent_runs_each_read_their_own_config(), _run(), test_settling_reads_the_graphs_own_config(), test_tools_inside_a_langgraph_run_see_the_run_config() (+5 more)

### Community 81 - "run.py"
Cohesion: 0.12
Nodes (8): display_complete_report(), analyze(), ensure_api_key(), _graphical_browser(), _offer_reports(), _open_page(), _run_directory(), _yes()

### Community 82 - "stocktwits.py"
Cohesion: 0.17
Nodes (5): TestStripHtml, _strip_html(), _body(), _created_at(), _within_window()

### Community 83 - "_graph"
Cohesion: 0.15
Nodes (12): _graph(), ScriptedModel, test_a_debug_run_prints_the_analysts_work_and_reaches_the_same_decision(), test_a_full_run_reaches_a_logged_decision(), test_a_graph_reused_across_runs_keeps_no_run_state(), test_a_streamed_run_reads_its_own_graph_config(), test_a_tool_limit_the_recursion_limit_cannot_hold_is_refused(), test_an_interrupted_run_resumes_from_its_checkpoint() (+4 more)

### Community 84 - "test_ohlcv_date_column.py"
Cohesion: 0.15
Nodes (5): _ohlcv(), test_cleaning_a_frame_with_undated_rows_writes_to_its_own_copy(), TestCleanDataframeAcrossVersions, TestEnsureDateColumn, _ensure_date_column()

### Community 85 - "test_structured_agent_prompts.py"
Cohesion: 0.23
Nodes (11): _capturing_llm(), _prompt_text(), test_constraint_text_is_unambiguous(), test_portfolio_manager_prompt_states_constraint(), test_research_manager_prompt_states_constraint(), test_sentiment_prompt_states_constraint(), test_the_sentiment_prompt_names_the_subreddits_searched(), test_tool_using_analysts_keep_their_date_guidance() (+3 more)

### Community 86 - "NoMarketDataError"
Cohesion: 0.04
Nodes (34): test_an_unreachable_yahoo_is_not_reported_as_a_symbol_without_insider_data(), TestLoadOhlcvNoPoison, TestRouteToVendorSentinel, raises_no_data(), raises_no_data(), TestNoMarketDataError, _rate_limited(), test_a_price_request_that_fails_is_unavailable_even_when_yahoo_answers() (+26 more)

### Community 87 - "attributes"
Cohesion: 0.12
Nodes (15): description, label, options, placeholder, render, value, body, attributes (+7 more)

### Community 88 - "attributes"
Cohesion: 0.12
Nodes (15): description, label, multiple, options, placeholder, value, body, attributes (+7 more)

### Community 89 - ".warn_if_unknown_model"
Cohesion: 0.08
Nodes (3): NormalizedChatAnthropic, _supports_effort(), NormalizedAzureChatOpenAI

### Community 90 - "test_suite_isolation.py"
Cohesion: 0.21
Nodes (4): test_a_test_cannot_reach_the_network(), test_a_test_saves_cli_selections_to_its_own_directory(), test_the_suite_keeps_its_files_out_of_the_users_home(), test_yfinance_keeps_its_cache_out_of_the_users_home()

### Community 91 - "test_minimax.py"
Cohesion: 0.20
Nodes (4): _client(), TestMinimaxReasoningSplit, TestMinimaxStructuredOutputDispatch, _Pick

### Community 92 - "run_backtest"
Cohesion: 0.14
Nodes (22): _config(), _scored(), test_a_bearish_call_that_fell_counts_as_right(), test_a_bearish_call_that_rose_counts_as_wrong(), test_a_bullish_call_is_scored_the_same_way_as_before(), test_a_cell_already_in_the_log_is_not_run_again(), test_a_failed_cell_does_not_abort_the_sweep(), test_a_failed_settlement_does_not_lose_the_remaining_tickers() (+14 more)

### Community 93 - "Changelog"
Cohesion: 0.12
Nodes (17): [0.1.0] — 2025-06-05, [0.1.1] — 2025-06-07, [0.3.1] — 2026-07-05, [0.4.0] — 2026-08-31, [0.5.1] — 2026-09-24, Added, Added, Added (+9 more)

### Community 94 - "test_llm_429_resilience.py"
Cohesion: 0.16
Nodes (8): _chat(), test_every_429_fails_after_the_retry_cap_with_a_clear_message(), test_one_429_with_retry_after_then_200_succeeds(), test_the_clear_message_never_carries_the_api_key(), _transport(), _chatgpt_credential(), LLMCapacityError, LocalCompatibleChatOpenAI

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

### Community 101 - "AnalystWallTimeTracker"
Cohesion: 0.38
Nodes (4): AnalystWallTimeTracker, sync_analyst_tracker_from_chunk(), AnalystWallTimeTrackerTests, AnalystExecutionPlan

### Community 103 - "[0.2.1] — 2026-03-15"
Cohesion: 0.33
Nodes (6): [0.2.1] — 2026-03-15, Added, Contributors, Fixed, Removed, Security

### Community 104 - "test_checkpoint_lifecycle.py"
Cohesion: 0.23
Nodes (10): _bare_graph(), _node_a(), _node_b(), _State, test_begin_returns_thread_id_and_recompiles(), test_checkpoint_input_is_none_only_when_resuming(), test_clearing_removes_the_database_sidecars(), test_cli_style_usage_saves_then_resumes() (+2 more)

### Community 105 - "test_fundamentals_units.py"
Cohesion: 0.33
Nodes (7): _fundamentals(), test_a_figure_with_no_stated_currency_is_printed_bare(), test_an_absent_percent_field_is_left_out(), test_an_adr_quotes_in_dollars_and_reports_in_its_home_currency(), test_each_money_figure_carries_the_currency_it_is_in(), test_income_figures_without_a_stated_reporting_currency_are_printed_bare(), test_percent_fields_carry_their_unit_and_fractions_are_unchanged()

### Community 106 - "Build with TypeSafe"
Cohesion: 0.12
Nodes (15): Build with TypeSafe, Compose requests, Confidence is rarely the gate, Cookbooks, Criteria, Design the state, Judgments from Jev, decisions in code, Live docs (+7 more)

### Community 107 - "pytest"
Cohesion: 0.33
Nodes (5): _call(), _response(), test_a_passthrough_status_is_returned_for_the_caller(), test_nothing_that_holds_the_url_travels_with_the_error(), test_the_key_is_masked_in_the_error()

### Community 108 - "[0.2.4] — 2026-04-25"
Cohesion: 0.33
Nodes (6): [0.2.4] — 2026-04-25, Added, Changed, Contributors, Fixed, Removed

### Community 109 - ".save_reports"
Cohesion: 0.18
Nodes (7): [0.6.0] — 2026-10-03, Added, Added, Contributors, Fixed, Models, Upgrading from 0.5.2

### Community 110 - "display.py"
Cohesion: 0.13
Nodes (3): format_tokens(), format_tool_args(), update_display()

### Community 112 - "test_memory_pointintime.py"
Cohesion: 0.44
Nodes (8): _log(), _resolve(), test_as_of_excludes_lessons_resolved_after_the_run_date(), test_cross_ticker_lessons_are_also_gated(), test_legacy_entry_without_resolution_date_excluded_in_backtest(), test_memory_as_of_gates_historical_but_not_live(), test_no_as_of_is_unfiltered_live_behavior(), test_resolution_date_is_stored_and_parsed()

### Community 113 - "[0.2.3] — 2026-03-29"
Cohesion: 0.40
Nodes (5): [0.2.3] — 2026-03-29, Added, Changed, Contributors, Fixed

### Community 114 - "run_analysis"
Cohesion: 0.20
Nodes (8): create_layout(), update_research_team_status(), _announce_checkpoint_state(), run_analysis(), save_message_decorator(), wrapper(), save_report_section_decorator(), save_tool_call_decorator()

### Community 115 - "[0.3.0] — 2026-06-22"
Cohesion: 0.40
Nodes (5): [0.3.0] — 2026-06-22, Changed, Contributors, Fixed, Removed

### Community 116 - "test_debate_opening.py"
Cohesion: 0.33
Nodes (8): prompt(), _capturing_llm(), _investment_state(), _risk_state(), test_researcher_opening_has_no_phantom_opponent(), test_researcher_passes_real_opponent_argument(), test_risk_opening_has_no_phantom_opponent(), test_risk_passes_real_opponent_arguments()

### Community 117 - "Installation and CLI"
Cohesion: 0.29
Nodes (7): CLI Usage, Docker, Installation, Installation and CLI, Markets and tickers, Rate-limited endpoints (429), Required APIs

### Community 119 - "write_report_tree"
Cohesion: 0.26
Nodes (11): _state(), test_a_partial_settings_dict_still_writes_the_report(), test_run_settings_name_the_version_of_the_running_code(), test_run_settings_record_the_run_without_endpoints_or_paths(), test_save_reports_defaults_under_results_dir(), test_save_reports_explicit_path(), test_the_header_names_the_analysts_as_users_select_them(), test_the_report_header_names_the_rating() (+3 more)

### Community 120 - "os"
Cohesion: 0.09
Nodes (9): FredConfigTests, FredRoutingTests, _unconfigured(), test_error_without_the_key_in_its_message_still_drops_the_request(), TestKeyKeptOutOfErrors, VendorNotConfiguredError, FredNotConfiguredError, get_api_key() (+1 more)

### Community 124 - "[0.2.5] — 2026-05-11"
Cohesion: 0.40
Nodes (5): [0.2.5] — 2026-05-11, Added, Changed, Fixed, Security

### Community 125 - "_analyst_graph"
Cohesion: 0.28
Nodes (7): handler(), _analyst_graph(), calls(), more_or_wrap_up(), rounds(), wrap_up(), _tools_or_done()

### Community 126 - "os"
Cohesion: 0.18
Nodes (9): test_a_period_reported_under_two_tags_takes_the_preferred_one_not_both(), _as_of(), _cached_json(), cik_for(), _fetch_json(), get_cashflow(), get_income_statement(), _span_index() (+1 more)

### Community 129 - "test_opencode_session.py"
Cohesion: 0.19
Nodes (9): test_get_llm_attaches_headers_for_opencode(), test_get_llm_no_headers_elsewhere(), test_headers_only_for_opencode(), test_opencode_endpoint_detection(), test_session_id_env_override(), test_session_id_stable_within_process(), is_opencode_endpoint(), request_headers() (+1 more)

### Community 130 - "_fact"
Cohesion: 0.14
Nodes (10): _columns(), _fact(), test_a_cash_flow_filed_year_to_date_is_served_with_its_span(), test_a_recast_outside_the_annual_report_still_counts_from_its_filing(), eps(), test_a_row_filed_only_year_to_date_keeps_its_figure_beside_a_row_filed_by_quarter(), test_a_twelve_month_total_from_a_quarterly_report_is_not_a_fiscal_year(), test_an_annual_balance_sheet_has_no_quarter_end_columns() (+2 more)

### Community 131 - "DeepSeekChatOpenAI"
Cohesion: 0.20
Nodes (4): TestDeepSeekLiveStructuredOutput, _Pick, _Sample, DeepSeekChatOpenAI

### Community 132 - "contact_links"
Cohesion: 0.33
Nodes (5): blank_issues_enabled, contact_links, about, name, url

### Community 134 - "LoopingModel"
Cohesion: 0.33
Nodes (3): LoopingModel, test_an_analyst_that_keeps_calling_tools_writes_its_report_at_the_limit(), test_the_last_turn_is_offered_no_tools_and_reads_its_tool_results_as_text()

### Community 135 - "[0.7.0] — 2026-10-16"
Cohesion: 0.40
Nodes (5): [0.7.0] — 2026-10-16, Added, Contributors, Fixed, Upgrading from 0.6.0

### Community 137 - "FakeOpenAI"
Cohesion: 0.20
Nodes (4): FakeOpenAI, home(), openai(), _Response

### Community 140 - "StaleGuardRoutingTests"
Cohesion: 0.20
Nodes (3): StaleGuardPropagationTests, StaleGuardRoutingTests, _stale()

### Community 143 - "build_default_config"
Cohesion: 0.20
Nodes (5): test_invalid_int_raises(), test_dependency_wiring_goes_the_same_route(), _apply_env_overrides(), build_default_config(), _coerce()

### Community 144 - "_validated_claims"
Cohesion: 0.28
Nodes (7): _b64(), _jwks(), test_a_genuine_id_token_is_accepted(), test_an_id_token_for_another_sign_in_is_refused(), test_an_id_token_signed_by_another_key_is_refused(), _b64url_decode(), _validated_claims()

### Community 153 - "[0.2.0] — 2026-02-04"
Cohesion: 0.40
Nodes (5): [0.2.0] — 2026-02-04, Added, Changed, Contributors, Fixed

### Community 155 - "crypto_base"
Cohesion: 0.32
Nodes (3): TestCryptoBase, crypto_base(), _stocktwits_symbol()

### Community 156 - "TradingAgents Package"
Cohesion: 0.40
Nodes (5): Current holdings, Fundamentals as filed, Implementation Details, Python Usage, TradingAgents Package

### Community 161 - "test_temperature_config.py"
Cohesion: 0.16
Nodes (3): TestProviderKwargsTemperature, TestTemperatureEnvOverlay, TestTemperatureForwarding

### Community 163 - "[0.2.2] — 2026-03-22"
Cohesion: 0.40
Nodes (5): [0.2.2] — 2026-03-22, Added, Changed, Contributors, Fixed

## Knowledge Gaps
- **1 isolated node(s):** `tradingagents`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1311 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **32 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `TradingAgentsGraph` connect `TradingAgentsGraph` to `thread_id`, `TestDeferredReflection`, `backtest.py`, `test_cli_headless.py`, `fetch_returns`, `test_portfolio_context.py`, `test_cli_memory_log.py`, `TradingAgents Package`, `BaseLLMClient`, `Propagator`, `ConditionalLogic`, `test_tool_date_enforcement.py`, `run_analysis`, `checkpointer.py`, `build_instrument_context`, `test_checkpoint_resume.py`, `settle_pending`, `test_dataflows_config.py`, `run.py`, `_graph`, `run_backtest`, `test_checkpoint_lifecycle.py`, `.save_reports`, `TestLegacyRemoval`, `test_memory_pointintime.py`, `run_analysis`, `write_report_tree`?**
  _High betweenness centrality (0.042) - this node is a cross-community bridge._
- **Are the 26 inferred relationships involving `TradingAgentsGraph` (e.g. with `Python Usage` and `_bare_graph()`) actually correct?**
  _`TradingAgentsGraph` has 26 INFERRED edges - model-reasoned connections that need verification._
- **What connects `tradingagents` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `set_config` be split into smaller, more focused modules?**
  _Cohesion score 0.0803633822501747 - nodes in this community are weakly interconnected._
- **Why does `Changelog` connect `Changelog` to `[0.2.2] — 2026-03-22`, `TradingAgents: Multi-Agents LLM Financial Trading Framework`, `build_instrument_context`, `[0.2.1] — 2026-03-15`, `[0.7.0] — 2026-10-16`, `[0.2.4] — 2026-04-25`, `.save_reports`, `[0.2.3] — 2026-03-29`, `[0.3.0] — 2026-06-22`, `[0.2.0] — 2026-02-04`, `[0.2.5] — 2026-05-11`, `[0.5.0] — 2026-09-18`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Are the 21 inferred relationships involving `NoMarketDataError` (e.g. with `TestNoUsableFieldsStillRaises` and `TestLoadOhlcvNoPoison`) actually correct?**
  _`NoMarketDataError` has 21 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_ohlcv_latest_bar.py` be split into smaller, more focused modules?**
  _Cohesion score 0.059227921734531994 - nodes in this community are weakly interconnected._