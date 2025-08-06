---
title: "It's Time to Say Goodbye to GPL"
date: 2021-09-16
hero: /hero/goodbye-gpl.jpg
author: |
  [Martin Kleppmann Original](https://martin.kleppmann.com/2021/04/14/goodbye-gpl.html) | Translator: [Vonng](https://vonng.com) ([@Vonng](https://vonng.com/en/)) | [WeChat Article](https://mp.weixin.qq.com/s/DJsDRO18saZaxe3oyzzYrA)
summary: >
  This article argues that in 2020, the enemy of computing freedom is **cloud software**, and advocates for the concept of **local-first software**.
tags: [database,opensource]
---

Original article published by Martin Kleppmann on April 14, 2021, translated by Vonng.

> Martin Kleppmann is the author of "Designing Data-Intensive Applications" (a.k.a DDIA), and translator Vonng is the Chinese translator of this book.

The catalyst for this article was Richard Stallman's [reinstatement](https://www.fsf.org/news/statement-of-fsf-board-on-election-of-richard-stallman), a [controversial figure](https://rms-open-letter.github.io/) for the board of the [Free Software Foundation](https://www.fsf.org/) (FSF). I was appalled by this and joined others in calling for his removal. This incident made me reassess the Free Software Foundation's position in the computing world — it is the steward of the GNU project ([broadly speaking](https://www.gnu.org/gnu/incorrect-quotation.en.html) part of Linux distributions) and the family of software licenses centered on the [GNU General Public License](https://en.wikipedia.org/wiki/GNU_General_Public_License) (GPL). These efforts are unfortunately tainted by Stallman's behavior. **However, that's not what I really want to discuss today**.

In this article, I argue that **we should move away from GPL and related licenses** (LGPL, AGPL), for reasons unrelated to Stallman, simply because I believe they fail to achieve their purpose and cause more trouble than they're worth.

First, a brief background: The defining characteristic of GPL-family licenses is the concept of [copyleft](https://en.wikipedia.org/wiki/Copyleft), which states that if you use some GPL-licensed code and modify or build upon it, you must also make your modifications/extensions available for free under the same license (called "[derivative works](https://en.wikipedia.org/wiki/Derivative_work)") (roughly speaking). This way, GPL source code cannot be incorporated into closed-source software. At first glance, this seems like a good idea. So what's the problem?

[![featured.jpg](featured.jpg)](https://mp.weixin.qq.com/s/DJsDRO18saZaxe3oyzzYrA)

------

## The Enemy Has Changed

In the 1980s and 1990s, when GPL was created, the enemies of the free software movement were Microsoft and other companies selling closed-source ("proprietary") software. GPL was intended to undermine this business model, primarily for two reasons:

1. Closed-source software is not easily modifiable by users; you can use it or not, but you can't modify and customize it according to your needs. To counter this, GPL was designed to force companies to release the source code of their software, so that software users could study, modify, compile, and use their own customized versions, thereby gaining the freedom to customize their computing devices as needed.

2. Additionally, GPL was motivated by a desire for fairness: if you write some software in your spare time and release it for free, but others profit from it without giving anything back to the community, you wouldn't want that to happen. Mandating that derivative works be open source ensures at least some bottom-line "return."

These reasons made sense in 1990, but I believe the world has changed, and closed-source software is no longer the main problem. **In 2020, the enemy of computing freedom is cloud software** (also known as: Software as a Service/SaaS, also known as Web Apps) — software that runs primarily on vendors' servers, with all your data stored on those servers. Typical examples include: Google Docs, Trello, Slack, Figma, Notion, and many other applications.

These "cloud software" applications may have a client component (mobile app, web app, JavaScript running in your browser), but they only work in conjunction with the vendor's server-side. Cloud software has many problems:

- If the company providing cloud software goes out of business or decides to [discontinue](https://killedbygoogle.com/) the service, the software stops working, and the documents and data you created with this software become locked away. This is a common problem for software written by startups: these companies may be [acquired by large corporations](https://ourincrediblejourney.tumblr.com/), and the large corporations have no interest in continuing to maintain these startup products.
- Google and other cloud services may [suddenly suspend your account](https://twitter.com/Demilogic/status/1358661840402845696) without any warning or [recourse](https://www.paullimitless.com/google-account-suspended-no-reason-given/). For example, you might be completely innocent but be automatically flagged by automated systems for violating terms of service: others might hack your account and use it to send malware or phishing emails without your knowledge, triggering terms of service violations. As a result, you might suddenly find that all documents you created with Google Docs or other apps are permanently locked away and inaccessible.
- Software that runs on your own computer can continue to work forever, even if the software vendor goes bankrupt. (If the software is no longer compatible with your operating system, you can also run it in virtual machines and emulators, provided it doesn't need to contact servers to check licenses). For example, the Internet Archive has a [collection of over 100,000 historical software programs](https://archive.org/details/softwarelibrary) that you can run in emulators in your browser! In contrast, if cloud software is shut down, you have no way to preserve it because you never had a copy of the server-side software, whether source code or compiled form.
- The problem of not being able to customize or extend the software you use, which was an issue in the 1990s, is further exacerbated with cloud software. For closed-source software running on your own computer, at least someone could reverse-engineer its data file formats so you could load them into other alternative software (such as Microsoft Office file formats before [OOXML](https://en.wikipedia.org/wiki/Office_Open_XML), or Photoshop files before the [specification](https://www.adobe.com/devnet-apps/photoshop/fileformatashtml/) was published). With cloud software, even this is impossible because data is only stored in the cloud, not in files on your own computer.

If all software were free and open source, these problems would all be solved. However, open source is actually not a necessary condition for solving cloud software problems; even closed-source software can avoid the above problems as long as it runs on your own computer rather than on vendor cloud servers. Note that the Internet Archive can keep historical software running without source code: if it's just for archival purposes, running compiled machine code in emulators is sufficient. Perhaps having source code would make things easier, but it's not critical — the most important thing is to have a copy of the software.

------

## Local-First Software

My collaborators and I have previously advocated for the concept of [local-first software](https://www.inkandswitch.com/local-first.html), which is a response to these problems with cloud software. Local-first software runs on your own computer, stores its data on your local hard drive, while also retaining the conveniences of cloud software, such as real-time collaboration and data synchronization across all your devices. Open-source local-first software is certainly great, but it's not necessary — 90% of the benefits of local-first software also apply to closed-source software.

Cloud software, not closed-source software, is the real threat to software freedom, because cloud vendors can suddenly lock away all your data on a whim, which is far more harmful than not being able to view and modify your software's source code. Therefore, promoting local-first software is more important and urgent. If in this process we can also make more software open source, that's great, but it's not that critical. We should focus on the most important and urgent challenges.

------

## Legal Tools for Promoting Software Freedom

Copyleft software licenses are legal tools that attempt to force more software vendors to open their source code. [AGPL](https://en.wikipedia.org/wiki/Affero_General_Public_License) in particular tries to force cloud vendors to release the source code of their server-side software. However, this doesn't work: most cloud vendors simply refuse to use AGPL-licensed software: they either use alternative implementations with more permissive licenses, re-implement the necessary functionality themselves, or directly [purchase a commercial license without copyright restrictions](https://www.elastic.co/pricing/faq/licensing). Some code will never be open regardless, and I don't think these licenses really make any previously closed software become open source.

As legal tools for promoting software freedom, I believe copyleft has largely failed, because they've done nothing to prevent the rise of cloud software, and may not even be useful in promoting the growth of open source software share. Open source software has been very successful, but this success mostly belongs to non-copyleft projects (such as Apache, MIT, or BSD licenses). Even in GPL-licensed projects (such as Linux), I doubt whether copyright aspects are really important factors in the project's success.

For promoting software freedom, I believe more promising legal tools are government regulation. For example, GDPR introduced the [right to data portability](https://ico.org.uk/for-organisations/guide-to-data-protection/guide-to-the-general-data-protection-regulation-gdpr/individual-rights/right-to-data-portability/), which means users must be able to transfer their data from one service to other services. Existing portability implementations, such as [Google Takeout](https://en.wikipedia.org/wiki/Google_Takeout), are quite primitive (what can you really do with a bunch of JSON archive files?), but we can lobby regulators to [push for better portability/interoperability](https://interoperability.news/), such as requiring two competing vendors to implement real-time bidirectional synchronization of your data between their two applications.

Another promising avenue is pushing for [public sector procurement to favor open source, local-first software](https://joinup.ec.europa.eu/sites/default/files/document/2011-12/OSS-procurement-guideline-final.pdf) over closed-source cloud software. This creates positive incentives for businesses to develop and maintain high-quality open source software, while copyright clauses do not.

You might argue that software licenses are something individual developers can control, while government regulation and public policy are bigger issues beyond any individual's power. Yes, but how much impact can your choice of a software license have? Anyone who doesn't like your license can simply choose not to use your software, in which case your power is zero. Effective change comes from collective action on big problems, not from one person's small open source project choosing one license over another.

------

## Other Problems with GPL-Family Licenses

You can force a company to provide source code for their GPL derivative software projects, but you can't force them to be good citizens of the open source community (for example, continuously maintaining features they add, fixing bugs, helping other contributors, providing good documentation, participating in project management). If they're not really engaged in the open source project, what's the use of this source code "thrown in your face"? At best, it's worthless; at worst, it's harmful because it shifts the maintenance burden to other contributors of the project.

We need people to become excellent open source community contributors, and this is achieved by maintaining an open and welcoming attitude and building the right incentive mechanisms, not through software licenses.

Finally, a practical problem with the GPL license family is that they are [incompatible with other widely used licenses](http://gplv3.fsf.org/wiki/index.php/Compatible_licenses), making it more difficult to use certain combinations of libraries in the same project and unnecessarily fragmenting the open source ecosystem. If GPL licenses had other strong advantages, maybe this problem would be worth tolerating. But as stated above, I don't believe these advantages exist.

------

## Conclusion

GPL and other copyleft licenses aren't bad, I just think they're pointless. They have practical problems and are tainted by FSF's behavior; but most importantly, I don't think they make effective contributions to software freedom. The only commercial software vendors now actually using copyleft ([MongoDB](https://www.mongodb.com/licensing/server-side-public-license/faq), [Elastic](https://www.elastic.co/pricing/faq/licensing)) — they want to prevent Amazon from offering their software as a service, which is certainly fine, but this is purely for commercial considerations, not software freedom.

Open source software has achieved tremendous success, and the free software movement that originated from 1990s anti-Microsoft sentiment has come a long way. I acknowledge that the Free Software Foundation played an important role in getting all this started. However, 30 years have passed, the ecosystem has changed, but the Free Software Foundation hasn't kept up and has [become increasingly out of touch](https://r0ml.medium.com/free-software-an-idea-whose-time-has-passed-6570c1d8218a). It has failed to provide a clear response to cloud software and other recent threats to software freedom, just continuing to repeat decades-old talking points. Now, by restoring Stallman's position and dismissing concerns about him, the FSF is [actively harming](https://lu.is/blog/2021/04/07/values-centered-npos-with-kmaher/) the cause of free software. We must distance ourselves from the FSF and their worldview.

Based on all these reasons, I think holding onto GPL and copyleft no longer makes sense — let it go. Instead, I would encourage you to adopt a permissive license for your projects (such as [MIT](https://opensource.org/licenses/MIT), [BSD](https://opensource.org/licenses/BSD-2-Clause), [Apache 2.0](https://opensource.org/licenses/Apache-2.0)), and then focus your energy on things that can actually make a difference for software freedom. [Resist](https://www.inkandswitch.com/local-first.html) the monopolistic effects of cloud software, develop sustainable business models that allow open source software to thrive, and push for regulation that puts software users' interests above vendors' interests.

* Thanks to [Rob McQueen](https://ramcq.net/) for feedback on a draft of this post.

------

## References

1. RMS Reinstatement: https://www.fsf.org/news/statement-of-fsf-board-on-election-of-richard-stallman
2. Free Software Foundation Homepage: https://www.fsf.org/
3. Open Letter to Remove RMS: https://rms-open-letter.github.io/
4. GNU Project Statement: https://www.gnu.org/gnu/incorrect-quotation.en.html
5. GNU General Public License: https://en.wikipedia.org/wiki/GNU_General_Public_License
6. Copyleft: https://en.wikipedia.org/wiki/Copyleft
7. Definition of Derivative Work: https://en.wikipedia.org/wiki/Derivative_work
8. x.ai acquired by Bizzabo: https://ourincrediblejourney.tumblr.com/
9. Google Account Suspended No Reason Given: https://www.paullimitless.com/google-account-suspended-no-reason-given/
10. Google suspending user accounts: https://twitter.com/Demilogic/status/1358661840402845696
11. Internet Archive Historical Software Collection: https://archive.org/details/softwarelibrary
12. Office Open XML: https://en.wikipedia.org/wiki/Office_Open_XML
13. Photoshop File Formats Specification: https://www.adobe.com/devnet-apps/photoshop/fileformatashtml/
14. Local-First Software: https://www.inkandswitch.com/local-first.html
15. AGPL License: https://en.wikipedia.org/wiki/Affero_General_Public_License
16. Elastic Commercial License: https://www.elastic.co/pricing/faq/licensing
17. Right to Data Portability: https://ico.org.uk/for-organisations/guide-to-data-protection/guide-to-the-general-data-protection-regulation-gdpr/individual-rights/right-to-data-portability/
18. Google Takeout: https://en.wikipedia.org/wiki/Google_Takeout
19. Interoperability News: https://interoperability.news/
20. EU Open Source Software Procurement Guide: https://joinup.ec.europa.eu/sites/default/files/document/2011-12/OSS-procurement-guideline-final.pdf
21. License Compatibility: https://gplv3.fsf.org/wiki/index.php/Compatible_licenses
22. MongoDB SSPL License FAQ: https://www.mongodb.com/licensing/server-side-public-license/faq
23. Elastic License Change FAQ: https://www.elastic.co/pricing/faq/licensing
24. "Free Software": An Idea Whose Time Has Passed: https://r0ml.medium.com/free-software-an-idea-whose-time-has-passed-6570c1d8218a
25. A Path FSF Never Envisioned: https://lu.is/blog/2021/04/07/values-centered-npos-with-kmaher/