# Evolve website copy: direct-response voice guide (September 8, 2026)

Directed by Marc Atnipp (FDI Creative) on 2026-09-08: page copy is to be developed in a Dan Kennedy
direct-response style, with solid headlines and hooks, but based in fact. This guide governs every
edit to the copy packages in `content/`. The generator (`build.py`) turns those Markdown files into
the site, so the structural rules below are not optional.

## 1. The voice

Write like a seasoned data-center builder talking to an owner across a table. Direct. Specific.
No throat-clearing. Every section should make the reader want the next section, and every page
should end with one clear thing to do.

Principles, in priority order:

1. **Fact first, then the hook.** The hook is allowed only when a fact carries it. The approved
   facts are listed in section 3. Nothing else is a fact on this site.
2. **Speak to "you."** Name the reader's situation (the utility queue, the change orders, the live
   floor, the GPU order) before describing what Evolve does about it.
3. **Problem, cost, solution, proof, next step.** Lead with the problem the reader has today, say
   what it costs when it is handled late, show how Evolve's lifecycle handles it, back it with the
   approved proof, then tell the reader exactly what to do next and why now.
4. **Reason why.** Whenever Evolve does something a certain way, say why in one sentence
   ("because the same team has to commission it").
5. **Specific beats clever.** "Long-lead switchgear" beats "critical equipment." "Before the first
   purchase order" beats "early."
6. **Subheads are hooks.** Every `###` and `####` heading that is not a structural marker
   (section 4) should promise something or name a decision, not label a topic.
7. **Bullets are fascinations.** A bullet states a result, a decision or a risk avoided, not a noun.
8. **Short sentences. Short paragraphs.** One idea per sentence. Cut every word that does not earn
   its place. Rewritten sections should be the same length or shorter than the original.
9. **Close every section.** The last line of a section points to the next decision or the CTA.
10. **Confident, never hype.** Kennedy is bold because he is specific, not because he shouts.

## 2. Words and claims that are banned

Never write: best, largest, leading, industry-leading, world-class, premier, unmatched, unrivaled,
guarantee/guaranteed, number one, cutting-edge, state-of-the-art, revolutionary, fastest, 24/7/365,
"zero downtime," "patented," "world's first," any response-time promise, any customer or project
name, any capacity, density, cooling, production-rate or headcount figure, any international claim,
any compliance credential (HIPAA, PCI, FedRAMP, FISMA) as an Evolve certification, any facilities-
maintained count. Do not invent case studies, quotes, testimonials, awards or statistics.

Do not add urgency that is not true. "Before the utility queue decides it for you" is a real cost
of delay. "Only three slots left" is not.

## 3. The only facts you may use (approved claims CLM-001 to CLM-014 and CLM-039)

- Evolve specializes in data centers and serves a nationwide market.
- Lifecycle: Plan, Design, Build, Power, Maintain (these exact five words, this order).
- Design & Build includes Modular, Hyperscale and AI Data Centers.
- 2,200+ mission-critical projects completed. 5.3+ GW of power deployed. 20+ years in business.
  Founded in 2004; headquartered in Houston, Texas. Zero injuries recorded since 2010.
- Evolve self-performs modular fabrication in its own shop. Modular systems can be factory-built
  and site-set in days (qualitative; never promise a schedule).
- Evolve stays engaged after turnover through monitoring, maintenance and long-term support.
- Construction capability: retrofits, live-environment work, power conversions, upgrades,
  expansions, new builds, planning, procurement, commissioning, monitoring and maintenance.
- Contact: 10555 Cossey Road, Houston, Texas 77070; 832-375-0099; support@evolveincorporated.com.

Write the proof exactly as shown: "2,200+", "5.3+ GW", "20+ years", "zero injuries recorded since
2010". Never "since 2004" for safety. Never restate the power figure in MW.

## 4. Structural rules the generator depends on

Keep these exactly as they are (line text and heading level), because `build.py` keys on them:

- The `# PAGE-nnn — Name` line, `**URL:**`, `**Page brief:**`, `**Audience:**`, `**Primary action:**`.
- `## Publishable page copy` / `## Publishable article`, `## Metadata recommendation`,
  `## Schema recommendation`, `## Claim review`, `**Title:**`, `**Meta description:**`.
- `### Hero`, `**Eyebrow:**`, the `# H1` line, the first paragraph after the H1, `**Primary CTA:**`,
  `**Secondary CTA:**`; the `### Final CTA` block with its `## heading`, description line and
  `**CTA:**` / `**Secondary CTA:**` lines. These were set on 2026-09-08 and are under test.
- Section titles that select a layout: `### Proof bar`, `### Direct answers`, `### Contact
  information`, any title beginning "Where Evolve fits", "Related", "Relevant" or "Where existing",
  `### Featured topics` (Insights hub), and the proof/callout titles: "Approved proof",
  "Approved aggregate experience", "Experience at a glance", "Aggregate experience", "Safety",
  "Experience and safety", "Proof presented accurately", "Proof without project disclosure",
  "Confidentiality is part of professional conduct", "Evolve's role".
- Home page band titles: "Power cannot be treated as a late-stage package" and "The work continues
  after turnover" (they select photographs).
- Sections whose four subsections are numbered `#### 1.`, `#### 2.` render as steps; sections
  whose five subsections are exactly Plan, Design, Build, Power, Maintain render as the lifecycle
  rail; label lines `**Plan:** text` through `**Maintain:** text` render as the lifecycle labels.
  You may rewrite the text after each label; keep the five labels and their order.
- Lines that are only bold text (`**2,200+ mission-critical projects completed**`) are statistics.
  Do not change them.
- Links: keep every `[label](href)` and its href. You may sharpen the label text. Lines of the form
  `[Label](href) — description` render as link cards; keep that pattern.
- `#### Question?` headings under Direct answers must stay questions.
- Sentences that are editorial instructions rather than copy (for example "Add the Careers link
  after…") are removed at build time; leave them exactly as they are or delete them. Do not rewrite
  them into copy.
- Do not add new sections, pages, images or links to pages that do not exist.

## 5. Working method

1. Read the whole page block before touching it.
2. Rewrite section by section: hook the heading, tighten the lead, turn lists into fascinations,
   close with the next step.
3. Run `python3 scripts/validate-copy.py <file>` until it passes. It checks blocked claims, banned
   words, structure and any number that was not in the original.
4. Do not run `build.py` while other writers are working; the site owner rebuilds and deploys.

## 6. Headline formulas used on 2026-09-08 (for reference and testing)

- Outcome without the pain: "Expand or retrofit a live data center without putting the systems
  that are already running at risk."
- Proof-led: "5.3+ GW deployed. Bring power into the data-center plan on day one."
- Contrast: "Commissioning that proves the facility is ready, not paperwork that says it is finished."
- Call-out: "Building for AI density? Here is what has to be settled before design starts."
- Reason-why: "Design-build for data centers, run by people who also have to power and maintain
  what they build."
- Decision framing: "Find out whether your data-center plan can actually be built, powered and
  paid for, before you commit to it."
