# Tension map

This is the 360 view of how one seat's choices land on another department. Each section is a pair of seats; each bullet names a common move by one seat, what it does to the other, and the agreement that usually settles it. Read your own pairs before you propose, and check that any compromise you accept does not quietly break a third seat. Figures are practitioner rules of thumb unless stated otherwise; anything marked (verify) is platform-specific and changes often.

## google-ads + seo
- **If `google-ads` bids on every brand term at full coverage:** paid takes clicks organic would have won for free, and `seo` sees branded organic clicks fall while total brand clicks barely move. Usual agreement: a 2 to 4 week brand holdout in one region or time block, then keep brand bidding only where competitors bid on the name or sitelinks carry offers organic cannot show.
- **If `google-ads` builds noindex conversion pages:** `seo` loses pages that could rank and the site collects thin near-duplicates. Usual agreement: paid pages stay noindex with a canonical to the main page, and winning test copy moves into the indexable page within one cycle.
- **If `seo` holds position 1 to 2 and an AI Overview citation on a non-brand query:** paid on that query may add few incremental clicks. Usual agreement: a monthly paid and organic query overlap report, with lower bids where overlap is high and paid incrementality tests low.
- **If `seo` changes URLs or site structure:** ads land on redirects, tracking parameters can drop, and Quality Score suffers. Usual agreement: `seo` shares the redirect map 5 working days before go-live; `google-ads` updates final URLs the same day.

## google-ads + developer
- **If `google-ads` asks for Enhanced Conversions and offline conversion import:** `developer` must capture click IDs in hidden fields, pass them to the CRM, hash user data and build the upload, typically 5 to 15 working days. Usual agreement: launch on the verified web conversion tag; move to value or pipeline-based bidding only after the import is verified.
- **If `developer` ships a slow landing page:** conversion rate and landing-page experience drop, and cost per conversion rises. Usual agreement: a performance budget as a launch gate, using Google's "good" Core Web Vitals thresholds (LCP under 2.5 s, INP under 200 ms, CLS under 0.1) on mobile.
- **If `google-ads` asks for a landing page per ad group:** `developer` capacity disappears into near-identical pages. Usual agreement: one template with parameter-driven headlines, and hand-built pages only for the top 3 to 5 intents.
- **If `developer` releases site changes without notice:** conversion tags break and Smart Bidding learns from bad data. Usual agreement: tag checks in the release checklist and a shared change log.

## google-ads + ux
- **If `google-ads` sends broad match and Performance Max traffic to one generic page:** `ux` gets visitors with mixed intent and conversion falls. Usual agreement: map ad groups and asset groups to 3 to 5 intent-specific page variants.
- **If `ux` adds qualification steps or a multi-step form:** conversion volume drops and can push a campaign under the roughly 30 conversions in 30 days Smart Bidding needs. Usual agreement: optimise to the step that keeps volume, and feed qualified leads back as a secondary or value signal.
- **If `google-ads` leaves final URL expansion on in Performance Max:** users land on pages `ux` never designed to convert. Usual agreement: URL exclusions, or expansion off for lead generation (verify current controls).

## google-ads + measurement
- **If `google-ads` sets every micro-conversion as primary:** Smart Bidding chases cheap actions and `measurement` reports inflated conversions. Usual agreement: one or two primary conversion actions tied to the KPI; everything else secondary.
- **If `google-ads` runs Performance Max without brand exclusions:** it picks up branded queries Search would have won cheaper, and `measurement` sees PMax ROAS inflated by brand demand. Usual agreement: brand exclusions in PMax, brand and non-brand reported separately (verify current controls).
- **If `measurement` changes conversion definitions or attribution mid-flight:** bidding relearns and week-on-week reports break. Usual agreement: changes only on agreed dates, annotated in reports.
- **If `google-ads` launches in the EEA or UK without consent signals:** `measurement` loses conversion modelling and remarketing lists shrink. Usual agreement: Consent Mode v2 through a certified consent platform before launch (verify).

## google-ads + youtube-video
- **If `google-ads` runs Performance Max:** it can serve on YouTube, with auto-generated video if none is supplied, overlapping `youtube-video` campaigns and muddying reach and frequency. Usual agreement: real video in every asset group and PMax channel reporting reviewed monthly (verify).
- **If `youtube-video` runs awareness video:** branded search volume rises and `google-ads` takes the credit. Usual agreement: track brand search lift in flight weeks and credit video in the plan.
- **If `youtube-video` and `google-ads` both claim Demand Gen:** audiences overlap and budgets compete. Usual agreement: one owner, `youtube-video` for video-first and `google-ads` for image and product-feed Demand Gen, with shared exclusions.

## google-ads + meta-ads
- **If `meta-ads` scales prospecting:** branded search rises and `google-ads` brand CPA improves; both platforms claim the same sale. Usual agreement: dedupe in GA4 or CRM and judge both on blended CAC or incrementality tests.
- **If `google-ads` and `meta-ads` each hold a fixed budget for the whole flight:** money stays in whichever channel is weaker at the margin. Usual agreement: a monthly reallocation rule on marginal CPA, capped at 10 to 15% of the total per move.

## google-ads + copywriter
- **If `google-ads` wants 15 headlines per responsive search ad with no pinning:** `copywriter` loses control of message order and legal lines. Usual agreement: pin only brand or mandatory legal text, and write 10 to 15 headlines by role (keyword, benefit, proof, offer, CTA) so any combination reads well.
- **If `copywriter` pins every position:** ad combinations collapse and Ad Strength drops. Usual agreement: at most two pinned positions, with 2 to 3 variants per pinned slot.
- **If `copywriter` writes without character counts:** headlines over 30 characters and descriptions over 90 are rejected when `google-ads` uploads them. Usual agreement: the copy deck carries a live character count per field (verify limits).

## google-ads + amazon-ads
- **If `google-ads` sends Shopping traffic to the brand site for SKUs that sell mainly on Amazon:** conversion is lower and `amazon-ads` loses organic rank from external sales. Usual agreement: route per SKU by where it converts, and use Amazon Attribution tags on traffic sent to Amazon (verify).
- **If `google-ads` and `amazon-ads` both bid on brand terms:** the client pays twice for the same buyer. Usual agreement: split by destination and intent, and track combined brand cost per sale.
- **If `amazon-ads` raises prices or runs deals:** the Shopping feed and site go out of sync. Usual agreement: a shared promo calendar, and feed updates the same day.

## meta-ads + creative-ops
- **If `meta-ads` asks for 20 new creatives a month:** at 3 ratios and 2 languages that is 120 files, beyond `creative-ops` capacity. Usual agreement: a monthly quota by tier (for example 4 new concepts plus 8 iterations), tests in 4:5 and 9:16 only, full matrix for winners.
- **If `creative-ops` delivers late:** frequency climbs and CPA rises as ads fatigue. Usual agreement: a bank of approved creatives covering at least two weeks of refresh.
- **If `meta-ads` switches on Advantage+ creative enhancements:** automated edits can alter approved assets. Usual agreement: an allowed list signed by `creative-ops` and the brand owner, checked in placement previews (verify defaults).
- **If `meta-ads` renames ads in Ads Manager:** reporting by concept breaks. Usual agreement: names come only from the `creative-ops` convention.

## meta-ads + measurement
- **If `meta-ads` wants conversion-optimised campaigns before the Conversions API is live:** the browser pixel under-reports and the algorithm learns from partial data. Usual agreement: CAPI with event_id deduplication and an acceptable Event Match Quality score before optimising to that event.
- **If `meta-ads` optimises to a shallow event to exit learning:** `measurement` sees cheap traffic that does not convert. Usual agreement: optimise to the deepest event that still reaches about 50 per ad set in 7 days.
- **If `measurement` reports on GA4 last click:** Meta looks weak against its own click and view attribution. Usual agreement: agree the attribution setting, report both views, and use lift tests for big budget decisions.

## meta-ads + creative-strategist
- **If `meta-ads` wants volume and fast iteration:** `creative-strategist` sees the proposition diluted into near-duplicates that Meta's retrieval system may treat as one ad. Usual agreement: 3 to 5 distinct concepts a month plus iterations of the current winner (verify).
- **If `creative-strategist` wants one hero concept with a long lead time:** testing stalls and current ads fatigue. Usual agreement: the hero launches with a fixed test budget and a read date, while iterations keep running.
- **If `meta-ads` judges a concept after two days:** it is killed before it has a signal. Usual agreement: kill rules agreed up front, based on spend against target CPA.

## meta-ads + ux
- **If `meta-ads` uses Instant Forms:** leads bypass the landing page, volume goes up and intent goes down. Usual agreement: test higher-intent form settings with one qualifying question against the landing page, and judge on qualified rate.
- **If `meta-ads` sends Reels traffic to a desktop-first page:** mobile visitors drop off in the first seconds. Usual agreement: a mobile-first first screen that matches the ad's opening frame and offer.
- **If `ux` runs page tests while ad sets are in learning:** conversion rate moves and confounds creative tests. Usual agreement: stagger page tests and creative tests, or run one at a time.

## meta-ads + tiktok-ads
- **If `meta-ads` reuses Reels edits on TikTok:** they look foreign and fatigue faster. Usual agreement: shoot shared raw 9:16 footage, edit natively per platform.
- **If `tiktok-ads` and `meta-ads` target the same young prospecting audience:** they bid against the same attention and both claim the conversion. Usual agreement: split by objective or audience, and judge on blended CAC.

## meta-ads + crm-email
- **If `meta-ads` wants customer lists for exclusions and audience signals:** `crm-email` needs consent status, a signed DPA and a refresh process. Usual agreement: an automated weekly sync of consented lists, with customers excluded from acquisition.
- **If `meta-ads` retargets people already in an email nurture:** they see the same offer in both channels and fatigue or unsubscribe. Usual agreement: shared suppression rules and a message calendar.

## linkedin-ads + ux
- **If `linkedin-ads` uses Lead Gen Forms:** forms prefill from the profile and bypass the landing page, so `ux` cannot educate or qualify, `measurement` loses on-site events, and the CRM fills with low-intent leads. Usual agreement: Lead Gen Forms for content offers with one or two qualifying questions, the landing page for demo requests, both judged on sales-accepted rate.
- **If `ux` puts a long form on the landing page:** CPL climbs on already expensive clicks. Usual agreement: ask only the fields sales uses in the first call, and enrich the rest in the CRM.

## linkedin-ads + client-lead
- **If `linkedin-ads` forecasts a high CPL:** the client pushes back. Usual agreement: targets on cost per sales-accepted lead or pipeline, with a 6 to 8 week read point.
- **If `client-lead` agrees a budget too small for the audiences planned:** campaigns sit near the 10 USD daily minimum and never gather enough data. Usual agreement: fewer campaigns and audiences, or leave LinkedIn out and say why.
- **If `linkedin-ads` plans Thought Leader Ads:** the client's executives must lend their posts and approve quickly. Usual agreement: `client-lead` secures the named executive and an approval SLA before the plan depends on it.

## linkedin-ads + crm-email
- **If `linkedin-ads` collects Lead Gen Form leads without a CRM sync:** leads wait for days, and slow follow-up destroys quality. Usual agreement: a native or middleware sync live before launch, with follow-up inside one working hour.
- **If `crm-email` routes slowly or drops all leads into one generic nurture:** LinkedIn lead quality looks worse than it is. Usual agreement: routing by lead type, a nurture track for content leads, and sales-accepted rate reported per campaign.
- **If `crm-email` does not send outcomes back:** `linkedin-ads` optimises to form fills only. Usual agreement: sales-accepted and opportunity events sent through LinkedIn's Conversions API (verify).

## linkedin-ads + measurement
- **If `linkedin-ads` reports platform leads and view-through conversions:** the numbers do not match the CRM. Usual agreement: the CRM is the source of truth for leads, with view-through reported separately.
- **If `linkedin-ads` launches before the Insight Tag and Conversions API are in place:** `measurement` has no reliable conversion signal, and optimisation and retargeting are weak. Usual agreement: both live and tested before conversion-optimised bidding.
- **If `measurement` uses last click on a long B2B cycle:** LinkedIn looks worthless. Usual agreement: a "how did you hear about us" field plus opportunity influence reporting.

## seo + developer
- **If `seo` asks for technical fixes (Core Web Vitals, rendering, schema, sitemaps):** the `developer` backlog grows. Usual agreement: rank fixes by traffic at stake, bundle them into sprints, ship schema through templates.
- **If `developer` builds pages rendered only in client-side JavaScript:** content may not be crawled or cited by answer engines. Usual agreement: server-side or static rendering for every indexable page.
- **If `developer` migrates the CMS or changes URLs:** traffic can drop for months. Usual agreement: a full redirect map, crawls before and after, and `seo` sign-off 5 working days before go-live.

## seo + ux
- **If `seo` wants long content for topical coverage:** `ux` wants short, scannable pages. Usual agreement: the answer first, then detail in sections or indexable accordions, with jump links.
- **If `ux` removes navigation or internal links to simplify a page:** crawl paths and link equity are lost. Usual agreement: keep crawlable links in breadcrumbs, related links and the footer.
- **If `ux` adds popups or interstitials:** mobile experience and layout stability suffer. Usual agreement: delayed, non-blocking banners only.

## seo + copywriter
- **If `seo` hands over keyword lists with density targets:** `copywriter` produces stiff, repetitive text. Usual agreement: briefs on topics, entities and the questions to answer; no density targets.
- **If `copywriter` writes clever headlines:** titles lose query match, and answer engines favour direct answers. Usual agreement: literal title tags and H1s; creativity in body copy and ads.
- **If `seo` or `copywriter` scales AI-written pages:** the site risks Google's scaled content abuse policy. Usual agreement: expert input, human edit, one quality bar for every page (verify).

## ux + ui
- **If `ui` pushes brand-heavy visuals (hero video, custom fonts):** the page slows and the CTA falls below the fold. Usual agreement: value proposition and CTA in the first mobile screen, hero media within the performance budget.
- **If `ux` wants plain high-contrast forms:** `ui` sees brand drift. Usual agreement: design-system components that meet WCAG 2.2 AA contrast and target size.
- **If `ui` restyles the page for each campaign:** `ux` loses tested patterns. Usual agreement: a tested page template with a brand layer that swaps per campaign.

## ux + developer
- **If `ux` designs complex interactions (calculators, multi-step flows, quizzes):** build time and page weight grow. Usual agreement: ship the simple version first and add the interaction as a tested upgrade.
- **If `developer` embeds a third-party form:** `ux` loses control of validation and error states, and events are hard to track. Usual agreement: a native form, or a form tool that exposes submit and error events.

## ux + crm-email
- **If `ux` cuts form fields to lift conversion:** `crm-email` cannot route or segment the lead. Usual agreement: keep the fields routing needs, enrich the rest after submission.
- **If `crm-email` wants consent checkboxes for every list:** the form gets longer and more confusing. Usual agreement: one clear consent line per purpose, worded with the client's legal team.

## ux + measurement
- **If `ux` designs the consent banner for conversion alone:** dark patterns breach EU and UK rules, and the data becomes a legal risk. Usual agreement: a compliant banner with equal accept and reject options, then optimise wording within the rules.
- **If `ux` runs A/B tests without a tracking plan:** the result cannot be read. Usual agreement: `measurement` defines events and the sample size before a test starts.

## developer + measurement
- **If `measurement` requires server-side tagging and CAPI:** `developer` needs roughly 10 to 20 working days for the server container, subdomain, consent integration and deduplication, and paid seats cannot launch conversion-optimised campaigns until it is verified. Usual agreement: phase 1 browser tags with Consent Mode at launch, phase 2 server-side by a dated milestone, bidding switched once events are verified.
- **If `developer` changes the data layer or form markup:** tags break silently. Usual agreement: `measurement` owns a versioned data layer spec, and every release is tested in staging.
- **If `measurement` asks for dozens of custom events:** the backlog swells. Usual agreement: tier events into must-have (bidding and KPIs) and later.

## developer + ui
- **If `ui` designs a bespoke layout for every page:** development time multiplies. Usual agreement: a component library, with new components only when a requirement needs one.
- **If `developer` simplifies designs for speed:** `ui` sees quality drop. Usual agreement: design review on staging with a short, dated fix list.
- **If `ui` hands over heavy images and multiple font families:** pages slow down. Usual agreement: modern image formats, subset fonts, an image weight budget per page.

## developer + creative-ops
- **If `developer` changes landing URLs after trafficking:** ads break or redirect, and UTMs are lost. Usual agreement: URLs frozen 3 working days before trafficking, changes only through a redirect agreed with `creative-ops`.
- **If `creative-ops` needs HTML5 banners or product feeds for dynamic creative:** `developer` builds the feed or template. Usual agreement: the feed spec agreed at kickoff, one template reused across the flight.
- **If `developer` builds page modules that mirror the ad templates:** `creative-ops` reuses assets and message match improves. Usual agreement: one shared asset library for ads and pages.

## developer + crm-email
- **If `developer` builds forms without hidden fields:** UTMs and click IDs never reach the CRM, and lead source reporting fails. Usual agreement: an integration spec (fields, dedupe, routing webhook) and end-to-end test leads before launch.
- **If `crm-email` changes CRM fields or workflows:** the form integration breaks. Usual agreement: a shared change log and a test lead after each change.

## ui + creative-strategist
- **If `creative-strategist` wants a lo-fi, platform-native look:** `ui` sees brand inconsistency. Usual agreement: fixed distinctive assets (logo, colour, end card) with a native layer that flexes.
- **If `ui` locks rigid templates:** creative diversity drops and near-identical ads compete with each other. Usual agreement: 3 to 4 template families with genuinely different layouts.
- **If `creative-strategist` changes the concept late:** `ui` reworks key visuals. Usual agreement: a concept lock date in the plan.

## ui + creative-ops
- **If `ui` builds a template system (components, auto-layout, safe zones, locked brand elements):** `creative-ops` production time falls sharply, and resizes take minutes instead of hours. Usual agreement: invest template time at campaign start; `creative-ops` resizes within the system without re-approval.
- **If `ui` delivers flattened files:** `creative-ops` cannot resize or localise. Usual agreement: layered source files, named layers, fonts licensed for advertising.
- **If `creative-ops` edits templates ad hoc:** brand drift spreads. Usual agreement: template changes go back to `ui` as a request.

## creative-strategist + creative-ops
- **If `creative-strategist` proposes 8 concepts in 4 ratios and 3 languages:** that is 96 files before variants, beyond `creative-ops` capacity. Usual agreement: tests in 2 ratios and 1 language, full matrix for winners.
- **If `creative-ops` pushes to reuse existing footage:** concepts shrink to what is on the shelf. Usual agreement: flag which concepts need a shoot and budget for them.
- **If `creative-strategist` writes a concept that needs talent or licensed music:** `creative-ops` finds the rights cost and lead time late. Usual agreement: rights needs listed in the concept brief.

## creative-strategist + copywriter
- **If `creative-strategist` writes the final lines too:** `copywriter` is sidelined and platform craft suffers. Usual agreement: the strategist delivers angle, hook intent and proof; the copywriter writes the lines.
- **If `copywriter` drifts from the proposition for a clever line:** the concept loses focus. Usual agreement: every line maps to an angle id.

## creative-strategist + client-lead
- **If `creative-strategist` presents only a bold route:** the client refuses and trust suffers. Usual agreement: a safe and a bold route, the bold one as a funded test.
- **If `client-lead` adds every stakeholder's message:** the proposition dissolves. Usual agreement: one proposition; secondary messages become angles to test.
- **If `client-lead` accepts a long client approval chain:** new concepts from `creative-strategist` miss the refresh window. Usual agreement: a pre-approved message house so iterations inside it skip full approval.

## creative-ops + client-lead
- **If `client-lead` accepts a three-stage approval chain at 3 working days per stage:** every refresh takes 9 working days before production time, against a Meta refresh rhythm of 2 to 4 weeks. Usual agreement: two rounds, batched approvals, and pre-approved templates and claims that skip legal review.
- **If `creative-ops` needs talent and music contracts:** the client often holds them. Usual agreement: `client-lead` collects rights documents at kickoff.

## creative-ops + tiktok-ads
- **If `tiktok-ads` needs refreshes every 7 to 14 days and creator content:** `creative-ops` volume and QA load jump. Usual agreement: a creator pipeline on standard usage terms with a light QA track.
- **If `tiktok-ads` wants trending sounds:** most are not licensed for ads. Usual agreement: only Commercial Music Library or licensed tracks in paid ads (verify).
- **If `tiktok-ads` runs Spark Ads on creator authorisation codes:** the ads stop without warning when a code expires, and `creative-ops` gets the blame. Usual agreement: authorisation expiry dates tracked in the DAM (verify durations).

## measurement + client-lead
- **If `measurement` needs client IT for tagging or consent:** launch slips. Usual agreement: `client-lead` secures a named IT owner and date at kickoff.
- **If `client-lead` promises a report in board metrics the tracking cannot produce:** the first report disappoints. Usual agreement: a reporting spec before launch saying what is measured, what is modelled and what is not available.
- **If `measurement` shows platform numbers and GA4 side by side without explanation:** the client loses confidence and `client-lead` fields the questions. Usual agreement: one named source of truth, explained in the first report.

## client-lead + developer
- **If `client-lead` commits to a launch date before dependencies are known:** `developer` is set up to miss it. Usual agreement: the date is confirmed only after the dependency list.
- **If `developer` waits on client CMS or IT access:** the timeline slips. Usual agreement: an access list at kickoff and a day-for-day slip rule the client accepts.
- **If `client-lead` accepts client changes after build without a change request:** `developer` absorbs unbilled work and dates slip. Usual agreement: a change request with cost and new date.

## copywriter + ux
- **If `copywriter` writes long persuasive copy:** `ux` sees scanning users miss the point. Usual agreement: the headline and CTA match the ad; proof goes in short, scannable blocks.
- **If `ux` wireframes with placeholder text:** real copy does not fit. Usual agreement: content-first wireframes with real headline lengths.
- **If `ux` leaves form labels and error messages to the build:** friction rises at the last step and `copywriter` is never asked. Usual agreement: `copywriter` writes the form microcopy against `ux` rules.

## copywriter + crm-email
- **If `copywriter` writes ad promises that the nurture does not repeat:** leads feel a bait-and-switch. Usual agreement: one message house, and the first email continues the ad's offer.
- **If `crm-email` needs high email volume:** copy capacity is stretched. Usual agreement: modular email templates with reusable blocks per angle.

## tiktok-ads + creative-strategist
- **If `tiktok-ads` follows every trend:** `creative-strategist` sees the proposition vanish. Usual agreement: the trend is the format, the angle stays fixed, and creators get the angle plus brand cues.
- **If `creative-strategist` repurposes TV or Meta assets:** they underperform on TikTok. Usual agreement: native 9:16 builds with a hook in the first second.

## tiktok-ads + measurement
- **If `tiktok-ads` optimises before the Events API is live:** conversion signal is thin. Usual agreement: pixel plus Events API with deduplication before conversion optimisation.
- **If `tiktok-ads` reports view-through conversions:** results look inflated. Usual agreement: report click-based results as primary, and run lift or holdout tests for scale decisions.

## tiktok-ads + client-lead
- **If `tiktok-ads` sends creator content through the full client approval chain:** the trend is gone before it runs. Usual agreement: pre-approved creator guardrails and a 24-hour approval lane.
- **If `client-lead` leaves the client's worries about brand safety or TikTok's regulatory status unanswered:** `tiktok-ads` spend stalls. Usual agreement: safety settings and a written fallback plan (verify market status).

## youtube-video + creative-ops
- **If `youtube-video` plans bumpers, 15 and 30-second cuts, Shorts and CTV:** `creative-ops` faces many cuts and ratios. Usual agreement: a cut-down plan before the shoot, framed for both 16:9 and 9:16.
- **If `youtube-video` books CTV without CTV specs in the asset matrix:** publishers reject files and placements go dark. Usual agreement: CTV specs and loudness checked in QA (verify).

## youtube-video + creative-strategist
- **If `creative-strategist` wants one long hero film:** `youtube-video` needs short cuts and sequences. Usual agreement: an ad sequence with a 6-second hook, a 15-second story, and a longer version for engaged viewers.
- **If `youtube-video` pushes brand-early rules:** the story's reveal is lost. Usual agreement: brand cues in the first 5 seconds without spoiling the idea.

## youtube-video + measurement
- **If `youtube-video` claims view-through conversions:** `measurement` doubts incrementality. Usual agreement: brand lift or conversion lift studies where spend qualifies, plus geo holdouts (verify thresholds).
- **If `measurement` judges video on last click:** awareness looks worthless. Usual agreement: report reach, frequency, lift and branded search lift alongside cost per action.

## programmatic + measurement
- **If `programmatic` reports cheap CPMs and view-through conversions:** `measurement` suspects low-quality inventory. Usual agreement: third-party viewability and invalid traffic verification, made-for-advertising site exclusions, and lift or holdout tests.
- **If `programmatic` adds third-party tags and pixels:** page speed and consent compliance suffer. Usual agreement: all tags through the tag manager, under consent rules.

## programmatic + creative-ops
- **If `programmatic` needs every standard display size plus HTML5 and CTV:** `creative-ops` workload multiplies. Usual agreement: the sizes carrying most impressions first, templated DCO for the rest.
- **If `programmatic` runs creatives through a third-party ad server:** `creative-ops` trafficking steps double. Usual agreement: `creative-ops` trafficks in the ad server and `programmatic` assigns in the DSP from one sheet.

## programmatic + client-lead
- **If `programmatic` buys through a stacked fee chain (DSP, data, verification):** the client sees less working media than expected. Usual agreement: the full fee stack disclosed in the plan.
- **If `programmatic` launches without client-signed safety settings:** any brand safety incident lands on `client-lead` and the relationship. Usual agreement: inclusion lists and safety settings signed by the client before launch.

## programmatic + youtube-video
- **If `programmatic` and `youtube-video` both buy CTV:** they reach the same households and stack frequency. Usual agreement: one CTV owner, shared frequency caps and combined reach reporting.
- **If `programmatic` buys YouTube through a DSP:** it overlaps Google Ads video campaigns. Usual agreement: one buying route for YouTube per flight (verify).

## amazon-ads + creative-ops
- **If `amazon-ads` scales spend before listings are ready:** poor images and missing A+ content waste clicks. Usual agreement: retail readiness (images, A+ content, reviews, stock) checked before scale.
- **If `amazon-ads` needs Sponsored Brands video and custom images:** `creative-ops` gets new specs and a strict policy review. Usual agreement: Amazon assets in the matrix with extra review time (verify specs).

## amazon-ads + client-lead
- **If `amazon-ads` optimises to ACoS alone:** it can starve growth or ignore margin. Usual agreement: TACoS and margin targets agreed with the client.
- **If `amazon-ads` keeps spending while stock runs low:** budget goes on products the client cannot ship. Usual agreement: inventory alerts that pause campaigns, owned by the client's retail team.

## amazon-ads + measurement
- **If `amazon-ads` reports inside Amazon only:** `measurement` cannot see the full path. Usual agreement: Amazon Marketing Cloud for path analysis and TACoS as the blended metric (verify access).
- **If `amazon-ads` receives off-Amazon traffic without attribution tags:** `measurement` cannot credit the channels that drove the sale. Usual agreement: Amazon Attribution tags on external traffic (verify).

## crm-email + measurement
- **If `crm-email` does not store lead source and click IDs:** paid seats cannot receive offline conversions. Usual agreement: hidden-field spec and lifecycle stage definitions agreed at kickoff.
- **If `crm-email` claims revenue that paid also claims:** totals double count. Usual agreement: one attribution rule for the blended report.

## crm-email + client-lead
- **If `client-lead` agrees to email bought or stale lists:** `crm-email` sees deliverability and consent collapse. Usual agreement: consented lists only, with sender authentication, one-click unsubscribe and low spam complaint rates as bulk sender rules require (verify).
- **If `crm-email` hands leads to the client's sales team with no agreed SLA:** follow-up speed is out of the agency's control and `client-lead` owns the fallout. Usual agreement: a written lead SLA signed by the client's sales lead.
- **If `crm-email` shares customer data for platform audiences:** legal exposure for the client, and for `client-lead`, grows. Usual agreement: a DPA and a consent check before any upload.
