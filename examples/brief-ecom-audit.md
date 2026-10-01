# Client brief

Example brief for The Marketing Room. Oakhaven Botanics and its competitors are fictional, and the two data files are made up for this example.

## Client and offer (critical)
Oakhaven Botanics (fictional), a direct-to-consumer skincare brand based in Amsterdam, selling fragrance-free products for sensitive skin through its own Shopify store. The range has 14 products: cleansers, serums, moisturisers, and a barrier cream launched in August 2026. Average order value is about 58 EUR, and about 35% of orders come from returning customers.

## Work type (critical)
audit

## Business goal (critical)
Return paid media to profitable growth. In the founder's words: "We are spending more and making less. I need to know what broke and what to fix before Black Friday."

## Objective and KPIs (critical)
- Primary: blended ROAS (platform-reported purchase value across Google and Meta, divided by spend) back to at least 3.0 within 60 days of the fixes starting.
- Blended ROAS fell from 3.8 in March 2026 to 2.1 in September 2026.
- Break-even ROAS: about 2.2 (the client's calculation from a contribution margin of about 45% after product, fulfilment and payment costs).
- Shopify total revenue for September 2026: 131,400 EUR across all channels, including organic and email.
- Secondary: Shopify revenue from paid channels, new-customer share of orders, CPA.

## Budget (critical)
45,000 EUR per month for media across Google Ads and Meta Ads, recently split about 60% Google and 40% Meta. Agency fees are excluded, and the audit is billed separately. No budget for new creative production in October beyond the in-house team.

## Timeline (critical)
- Today: 2026-10-01
- Audit due: 2026-10-09
- 30-day fix plan runs: 2026-10-12 to 2026-11-10
- Black Friday promotion starts: 2026-11-20
- Black Friday: 2026-11-27. Cyber Monday: 2026-11-30.
- Sinterklaas gifting peak in the Netherlands: up to 2026-12-05.
- Any change that resets learning should be live by 2026-11-06 so campaigns are stable before the promotion.

## Geography and language (critical)
Germany, France and the Netherlands. Ads and site in German, French and Dutch; an English version of the site exists but is not advertised. Shopify revenue split for September 2026: Germany 48%, France 31%, Netherlands 21%.

## Audience
Adults aged 25 to 45 with sensitive or reactive skin; about 70% of customers are women. Common purchase triggers are a reaction to a fragranced product, advice from a dermatologist, and recommendations from friends or creators. The most common objection is price compared with pharmacy brands.

## Channels in scope and out of scope
- In scope: the Google Ads account, the Meta Ads account, tracking and consent setup, the product feed, and the product and landing pages that paid traffic lands on.
- Out of scope: email and SMS (Klaviyo, run in-house), TikTok (not running), the affiliate programme, organic social, and SEO beyond the paid landing pages.

## Current state
- Store: Shopify. The product feed goes to Google Merchant Center through the Shopify Google & YouTube app.
- Checkout: moved to Shopify's new checkout and thank-you page in August 2026; the old additional scripts on the order status page were removed at the same time.
- Google Ads: Search (brand and non-brand), Performance Max, Standard Shopping and Demand Gen. Performance Max launched in May 2026 and has taken the largest share of budget since. Which conversion actions count as primary (the Shopify app tag, a GA4 import, or both): unknown. Enhanced Conversions: unknown.
- Meta: browser pixel only, no Conversions API. An Advantage+ shopping campaign launched in June 2026. Attribution setting: 7-day click, 1-day view.
- Consent: a cookie banner shows in all three markets. CMP vendor: unknown. Consent Mode v2 status: unknown.
- GA4: installed through Shopify, not checked since 2025.
- Known changes in the last six months: Performance Max launch (May), budget moved from Standard Shopping into Performance Max (May to June), Advantage+ shopping launch (June), a price rise of about 8% across the range (July), checkout migration and barrier cream launch (August).
- Blended ROAS by month, platform-reported (client figures, no exports before September): March 3.8, April 3.6, May 3.1, June 2.8, July 2.5, August 2.3, September 2.1.

## Assets and resources
- Brand guidelines: yes.
- Creative: about 20 UGC videos from 6 creators (usage rights run to 2026-12-31), product photography, and a set of static ads last refreshed in July 2026.
- Development: a Shopify theme freelancer, 1 day a week.
- In-house: one designer who also covers email and organic social.
- Access: admin access to Google Ads, Meta Business Manager, GA4, Shopify and Merchant Center will be granted for the audit.

## Competitors
All fictional:
- Dermalune: a pharmacy-channel brand, cheaper.
- Hautwerk: a German DTC brand, spends heavily on Meta.
- Soin Clair: a French brand with a strong search presence.

## Mandatories and constraints
- EU cosmetics rules apply: claims must meet Regulation (EC) No 1223/2009 and the common criteria in Regulation (EU) No 655/2013. No medical claims (for example "treats eczema").
- No before-and-after images that imply a medical result.
- GDPR and ePrivacy: marketing tags must respect consent in all three markets.
- Brand search must not be paused without the founder's approval.
- Fixes must not put the Black Friday period at risk; see the 2026-11-06 cut-off above.

## Approvals and stakeholders
- Sign-off: the founder and CEO.
- Day to day: the Head of Growth, who runs both ad accounts in-house today.
- The finance lead supplies margin and Shopify revenue figures.

## Data files and links
These paths are relative to the repository root (the marketing-room folder), not absolute:
- `examples/sample-google-export.csv`: Google Ads campaign report, 2026-09-01 to 2026-09-30, costs and conversion value in EUR.
- `examples/sample-meta-export.csv`: Meta Ads Manager campaign report, 2026-09-01 to 2026-09-30, EUR, attribution setting 7-day click and 1-day view.
- Not supplied: exports for March to August 2026, the search terms report, Performance Max asset group and placement data, Merchant Center diagnostics, and GA4 or Shopify orders by channel.

## Deliverable format
A prioritised audit with a 30-day fix plan: findings ranked by severity, each with its evidence and an owner, and a week-by-week plan the Head of Growth can run. Markdown document.

## Anything else
- The Head of Growth thinks Meta is the problem; the founder thinks Performance Max is. Both want a neutral view.
- The founder also wants to know whether 45,000 EUR per month is still the right budget going into Black Friday.
