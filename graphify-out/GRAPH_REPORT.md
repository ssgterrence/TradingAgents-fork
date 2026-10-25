# Graph Report - TradingAgents-fork  (2026-10-25)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 3436 nodes · 8091 edges · 153 communities (118 shown, 35 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 442 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e8f5503e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- date_window.py
- test_ohlcv_latest_bar.py
- test_cli_updates.py
- NoMarketDataError
- test_sec_edgar.py
- test_news_lookahead.py
- get_instrument_context_from_state
- prompts.py
- set_config
- get_capabilities
- router.py
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
- test_structured_agents.py
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
- test_structured_agent_prompts.py
- test_undated_tools_as_of.py
- TraderProposal
- fetch_reddit_posts
- BaseLLMClient
- build
- create_sentiment_analyst
- openai_client.py
- test_cli_prefs.py
- Propagator
- normalize_symbol
- trading_graph.py
- test_api_key_env.py
- create_llm_client
- test_env_overrides.py
- test_chatgpt_auth.py
- tradingagents-ollama
- report_html.py
- ConditionalLogic
- test_dataflows_config.py
- test_tool_date_enforcement.py
- display.py
- re
- checkpointer.py
- test_fundamentals_lookahead.py
- build_llm_kwargs
- route_to_vendor
- AnthropicClient
- resolve_instrument_identity
- test_llm_max_tokens.py
- test_post_screen.py
- parse_rating
- StatsCallbackHandler
- test_cli_config_precedence.py
- _structured_pm_llm
- settle_all_pending
- settle_pending
- test_model_validation.py
- test_provider_registry.py
- test_cli_display.py
- conftest.py
- HierarchyTests
- run.py
- sign_in
- _graph
- write_report_tree
- test_temperature_config.py
- .warn_if_unknown_model
- attributes
- attributes
- test_checkpoint_resume.py
- test_checkpoint_lifecycle.py
- test_minimax.py
- test_cli_env_skip.py
- post_screen.py
- safe_ticker_component
- build_verified_market_snapshot
- MessageBuffer
- test_deepseek_reasoning.py
- body
- test_a_report_that_was_never_produced_says_so
- test_graph_end_to_end.py
- test_suite_isolation.py
- TestStructuredOutputCapabilityDispatch
- unit
- DeepSeekChatOpenAI
- test_fundamentals_units.py
- analyst_execution.py
- pytest
- FakeOpenAI
- thread_id
- build_instrument_context
- TestLegacyRemoval
- test_memory_pointintime.py
- AnalystWallTimeTracker
- jev
- test_the_cli_says_when_a_run_produced_no_usable_rating
- create_trader
- backtest.py
- ScriptedModel
- _validated_claims
- FredRoutingTests
- test_i18n_coverage.py
- TestOneRequestForAllSubreddits
- login
- _Callback
- TestDeepSeekReasoningContent
- _analyst_graph
- test_layering.py
- NormalizedChatOpenAI
- tradingagents/__init__.py
- get_verified_market_snapshot
- wrapper
- contact_links
- test_news_analyst_prompt.py
- LoopingModel
- TestCryptoSearchTerm
- _FakeGraph
- analyze
- _Unreachable
- test_fundamentals_ask_a_new_ticker_after_a_rate_limit
- _identity
- _apply_env_overrides
- test_a_settlement_failure_is_noted_and_the_run_goes_on
- test_the_sentiment_analyst_hands_the_screen_to_both_social_fetchers
- tradingagents

## God Nodes (most connected - your core abstractions)
1. `TradingAgentsGraph` - 67 edges
2. `NoMarketDataError` - 60 edges
3. `set_config()` - 53 edges
4. `VendorUnavailableError` - 51 edges
5. `make_log()` - 49 edges
6. `TradingMemoryLog` - 47 edges
7. `get_instrument_context_from_state()` - 44 edges
8. `route_to_vendor()` - 43 edges
9. `get_language_instruction()` - 42 edges
10. `normalize_symbol()` - 39 edges

## Surprising Connections (you probably didn't know these)
- `HierarchyTests` --uses--> `AlphaVantageNotConfiguredError`  [INFERRED]
  tests/test_vendor_errors.py → tradingagents/dataflows/vendors/alpha_vantage/common.py
- `RouterHandlesBaseTypesTests` --uses--> `AlphaVantageNotConfiguredError`  [INFERRED]
  tests/test_vendor_errors.py → tradingagents/dataflows/vendors/alpha_vantage/common.py
- `_unconfigured()` --calls--> `AlphaVantageNotConfiguredError`  [EXTRACTED]
  tests/test_vendor_errors.py → tradingagents/dataflows/vendors/alpha_vantage/common.py
- `HierarchyTests` --uses--> `AlphaVantageRateLimitError`  [INFERRED]
  tests/test_vendor_errors.py → tradingagents/dataflows/vendors/alpha_vantage/common.py
- `RouterHandlesBaseTypesTests` --uses--> `AlphaVantageRateLimitError`  [INFERRED]
  tests/test_vendor_errors.py → tradingagents/dataflows/vendors/alpha_vantage/common.py

## Import Cycles
- None detected.

## Communities (153 total, 35 thin omitted)

### Community 0 - "date_window.py"
Cohesion: 0.05
Nodes (36): _FakeResponse, _patched_get(), fake_get(), test_a_rejected_request_is_unavailable_not_data(), test_an_indicator_this_vendor_lacks_lets_the_next_one_serve_it(), test_empty_body_still_passes_through(), test_fundamentals_no_curr_date_passes_through(), test_global_news_omitted_optionals_use_the_configured_defaults() (+28 more)

### Community 1 - "test_ohlcv_latest_bar.py"
Cohesion: 0.05
Nodes (34): _fail_download(), _load(), _stamp(), test_a_download_from_an_earlier_day_is_not_fresh(), test_current_day_cache_past_ttl_is_not_fresh(), test_historical_request_uses_todays_cache_past_the_ttl(), test_load_ohlcv_refetches_stale_same_day_cache(), test_load_ohlcv_reuses_fresh_same_day_cache() (+26 more)

### Community 2 - "test_cli_updates.py"
Cohesion: 0.07
Nodes (42): _applies(), due(), enabled(), _get_json(), messages(), parse_notices(), _plain(), read_cache() (+34 more)

### Community 3 - "NoMarketDataError"
Cohesion: 0.05
Nodes (23): TestLoadOhlcvNoPoison, TestRouteToVendorSentinel, raises_no_data(), raises_no_data(), TestNoMarketDataError, load(), _frame(), StaleGuardPropagationTests (+15 more)

### Community 4 - "test_sec_edgar.py"
Cohesion: 0.06
Nodes (36): _columns(), _fact(), _no_network_or_cache(), test_a_cash_flow_filed_year_to_date_is_served_with_its_span(), test_a_filer_with_no_usable_facts_reads_differently_from_a_non_filer(), test_a_line_the_filer_does_not_tag_is_named_unavailable(), test_a_non_filer_is_reported_as_such_not_as_missing_data(), test_a_per_share_figure_keeps_its_own_unit() (+28 more)

### Community 5 - "test_news_lookahead.py"
Cohesion: 0.08
Nodes (38): _epoch(), _tagged(), test_a_flat_article_with_a_null_field_is_read_with_its_default(), test_a_quote_feed_with_articles_is_not_searched(), test_a_search_with_articles_has_answered_even_without_listing_the_symbol(), test_a_search_yahoo_answers_with_not_found_is_an_outage(), test_a_symbol_yahoo_has_no_articles_for_is_left_to_the_next_vendor(), test_a_yahoo_news_outage_moves_to_the_next_configured_vendor() (+30 more)

### Community 6 - "get_instrument_context_from_state"
Cohesion: 0.13
Nodes (27): _risk_state(), test_helper_marks_empty_and_passes_through(), test_risk_passes_real_opponent_arguments(), create_fundamentals_analyst(), fundamentals_analyst_node(), create_market_analyst(), market_analyst_node(), create_news_analyst() (+19 more)

### Community 7 - "prompts.py"
Cohesion: 0.08
Nodes (18): backtest(), AnalystType, AssetType, detect_asset_type(), filter_analysts_for_asset_type(), is_valid_ticker_input(), _llm_provider_table(), normalize_ticker_symbol() (+10 more)

### Community 8 - "set_config"
Cohesion: 0.07
Nodes (14): DataflowsConfigIsolationTests, test_get_yfin_requests_inclusive_end(), test_load_ohlcv_requests_inclusive_end(), test_a_current_run_is_still_served_yahoo_statements(), test_alpha_vantage_withholds_insider_trades_from_a_past_run_without_asking(), test_alpha_vantage_withholds_statements_from_a_past_run_without_asking(), test_statements_come_from_sec_edgar_first_by_default(), test_yahoo_withholds_insider_trades_from_a_past_run_without_asking() (+6 more)

### Community 9 - "get_capabilities"
Cohesion: 0.07
Nodes (8): test_capabilities_dataclass_is_frozen(), TestDefault, TestExactIdMatches, TestMinimaxExactMatches, TestOpenRouterDeepSeekNamespace, TestPatternMatches, get_capabilities(), ModelCapabilities

### Community 10 - "router.py"
Cohesion: 0.09
Nodes (19): test_an_unreachable_yahoo_is_not_reported_as_a_symbol_without_insider_data(), _yahoo_calls(), withhold_undisclosed_trades(), VendorNotConfiguredError, VendorUnavailableError, vendor_reachable(), _answered_empty(), raise_for_empty() (+11 more)

### Community 11 - "test_backtest.py"
Cohesion: 0.11
Nodes (32): _config(), _fake_graph(), _log_with(), _scored(), test_a_backtest_result_is_summarized_directly(), test_a_bearish_call_that_fell_counts_as_right(), test_a_bearish_call_that_rose_counts_as_wrong(), test_a_bullish_call_is_scored_the_same_way_as_before() (+24 more)

### Community 12 - "TradingMemoryLog"
Cohesion: 0.07
Nodes (9): test_the_window_reported_is_the_one_the_outcomes_used(), _resolve_entry(), test_concurrent_writers_keep_every_decision_and_outcome(), work(), test_an_unscored_decision_is_left_out_of_the_backtest_figures(), test_the_memory_log_records_review_rather_than_a_tradeable_hold(), test_the_signal_and_the_log_agree_on_the_same_decision(), locked() (+1 more)

### Community 13 - "TestDeferredReflection"
Cohesion: 0.06
Nodes (3): TestDeferredReflection, Reflector, resolve_benchmark()

### Community 14 - "test_chatgpt_provider.py"
Cohesion: 0.08
Nodes (28): ensure_api_key(), ensure_signed_in(), select_llm_provider(), _check_tier_providers(), _expired(), _llm(), _menu(), signed_in() (+20 more)

### Community 15 - "select_openrouter_model"
Cohesion: 0.08
Nodes (19): ask_output_language(), _fetch_openrouter_models(), _matching_choice(), _prompt_custom_model_id(), _require_text(), select_chatgpt_model(), _select_listed_model(), _select_model() (+11 more)

### Community 16 - "test_cli_headless.py"
Cohesion: 0.10
Nodes (29): _offer_reports(), unattended_gaps(), _answer(), _Browser, _report_graph(), _selections_with_env(), test_a_closed_stdin_counts_as_no_terminal(), test_a_missing_key_without_a_terminal_names_the_variable() (+21 more)

### Community 17 - "make_log"
Cohesion: 0.08
Nodes (3): make_log(), _seed_completed(), TestTradingMemoryLogCore

### Community 18 - "fetch_returns"
Cohesion: 0.06
Nodes (13): _closes(), _price_df(), test_a_close_that_is_not_a_price_is_skipped_not_scored(), test_a_failed_reflection_leaves_the_entry_pending_and_lets_the_run_start(), test_a_longer_window_asks_for_enough_price_history(), _make_ticker(), _make_ticker(), _make_ticker() (+5 more)

### Community 19 - "test_cli_commands.py"
Cohesion: 0.08
Nodes (25): _Result, runner(), _Summary, test_a_failed_login_exits_with_the_reason(), refuse(), test_a_failure_message_with_brackets_is_printed_as_text(), refuse(), test_backtest_can_continue_an_interrupted_sweep() (+17 more)

### Community 20 - "selections.py"
Cohesion: 0.08
Nodes (19): ask_anthropic_effort(), ask_gemini_thinking_config(), ask_glm_region(), ask_minimax_region(), ask_openai_reasoning_effort(), ask_qwen_region(), get_ticker(), parse_analysis_date() (+11 more)

### Community 21 - "stocktwits.py"
Cohesion: 0.08
Nodes (12): _drop_spam(), _raise(), _stream(), test_html_entities_in_message_bodies_are_decoded(), TestStockTwitsCryptoSymbols, TestStockTwitsResilience, TestStockTwitsScreening, _body() (+4 more)

### Community 22 - "ohlcv.py"
Cohesion: 0.09
Nodes (15): _fake_msvcrt(), _recording_replace(), test_a_file_held_open_elsewhere_keeps_its_old_content(), test_a_lock_held_elsewhere_is_reported_when_not_waiting(), holder(), test_a_replaced_file_keeps_the_usual_permissions(), test_on_windows_a_held_lock_is_reported_when_not_waiting(), test_on_windows_a_lock_that_cannot_be_taken_is_reported_not_retried_forever() (+7 more)

### Community 23 - "test_portfolio_context.py"
Cohesion: 0.09
Nodes (20): _bare_graph(), test_a_ticker_held_under_another_spelling_is_matched(), test_absent_context_is_reported_as_not_provided(), test_checkpoint_signature_changes_with_the_portfolio(), test_cli_passes_a_valid_portfolio_into_the_run(), test_cli_rejects_an_unusable_portfolio_file_before_running(), test_completed_run_clears_the_checkpoint_it_wrote(), test_create_run_state_renders_the_portfolio_once() (+12 more)

### Community 24 - "requests"
Cohesion: 0.07
Nodes (13): test_error_without_the_key_in_its_message_still_drops_the_request(), PolymarketFilterTests, PolymarketFormatTests, PolymarketResilienceTests, PolymarketRoutingTests, get_scrubbed(), FredNotConfiguredError, get_api_key() (+5 more)

### Community 25 - "test_cli_memory_log.py"
Cohesion: 0.07
Nodes (11): _bare_graph(), _FakeBuffer, _FakeGraph, _NullLive, _run_cli(), test_a_run_without_checkpointing_says_nothing_about_resuming(), test_cli_run_uses_the_memory_log_like_propagate(), test_record_decision_appends_a_pending_entry() (+3 more)

### Community 26 - "test_structured_agents.py"
Cohesion: 0.11
Nodes (12): test_invoke_structured_falls_back_when_result_is_none(), test_the_trader_names_the_levels_it_did_not_give(), create_portfolio_manager(), portfolio_manager_node(), research_manager_node(), render_pm_decision(), render_research_plan(), render_trader_proposal() (+4 more)

### Community 27 - "get_macro_data"
Cohesion: 0.08
Nodes (9): FredConfigTests, FredFormattingTests, _capture(), FredResolutionTests, _request_stub(), TestKeyKeptOutOfErrors, _fred_today(), get_macro_data() (+1 more)

### Community 28 - "test_reddit_fallback.py"
Cohesion: 0.08
Nodes (16): _raise(), _resp(), _screen_out(), test_a_crypto_pair_is_fetched_from_its_communities_in_one_request(), test_a_crypto_ticker_is_searched_in_crypto_communities(), test_a_subreddit_emptied_by_screening_is_not_called_empty(), test_an_unavailable_screen_keeps_every_post_and_says_so(), test_each_subreddit_keeps_its_own_quota() (+8 more)

### Community 29 - "test"
Cohesion: 0.07
Nodes (35): concurrency, cancel-in-progress, group, TZ, python-version, tz, jobs, lint (+27 more)

### Community 30 - "reddit.py"
Cohesion: 0.09
Nodes (12): _atom_resp(), TestRss429Backoff, TestStripHtml, _coverage_dates(), _fetch_subreddit_rss(), _jitter(), _posted_at(), _read_capped() (+4 more)

### Community 31 - "test_yahoo_rate_limit.py"
Cohesion: 0.09
Nodes (13): _rate_limited(), test_a_missing_time_zone_is_not_taken_for_an_answer(), test_a_price_request_that_fails_is_unavailable_even_when_yahoo_answers(), test_a_price_request_that_raises_is_unavailable_whether_or_not_yahoo_answers(), test_a_rate_limit_that_outlasts_the_retries_is_reported_as_one(), test_a_request_that_yfinance_would_swallow_is_unavailable(), test_a_snapshot_with_no_rows_is_reported_not_raised(), test_a_yahoo_request_that_fails_is_unavailable_not_absent() (+5 more)

### Community 32 - "GoogleClient"
Cohesion: 0.08
Nodes (13): TestGoogleApiKeyStandardization, _captured_kwargs(), test_a_gemini_call_times_out_like_the_other_providers(), test_flash_38_keeps_supported_levels(), test_flash_38_remaps_minimal_to_low(), test_flash_passes_thinking_level_through(), test_latest_alias_remaps_minimal_to_low(), test_no_thinking_level_is_omitted() (+5 more)

### Community 33 - "OpenAIClient"
Cohesion: 0.08
Nodes (9): _effort_on(), test_non_reasoning_model_drops_effort(), test_reasoning_model_receives_effort(), test_supports_reasoning_effort(), NativeBaseUrlTests, ResponsesApiSelectionTests, _is_native_openai_base_url(), OpenAIClient (+1 more)

### Community 34 - "chatgpt_auth.py"
Cohesion: 0.09
Nodes (18): refuse(), unreachable(), _b64url(), ChatGPTAuthError, ChatGPTUnreachable, credential(), _due(), _host_id() (+10 more)

### Community 35 - "TradingAgentsGraph"
Cohesion: 0.10
Nodes (4): _announce_checkpoint_state(), run_analysis(), run_rating(), TradingAgentsGraph

### Community 36 - "tools.py"
Cohesion: 0.12
Nodes (14): get_balance_sheet(), get_cashflow(), get_fundamentals(), get_global_news(), get_income_statement(), get_indicators(), get_insider_transactions(), get_macro_indicators() (+6 more)

### Community 37 - "test_rating_integrity.py"
Cohesion: 0.12
Nodes (14): test_a_decision_prompt_states_the_shape_of_its_answer(), test_a_quoted_rating_in_a_list_table_or_quote_is_not_the_decision(), test_a_rating_argued_against_is_not_read_as_the_decision(), test_a_rating_someone_else_gave_does_not_become_the_decision(), test_a_rating_the_text_quotes_does_not_replace_the_decision(), test_a_rating_word_without_a_label_is_not_read_as_the_call(), test_a_refusal_has_no_rating_and_is_not_defaulted(), test_a_state_without_the_typed_rating_reads_it_from_the_decision() (+6 more)

### Community 38 - "test_ollama_base_url.py"
Cohesion: 0.10
Nodes (18): confirm_ollama_endpoint(), _base_url(), _client_module(), _console_out(), test_client_get_llm_picks_up_env(), test_confirm_endpoint_marks_env_origin(), test_confirm_endpoint_quiet_on_local_no_port(), test_confirm_endpoint_shows_default() (+10 more)

### Community 39 - "test_structured_agent_prompts.py"
Cohesion: 0.14
Nodes (17): _capturing_llm(), _prompt_text(), test_constraint_text_is_unambiguous(), test_portfolio_manager_prompt_states_constraint(), test_research_manager_prompt_states_constraint(), test_sentiment_prompt_states_constraint(), test_the_sentiment_prompt_names_the_subreddits_searched(), test_tool_using_analysts_keep_their_date_guidance() (+9 more)

### Community 40 - "test_undated_tools_as_of.py"
Cohesion: 0.11
Nodes (19): _dates_after(), _insider_frame(), test_a_current_run_is_not_cluttered_with_a_vintage_note(), test_a_historical_run_gets_the_current_name_only_as_an_identifier(), test_a_historical_run_is_not_told_todays_date(), test_a_yfinance_failure_is_a_vendor_error_not_a_report(), test_a_yfinance_news_failure_is_a_vendor_error_not_a_report(), test_an_indicator_that_could_not_be_read_is_not_shown_as_a_blank_value() (+11 more)

### Community 41 - "TraderProposal"
Cohesion: 0.10
Nodes (9): test_a_field_the_model_did_not_give_says_so(), test_a_price_that_is_a_number_survives(), test_a_price_written_as_a_range_drops_only_that_field(), test_conflict_alone_is_not_a_hold_trigger(), TestNullishFloatCoercion, TestRenderTraderProposal, _coerce_optional_float(), PortfolioDecision (+1 more)

### Community 42 - "fetch_reddit_posts"
Cohesion: 0.14
Nodes (20): _epoch(), _JsonResp, _msg(), test_in_window_bounds_and_exclusive_upper(), test_in_window_undated_excluded_in_backtest_kept_live(), test_reddit_covered_but_empty_window_is_a_real_absence(), test_reddit_empty_feed_for_an_old_window_is_unavailable(), test_reddit_full_page_does_not_vouch_for_older_days() (+12 more)

### Community 43 - "BaseLLMClient"
Cohesion: 0.12
Nodes (12): _captured(), _config(), test_a_tier_on_another_provider_gets_that_provider_s_settings_and_not_the_main_url(), test_a_tier_url_is_used_for_that_tier_only(), test_a_tier_without_its_own_provider_uses_the_run_s(), test_the_run_settings_and_report_name_each_tier_s_provider(), test_the_tier_settings_are_read_from_the_environment(), AzureOpenAIClient (+4 more)

### Community 44 - "build"
Cohesion: 0.07
Nodes (29): env, name, permissions, runs-on, steps, concurrency, cancel-in-progress, group (+21 more)

### Community 45 - "create_sentiment_analyst"
Cohesion: 0.12
Nodes (11): _make_sentiment_state(), _structured_sentiment_llm(), TestRenderSentimentReport, TestSentimentAnalystAgent, _build_system_message(), create_sentiment_analyst(), sentiment_analyst_node(), _seven_days_back() (+3 more)

### Community 46 - "openai_client.py"
Cohesion: 0.12
Nodes (7): NormalizedChatAnthropic, _supports_effort(), normalize_content(), _bedrock_class(), invoke(), _chatgpt_credential(), validate_model()

### Community 47 - "test_cli_prefs.py"
Cohesion: 0.14
Nodes (17): load_last_run(), sanitize(), save_last_run(), get_user_selections(), _answer_every_prompt(), test_a_corrupt_file_degrades_to_no_memory(), test_a_custom_language_is_remembered_without_breaking_the_next_run(), test_a_half_written_file_cannot_be_observed() (+9 more)

### Community 48 - "Propagator"
Cohesion: 0.11
Nodes (4): TestPortfolioManagerInjection, InvestDebateState, RiskDebateState, Propagator

### Community 49 - "normalize_symbol"
Cohesion: 0.13
Nodes (5): TestCryptoBase, TestNormalizeSymbol, crypto_base(), _normalize_crypto(), normalize_symbol()

### Community 50 - "trading_graph.py"
Cohesion: 0.08
Nodes (5): test_the_holding_window_is_configurable(), test_the_reflection_states_the_window_it_judges(), run_config_context(), GraphSetup, _validate_trade_date()

### Community 51 - "test_api_key_env.py"
Cohesion: 0.10
Nodes (13): _prompt_key(), test_case_insensitive_lookup(), test_ensure_api_key_prompts_and_writes_to_env(), test_ensure_api_key_updates_existing_env_file(), test_ensure_api_key_user_cancels_returns_none(), test_every_select_llm_provider_choice_has_an_entry(), test_existing_key_file_is_tightened_before_writing(), test_known_providers_resolve() (+5 more)

### Community 52 - "create_llm_client"
Cohesion: 0.15
Nodes (16): _capture_kwargs(), test_bearer_token_passed_as_api_key(), test_bedrock_any_model_and_no_key_env(), test_construction_when_extra_installed(), test_factory_routes_bedrock(), test_helpful_error_when_langchain_aws_absent(), test_no_bearer_token_omits_api_key(), test_any_model_accepted_no_forced_key() (+8 more)

### Community 53 - "test_env_overrides.py"
Cohesion: 0.12
Nodes (13): _config_with_env(), test_bool_coercion(), test_empty_env_value_is_passthrough(), test_empty_path_value_keeps_the_default_path(), test_int_coercion(), test_invalid_bool_raises(), test_invalid_int_raises(), test_no_env_uses_built_in_defaults() (+5 more)

### Community 54 - "test_chatgpt_auth.py"
Cohesion: 0.25
Nodes (18): _renewal(), _signed_in(), test_a_fresh_token_is_used_without_asking_openai(), test_a_refused_renewal_asks_to_sign_in_again_and_keeps_the_file(), test_a_renewal_for_another_account_is_refused(), test_a_temporary_failure_after_expiry_says_to_try_again_not_to_sign_in(), test_a_temporary_failure_keeps_a_token_that_still_works(), test_a_token_near_expiry_is_renewed_with_the_stored_refresh_token() (+10 more)

### Community 55 - "tradingagents-ollama"
Cohesion: 0.08
Nodes (23): image, profiles, volumes, services, ollama, tradingagents, tradingagents-ollama, build (+15 more)

### Community 56 - "report_html.py"
Cohesion: 0.13
Nodes (10): _chain(), _fields(), _group(), _markdown(), _render_agent_text(), render_report(), _run_details(), analyst_names() (+2 more)

### Community 57 - "ConditionalLogic"
Cohesion: 0.17
Nodes (9): _debate_state(), _state(), test_debate_path_map_covers_full_router_range(), test_debate_router_return_always_routable(), test_path_map_covers_full_router_range(), test_router_return_always_routable(), test_router_terminates_at_round_limit(), AgentState (+1 more)

### Community 58 - "test_dataflows_config.py"
Cohesion: 0.15
Nodes (13): _graph(), test_a_graph_built_earlier_still_runs_with_its_own_config(), test_a_run_config_missing_a_newer_key_still_reads_the_default(), test_a_run_reads_its_own_graphs_vendors_not_the_last_graph_built(), test_concurrent_runs_each_read_their_own_config(), _run(), test_settling_reads_the_graphs_own_config(), test_tools_inside_a_langgraph_run_see_the_run_config() (+5 more)

### Community 59 - "test_tool_date_enforcement.py"
Cohesion: 0.17
Nodes (16): _run(), _State, test_a_start_date_that_is_not_a_date_is_sent_back_to_the_model(), test_a_tool_serves_the_run_instrument_whatever_the_model_passes(), test_a_window_whose_start_is_not_a_date_is_refused(), test_as_of_takes_the_earlier_date(), test_as_of_window(), test_as_of_without_a_trade_date_passes_the_request_through() (+8 more)

### Community 60 - "display.py"
Cohesion: 0.10
Nodes (6): classify_message_type(), create_layout(), format_tokens(), format_tool_args(), update_display(), update_research_team_status()

### Community 61 - "re"
Cohesion: 0.25
Nodes (17): _fields(), _html(), _state(), test_an_agent_s_own_headings_sit_below_its_heading(), test_header_values_are_escaped(), test_report_text_cannot_inject_markup_or_fetch_anything(), test_run_details_show_each_value_as_its_own_field(), test_the_contents_name_each_section_once_and_list_its_agents_beneath() (+9 more)

### Community 62 - "checkpointer.py"
Cohesion: 0.16
Nodes (5): checkpoint_step(), clear_all_checkpoints(), clear_checkpoint(), _db_path(), get_checkpointer()

### Community 63 - "test_fundamentals_lookahead.py"
Cohesion: 0.15
Nodes (6): _av(), TestAlphaVantageHistoricalRun, TestLiveRunUnchanged, TestNoUsableFieldsStillRaises, TestYFinanceHistoricalRun, _yf()

### Community 64 - "build_llm_kwargs"
Cohesion: 0.21
Nodes (13): _config_with_env(), test_coerce_accepts_non_negative_ints_and_numeric_strings(), test_coerce_rejects_booleans(), test_coerce_rejects_negative(), test_coerce_rejects_non_integers(), test_default_is_none(), test_env_override_sets_config(), test_forwarded_across_providers() (+5 more)

### Community 65 - "route_to_vendor"
Cohesion: 0.20
Nodes (7): _no_data(), _raises(), _reset_config(), _returns(), impl(), VendorRoutingTests, route_to_vendor()

### Community 66 - "AnthropicClient"
Cohesion: 0.18
Nodes (3): _capture_kwargs(), TestEffortGate, AnthropicClient

### Community 67 - "resolve_instrument_identity"
Cohesion: 0.14
Nodes (4): GetInstrumentContextFromStateTests, ResolveInstrumentIdentityTests, test_identity_lookup_normalizes_symbol(), resolve_instrument_identity()

### Community 68 - "test_llm_max_tokens.py"
Cohesion: 0.22
Nodes (14): _config_with_env(), test_coerce_accepts_positive_ints_and_numeric_strings(), test_coerce_rejects_booleans(), test_coerce_rejects_non_integers(), test_coerce_rejects_non_positive(), test_default_is_none(), test_env_override_sets_config(), test_env_string_is_coerced() (+6 more)

### Community 69 - "test_post_screen.py"
Cohesion: 0.23
Nodes (13): _ok(), _Response, test_a_long_retry_after_is_capped(), test_a_response_without_every_answer_is_an_error(), test_a_retry_after_header_sets_the_wait(), test_other_failures_raise_without_retry(), test_other_request_errors_are_screening_failures_without_retry(), test_rate_limits_overload_and_dropped_connections_are_retried() (+5 more)

### Community 70 - "parse_rating"
Cohesion: 0.16
Nodes (3): TestExtractRating, TestParseRating, parse_rating()

### Community 72 - "test_cli_config_precedence.py"
Cohesion: 0.16
Nodes (10): resolve_backend_url(), _build_run_config(), test_a_half_set_round_count_says_which_value_won(), test_a_tier_s_thinking_setting_survives_a_main_provider_that_has_none(), test_checkpoint_flag_overrides_env(), test_checkpoint_none_preserves_env_default(), test_env_round_counts_win_over_selection(), test_glm_resolves_to_the_endpoint_its_key_belongs_to() (+2 more)

### Community 73 - "_structured_pm_llm"
Cohesion: 0.14
Nodes (8): prompt(), _capturing_llm(), _investment_state(), test_researcher_opening_has_no_phantom_opponent(), test_researcher_passes_real_opponent_argument(), test_risk_opening_has_no_phantom_opponent(), _make_pm_state(), _structured_pm_llm()

### Community 74 - "settle_all_pending"
Cohesion: 0.12
Nodes (6): test_a_run_does_not_wait_on_another_settlement_pass(), other_pass(), test_the_graph_settles_every_ticker_under_its_own_config(), TestSettleAll, settle_all_pending(), Settlement

### Community 75 - "settle_pending"
Cohesion: 0.13
Nodes (4): test_any_failure_to_price_a_decision_is_reported(), TestSettlementOnceAndDurably, down(), settle_pending()

### Community 76 - "test_model_validation.py"
Cohesion: 0.18
Nodes (7): DummyLLMClient, ModelValidationTests, test_a_retired_model_id_still_runs_without_a_warning(), test_an_explicit_alias_of_a_listed_model_is_known(), test_every_provider_lets_you_name_your_own_model(), test_legacy_ids_stay_valid_without_being_offered(), get_known_models()

### Community 77 - "test_provider_registry.py"
Cohesion: 0.16
Nodes (10): _Recorder, _signed_in_provider(), test_a_missing_sign_in_fails_before_any_request(), test_a_signed_in_provider_refuses_another_endpoint_or_key(), test_a_signed_in_provider_sends_its_own_credential_never_an_api_key(), test_key_optionality(), test_registry_membership(), test_registry_spec() (+2 more)

### Community 78 - "test_cli_display.py"
Cohesion: 0.18
Nodes (8): extract_content_string(), _bare_graph(), _state(), test_a_message_that_reads_like_a_python_value_is_still_text(), test_the_live_display_does_not_scroll_the_terminal(), test_the_other_shapes_are_unchanged(), test_the_state_log_keeps_non_ascii_readable(), test_the_state_log_names_each_field_as_the_state_does()

### Community 79 - "conftest.py"
Cohesion: 0.14
Nodes (7): _at_a_terminal(), _blank_settings_overlay(), _dummy_api_keys(), _isolate_config(), _no_network(), _own_cli_prefs(), _own_file_locations()

### Community 80 - "HierarchyTests"
Cohesion: 0.12
Nodes (7): HierarchyTests, RouterHandlesBaseTypesTests, not_covered(), throttled(), _unconfigured(), _throttled(), _unconfigured()

### Community 81 - "run.py"
Cohesion: 0.15
Nodes (6): display_complete_report(), _graphical_browser(), _open_page(), _run_directory(), _yes(), test_the_run_directory_cannot_escape_the_results_directory()

### Community 82 - "sign_in"
Cohesion: 0.22
Nodes (16): _id_token(), _nonce_of(), _paster(), read_line(), _status(), test_a_network_failure_while_signing_in_is_reported_not_raised_raw(), test_a_sign_in_without_plan_usage_is_refused(), test_an_answer_for_another_sign_in_attempt_is_ignored() (+8 more)

### Community 83 - "_graph"
Cohesion: 0.18
Nodes (10): _graph(), test_a_debug_run_prints_the_analysts_work_and_reaches_the_same_decision(), test_a_full_run_reaches_a_logged_decision(), test_a_graph_reused_across_runs_keeps_no_run_state(), test_a_streamed_run_reads_its_own_graph_config(), test_a_tool_limit_the_recursion_limit_cannot_hold_is_refused(), test_an_interrupted_run_resumes_from_its_checkpoint(), test_each_report_streams_as_soon_as_its_analyst_files_it() (+2 more)

### Community 84 - "write_report_tree"
Cohesion: 0.26
Nodes (11): _state(), test_a_partial_settings_dict_still_writes_the_report(), test_run_settings_name_the_version_of_the_running_code(), test_run_settings_record_the_run_without_endpoints_or_paths(), test_save_reports_defaults_under_results_dir(), test_save_reports_explicit_path(), test_the_header_names_the_analysts_as_users_select_them(), test_the_report_header_names_the_rating() (+3 more)

### Community 85 - "test_temperature_config.py"
Cohesion: 0.16
Nodes (3): TestProviderKwargsTemperature, TestTemperatureEnvOverlay, TestTemperatureForwarding

### Community 87 - "attributes"
Cohesion: 0.12
Nodes (15): description, label, options, placeholder, render, value, body, attributes (+7 more)

### Community 88 - "attributes"
Cohesion: 0.12
Nodes (15): description, label, multiple, options, placeholder, value, body, attributes (+7 more)

### Community 89 - "test_checkpoint_resume.py"
Cohesion: 0.17
Nodes (5): _build_graph(), _node_a(), _node_b(), _SimpleState, TestCheckpointResume

### Community 90 - "test_checkpoint_lifecycle.py"
Cohesion: 0.23
Nodes (10): _bare_graph(), _node_a(), _node_b(), _State, test_begin_returns_thread_id_and_recompiles(), test_checkpoint_input_is_none_only_when_resuming(), test_clearing_removes_the_database_sidecars(), test_cli_style_usage_saves_then_resumes() (+2 more)

### Community 91 - "test_minimax.py"
Cohesion: 0.20
Nodes (4): _client(), TestMinimaxReasoningSplit, TestMinimaxStructuredOutputDispatch, _Pick

### Community 92 - "test_cli_env_skip.py"
Cohesion: 0.19
Nodes (5): provider_default_url(), TestCliSkipsPromptsFromEnv, TestProviderDefaultUrl, TestReasoningEffortSkippedFromEnv, TestResearchDepthSkippedFromEnv

### Community 93 - "post_screen.py"
Cohesion: 0.16
Nodes (8): _answers(), _ask_each(), screen(), _retry_after(), _stance(), TypeSafeError, _unscreened(), _url()

### Community 95 - "build_verified_market_snapshot"
Cohesion: 0.23
Nodes (4): _sample_ohlcv(), TestTool, TestVerifiedSnapshot, build_verified_market_snapshot()

### Community 96 - "MessageBuffer"
Cohesion: 0.16
Nodes (3): MessageBuffer, update_analyst_statuses(), test_every_selected_analyst_is_in_progress_until_its_report_lands()

### Community 97 - "test_deepseek_reasoning.py"
Cohesion: 0.19
Nodes (3): TestBaseClassIsolation, TestInputToMessages, _input_to_messages()

### Community 98 - "body"
Cohesion: 0.15
Nodes (12): description, label, value, body, attributes, id, type, validations (+4 more)

### Community 99 - "test_a_report_that_was_never_produced_says_so"
Cohesion: 0.24
Nodes (3): test_a_report_that_was_never_produced_says_so(), test_an_analyst_brief_is_text_not_a_python_object(), test_an_analyst_is_not_asked_for_a_trade_call_nothing_reads()

### Community 100 - "test_graph_end_to_end.py"
Cohesion: 0.17
Nodes (4): _Client, offline(), test_past_decisions_settle_alongside_the_analysts(), TimedModel

### Community 101 - "test_suite_isolation.py"
Cohesion: 0.21
Nodes (4): test_a_test_cannot_reach_the_network(), test_a_test_saves_cli_selections_to_its_own_directory(), test_the_suite_keeps_its_files_out_of_the_users_home(), test_yfinance_keeps_its_cache_out_of_the_users_home()

### Community 103 - "unit"
Cohesion: 0.29
Nodes (11): _post_answers(), test_a_base_url_without_a_key_does_not_turn_screening_on(), test_a_failure_does_not_wait_for_requests_still_in_flight(), json(), test_an_answer_missing_its_fields_reads_as_malformed(), test_each_post_is_its_own_state_under_the_fixed_questions(), test_no_key_no_screen(), test_one_failed_request_leaves_every_post_unscreened() (+3 more)

### Community 104 - "DeepSeekChatOpenAI"
Cohesion: 0.18
Nodes (4): TestDeepSeekLiveStructuredOutput, _Pick, _Sample, DeepSeekChatOpenAI

### Community 105 - "test_fundamentals_units.py"
Cohesion: 0.33
Nodes (7): _fundamentals(), test_a_figure_with_no_stated_currency_is_printed_bare(), test_an_absent_percent_field_is_left_out(), test_an_adr_quotes_in_dollars_and_reports_in_its_home_currency(), test_each_money_figure_carries_the_currency_it_is_in(), test_income_figures_without_a_stated_reporting_currency_are_printed_bare(), test_percent_fields_carry_their_unit_and_fractions_are_unchanged()

### Community 106 - "analyst_execution.py"
Cohesion: 0.27
Nodes (4): AnalystExecutionPlanTests, AnalystExecutionPlan, AnalystNodeSpec, build_analyst_execution_plan()

### Community 107 - "pytest"
Cohesion: 0.33
Nodes (5): _call(), _response(), test_a_passthrough_status_is_returned_for_the_caller(), test_nothing_that_holds_the_url_travels_with_the_error(), test_the_key_is_masked_in_the_error()

### Community 108 - "FakeOpenAI"
Cohesion: 0.20
Nodes (4): FakeOpenAI, home(), openai(), _Response

### Community 110 - "build_instrument_context"
Cohesion: 0.22
Nodes (3): BuildInstrumentContextTests, TickerSymbolHandlingTests, build_instrument_context()

### Community 112 - "test_memory_pointintime.py"
Cohesion: 0.44
Nodes (8): _log(), _resolve(), test_as_of_excludes_lessons_resolved_after_the_run_date(), test_cross_ticker_lessons_are_also_gated(), test_legacy_entry_without_resolution_date_excluded_in_backtest(), test_memory_as_of_gates_historical_but_not_live(), test_no_as_of_is_unfiltered_live_behavior(), test_resolution_date_is_stored_and_parsed()

### Community 113 - "AnalystWallTimeTracker"
Cohesion: 0.49
Nodes (3): AnalystWallTimeTracker, sync_analyst_tracker_from_chunk(), AnalystWallTimeTrackerTests

### Community 114 - "jev"
Cohesion: 0.22
Nodes (4): _Calls, jev(), post(), fake_post()

### Community 116 - "create_trader"
Cohesion: 0.44
Nodes (4): _make_trader_state(), _structured_trader_llm(), TestTraderAgent, create_trader()

### Community 117 - "backtest.py"
Cohesion: 0.22
Nodes (4): _alpha(), BacktestSummary, _canonical(), RatingScore

### Community 119 - "_validated_claims"
Cohesion: 0.28
Nodes (7): _b64(), _jwks(), test_a_genuine_id_token_is_accepted(), test_an_id_token_for_another_sign_in_is_refused(), test_an_id_token_signed_by_another_key_is_refused(), _b64url_decode(), _validated_claims()

### Community 120 - "FredRoutingTests"
Cohesion: 0.22
Nodes (3): FredRoutingTests, _unconfigured(), get_category_for_method()

### Community 126 - "_analyst_graph"
Cohesion: 0.32
Nodes (6): _analyst_graph(), calls(), more_or_wrap_up(), rounds(), wrap_up(), _tools_or_done()

### Community 130 - "get_verified_market_snapshot"
Cohesion: 0.29
Nodes (3): get_verified_market_snapshot(), no_data_available(), vendor_unavailable()

### Community 131 - "wrapper"
Cohesion: 0.33
Nodes (4): save_message_decorator(), wrapper(), save_report_section_decorator(), save_tool_call_decorator()

### Community 132 - "contact_links"
Cohesion: 0.33
Nodes (5): blank_issues_enabled, contact_links, about, name, url

### Community 134 - "LoopingModel"
Cohesion: 0.33
Nodes (3): LoopingModel, test_an_analyst_that_keeps_calling_tools_writes_its_report_at_the_limit(), test_the_last_turn_is_offered_no_tools_and_reads_its_tool_results_as_text()

## Knowledge Gaps
- **1 isolated node(s):** `tradingagents`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 1204 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **35 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `TradingAgentsGraph` connect `TradingAgentsGraph` to `.save_reports`, `test_backtest.py`, `TestDeferredReflection`, `test_cli_headless.py`, `._memory_step`, `fetch_returns`, `test_portfolio_context.py`, `test_cli_memory_log.py`, `BaseLLMClient`, `Propagator`, `trading_graph.py`, `ConditionalLogic`, `test_dataflows_config.py`, `test_tool_date_enforcement.py`, `checkpointer.py`, `settle_all_pending`, `test_cli_display.py`, `run.py`, `_graph`, `write_report_tree`, `test_checkpoint_resume.py`, `test_checkpoint_lifecycle.py`, `thread_id`, `TestLegacyRemoval`, `test_memory_pointintime.py`, `backtest.py`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Are the 25 inferred relationships involving `TradingAgentsGraph` (e.g. with `_bare_graph()` and `TestCheckpointSignature`) actually correct?**
  _`TradingAgentsGraph` has 25 INFERRED edges - model-reasoned connections that need verification._
- **What connects `tradingagents` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `date_window.py` be split into smaller, more focused modules?**
  _Cohesion score 0.052947052947052944 - nodes in this community are weakly interconnected._
- **Why does `TradingMemoryLog` connect `TradingMemoryLog` to `test_rating_integrity.py`, `_FakeGraph`, `test_backtest.py`, `TestLegacyRemoval`, `test_memory_pointintime.py`, `make_log`, `trading_graph.py`, `fetch_returns`, `backtest.py`, `test_portfolio_context.py`, `test_cli_memory_log.py`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Are the 22 inferred relationships involving `NoMarketDataError` (e.g. with `TestNoUsableFieldsStillRaises` and `TestLoadOhlcvNoPoison`) actually correct?**
  _`NoMarketDataError` has 22 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_ohlcv_latest_bar.py` be split into smaller, more focused modules?**
  _Cohesion score 0.0525879917184265 - nodes in this community are weakly interconnected._