# Market and competitor research

Use this when the client asks "what do others do?", when a buy-vs-build decision is open, or when a gap analysis needs an outside reference. Research answers one question: **which capabilities does the market treat as standard, and where can this solution be different?**

## Source weight

Rank sources and say which one an answer rests on:

1. Analyst reports the client has licensed (Gartner, Forrester, IDC). Use only the parts you can read. A gated report you cannot open is a pointer, not evidence.
2. Vendor documentation and release notes (what shipped, with dates).
3. Independent reviews (G2, Capterra, Peer Insights) for weaknesses and complaints.
4. Vendor marketing pages. Mark these "vendor claim".
5. AI-generated decks and summaries. Lowest weight. Check each number elsewhere.

## Rules

- **Never get around a bot check, paywall or login.** If a site blocks automated access, use other public sources and say which facts come from search snippets only.
- **Every claim has a numbered source** with an access date.
- **Record conflicts** (two sources disagree on price, dates or status). Never pick one silently.
- **Shipped vs announced.** AI features are often announced months before general availability. Record the status and date.
- **Prices change.** Store them with a date and say "not public" when they are not.

## Profile per competitor

Keep one folder per vendor in the knowledge base: `<vendor>/docs/sources.md` (URL list, the original) and `<vendor>/docs-md/01_<vendor>-profile.md` (the profile). Use `templates/competitor-profile.md`:

1. Summary (what, for whom, platform)
2. Fit for this client (size, stack, price)
3. Pricing (public facts only)
4. Capabilities by area (one row per requirement area)
5. AI and agents (shipped vs announced)
6. Client-facing features
7. UX patterns worth copying
8. Weaknesses from reviews
9. Analyst position
10. Ideas for this solution, each tagged with a requirement area

Profile five or six vendors from different segments (enterprise suite, mid-market, client-portal specialist, ERP-native, the client's own ecosystem vendor). More vendors add noise.

## From research to gaps

Build `templates/gap-matrix.md`: one row per capability, with columns for the market reference, the legacy system, the current prototype, the gap, and the requirement ID. Then write two short lists:

- **Where the solution wins** — lead the client demo with these.
- **Where it must catch up before a client sees it** — these become the next prototype's scope.

## Delegation

Research is parallel work. Give one researcher agent (`market-researcher`) two vendors each, with the profile template and the source rules above. Each agent writes its files and returns a ten-line summary. You then write the gap matrix yourself, so one mind holds the comparison.
