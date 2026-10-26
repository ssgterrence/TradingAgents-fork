"""Shared prompt rules for decision agents.

Kept outside the agent modules so a rule can be stated once and rendered by
both the Research Manager and the Portfolio Manager (issue I-16).
"""

HEADLINE_NUMERIC_CLAIM_RULE = (
    "A numeric claim sourced only from a news headline must be labelled "
    "\"headline, unverified\" and cannot be the sole basis for a rating."
)
