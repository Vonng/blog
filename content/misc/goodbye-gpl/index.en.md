---
title: Time to Say Goodbye to the GPL
date: 2021-09-16
showAuthor: false
summary: >
  The real threat to software freedom in the 2020s isn’t shrink-wrapped binaries, it’s cloud software. Copyleft hasn’t kept up; local-first software has a better shot.
tags: [数据库,开源]
---

Originally written by Martin Kleppmann on Apr 14, 2021. Translated to Chinese by me; here’s the English rendition with my commentary. ([Original post](https://martin.kleppmann.com/2021/04/14/goodbye-gpl.html))

> Martin also wrote DDIA; I translated that book into Chinese.

Richard Stallman’s [return to the FSF board](https://www.fsf.org/news/statement-of-fsf-board-on-election-of-richard-stallman) sparked this piece. Many of us signed the [open letter](https://rms-open-letter.github.io/) calling for his removal. The episode forced me to re-evaluate the Free Software Foundation—the steward of GNU and the GPL family. Stallman’s behavior taints that legacy. But my point today isn’t about RMS personally.

**We should move away from the GPL, LGPL, and AGPL**—not because of Stallman, but because the licenses no longer achieve their stated goals and now cause more trouble than value.

GPL’s defining feature is [copyleft](https://en.wikipedia.org/wiki/Copyleft): if you build on GPL code, you must share your derivative work under the same terms. Closed-source vendors can’t absorb GPL code without publishing their changes. That seemed like a clever hack in the 1980s. In 2025 it misses the real enemy.

-------

## The enemy changed

Back then, the villain was Microsoft selling shrink-wrapped binaries. People couldn’t inspect, modify, or fix them; GPL’s goal was to force source releases so users could control their machines. It also scratched a fairness itch: if someone monetized your hobby project without giving back, copyleft forced reciprocity.

Those arguments mattered in 1990. Today the threat isn’t boxed software; it’s cloud software—SaaS running on someone else’s servers, holding all your data. Think Google Docs, Trello, Slack, Figma, Notion.

These apps might ship a thin client, but they only function with the vendor’s backend. Problems abound:

- If the vendor dies or [kills the product](https://killedbygoogle.com/), your documents go with it. Startups get [acquired and sunset all the time](https://ourincrediblejourney.tumblr.com/).
- Platforms like Google can [suspend your account](https://twitter.com/Demilogic/status/1358661840402845696) without notice or appeal. Maybe someone hacked you and tripped an automated rule. Overnight you lose every doc you ever created.
- Software running locally keeps working even if the vendor folds. You can virtualize old OSes if you must. Cloud software dies the moment the provider does.

Copyleft never addressed this. AGPL tried by forcing SaaS providers to publish backend code. They simply refused: they pick permissively licensed alternatives, reimplement features, or [buy commercial licenses](https://www.elastic.co/pricing/faq/licensing). Nothing significant got open-sourced as a result.

-------

## Better legal tools

As a legal strategy, copyleft failed to stop cloud lock-in or meaningfully expand open source. Open source succeeded mostly via permissive licenses (Apache/MIT/BSD). Even Linux’s success would have happened regardless of GPL clauses.

If you want leverage, look to regulation. GDPR’s [right to data portability](https://ico.org.uk/for-organisations/guide-to-data-protection/guide-to-the-general-data-protection-regulation-gdpr/individual-rights/right-to-data-portability/) enshrines the idea that users can move their data between services. Current exports ([Google Takeout](https://en.wikipedia.org/wiki/Google_Takeout)) are crude—ZIPs full of JSON aren’t interoperability. But regulators can push for [real-time, bidirectional data exchange](https://interoperability.news/) between competing vendors.

Similarly, we can lobby governments to [procure open-source, local-first software](https://joinup.ec.europa.eu/sites/default/files/document/2011-12/OSS-procurement-guideline%20-final.pdf) instead of proprietary SaaS. That creates sustainable incentives for companies to build great open software—something license clauses never achieved.

Yes, licenses feel like something individual developers control, whereas regulation sounds out of reach. But how much impact does your license choice truly have? Anyone who dislikes it just doesn’t use your code. Real change requires collective action on the big levers, not solo license theater.

-------

## Other GPL headaches

Forcing companies to publish source doesn’t make them good community citizens. They can dump tarballs without maintaining features, fixing bugs, writing docs, or engaging upstream. Best case useless, worst case a burden on maintainers.

We need people to *want* to contribute—through welcoming communities and incentives—not by wielding legal cudgels.

And GPL-family licenses are notoriously [incompatible with other common licenses](http://gplv3.fsf.org/wiki/index.php/Compatible_licenses). That makes it harder to combine libraries and fragments the ecosystem. If the GPL delivered overwhelming benefits, maybe the pain would be worth it. It doesn’t.

-------

## Conclusion

GPL and copyleft aren’t evil; they’re just pointless now. They have practical issues, they’re tied to an FSF that refuses to evolve, and they don’t protect software freedom. The only companies clinging to copyleft today—[MongoDB](https://www.mongodb.com/licensing/server-side-public-license/faq) and [Elastic](https://www.elastic.co/pricing/faq/licensing)—do it to stop AWS from reselling their services. That’s business, not freedom.

Open source won. The FSF helped kickstart it, but 30 years later the ecosystem moved on while the FSF became [increasingly insular](https://r0ml.medium.com/free-software-an-idea-whose-time-has-passed-6570c1d8218a). By reinstating Stallman and dismissing legitimate criticism, they’re now [actively hurting](https://lu.is/blog/2021/04/07/values-centered-npos-with-kmaher/) the cause.

So let go. Pick a permissive license (MIT/BSD/Apache) for your projects and focus on actions that actually advance software freedom: [build local-first alternatives](https://www.inkandswitch.com/local-first.html), resist cloud lock-in, invent sustainable business models for open source, and push regulators to prioritize users over vendors.

Thanks to [Rob McQueen](https://ramcq.net/) for feedback on the draft.

-------

## References

1. RMS returns: https://www.fsf.org/news/statement-of-fsf-board-on-election-of-richard-stallman
2. Free Software Foundation: https://www.fsf.org/
3. Open letter on RMS: https://rms-open-letter.github.io/
4. GNU project statement: https://www.gnu.org/gnu/incorrect-quotation.en.html
5. GPL overview: https://en.wikipedia.org/wiki/GNU_General_Public_License
6. Copyleft: https://en.wikipedia.org/wiki/Copyleft
7. Derivative works: https://en.wikipedia.org/wiki/Derivative_work
8. Our Incredible Journey: https://ourincrediblejourney.tumblr.com/
9. Google account suspensions: https://www.paullimitless.com/google-account-suspended-no-reason-given/
10. Another suspension example: https://twitter.com/Demilogic/status/1358661840402845696
11. Software archives: https://archive.org/details/softwarelibrary
12. Office Open XML: https://en.wikipedia.org/wiki/Office_Open_XML
13. Photoshop file format spec: https://www.adobe.com/devnet-apps/photoshop/fileformatashtml/
14. Local-first manifesto: https://www.inkandswitch.com/local-first.html
15. AGPL: https://en.wikipedia.org/wiki/Affero_General_Public_License
16. Elastic licensing FAQ: https://www.elastic.co/cn/pricing/faq/licensing
17. Data portability right: https://ico.org.uk/for-organisations/guide-to-data-protection/guide-to-the-general-data-protection-regulation-gdpr/individual-rights/right-to-data-portability/
18. Google Takeout: https://en.wikipedia.org/wiki/Google_Takeout
19. Interoperability News: https://interoperability.news/
20. EU OSS procurement guide: https://joinup.ec.europa.eu/sites/default/files/document/2011-12/OSS-procurement-guideline%20-final.pdf
21. License compatibility: http://gplv3.fsf.org/wiki/index.php/Compatible_licenses
22. MongoDB SSPL FAQ: https://www.mongodb.com/licensing/server-side-public-license/faq
23. Elastic license change Q&A: https://www.elastic.co/pricing/faq/licensing
24. “Free Software: an Idea Whose Time Has Passed”: https://r0ml.medium.com/free-software-an-idea-whose-time-has-passed-6570c1d8218a
25. “Values-Centered NPOs” by Luis Villa: https://lu.is/blog/2021/04/07/values-centered-npos-with-kmaher/
