---
title: "The World in Ten Years: What Gets Cheap, What Gets Expensive"
date: 2026-08-16
author: |
  [Ruohang Feng](https://vonng.com) ([@Vonng](https://vonng.com/en/))
summary: >
  Starting with the price curve of AI inference, this essay projects how the world will be repriced by 2036: intelligence will become as cheap and ubiquitous as electricity, while electricity itself, trust, accountability, attention, physical presence, and judgment become the truly scarce goods.
tags: [AI, Future]
ai_generated: 99
---

> A price list for 2036

AI-generated content: 99%.

## 1. First, a Word on Prediction

In 1960, Herbert Simon wrote a sentence in *The New Science of Management Decision* that would be quoted for decades: within twenty years, machines would be capable of doing any work a person could do. The line later appeared in his 1965 book *The Shape of Automation for Men and Management* ([Quote Investigator traced its origin](https://quoteinvestigator.com/2020/11/11/ai-can-do/)). Ten years later, Marvin Minsky was even more specific in an interview with *Life*: [within three to eight years, we would have a machine with the general intelligence of an average human being](https://en.wikiquote.org/wiki/Marvin_Minsky)—one that could read Shakespeare, grease a car, play office politics, tell a joke, and get into a fight.

These men were not cranks. Simon later won both the Turing Award and the Nobel Memorial Prize in Economic Sciences. Minsky was one of the four organizers of the 1956 Dartmouth workshop and also a Turing Award winner. They were wrong by half a century.

Now consider 1965. Gordon Moore published a four-page article in *Electronics* and [drew a line](https://www.cs.utexas.edu/~fussell/courses/cs352h/papers/moore.pdf): the number of components on an integrated circuit would double at regular intervals, driving down the cost per component. He also ventured a specific number. By 1975, he wrote, it might be economical to put 65,000 components on a single integrated circuit. Ten years later, a new memory chip contained 65,536—[an error of less than one percent](https://www.intel.com/content/www/us/en/history/virtual-vault/articles/moores-law.html).

Moore described no futuristic scene. No personal computers, no internet, no mobile phones. He simply drew a price curve, and that curve held for sixty years.

There is a lesson here that I find more valuable than any specific technological forecast: **predictions about form are almost always wrong; predictions about price are often right.**

Form comes from imagination, and imagination is constrained by what you have already seen. A century ago, people imagining the future of transportation could picture "flying," but not "horseless." They drew carriages with wings. Prices are different. They emerge from physics and economics and follow rules that are duller, harder, and more dependable: capacity ramps up, learning curves drive costs down, efficiency improves, and bottlenecks move.

So this essay will not describe any dazzling scene from 2036. I do not know what interfaces will look like, whether humanoid robots will be able to turn a screw, or who will win. I want to do just one thing: draw up a price list for 2036. Which price tags will disappear, and which will soar?

---

## 2. The Collapse Zone: Thought Becomes a Consumable

Let us start with the category that will collapse. It contains only one item, but it is a large one: intelligence.

Consider a few numbers. In December 2022, the cheapest API offering GPT-3.5-class performance cost $20 per million tokens. By August 2024, Gemini 1.5 Flash reached the same performance threshold for $0.075. Tsinghua University's paper on the ["Densing Law"](https://arxiv.org/pdf/2412.04315) did the math: a 266.7-fold decline, equivalent to a halving every 2.6 months.

That was not an isolated case. Epoch AI systematically tracked price curves across multiple benchmarks. Its conclusion: [the lowest inference price required to reach a given capability milestone is falling by a factor of 9 to 900 per year](https://epoch.ai/data-insights/llm-inference-price-trends), depending on the capability tier. A paper published this March combined real-time prices for 318 models on OpenRouter, 3,237 model records in Epoch's database, and 62 cross-validated milestone points. [It found that token prices fell by a factor of roughly 600 overall between 2020 and 2026](https://arxiv.org/html/2603.28576v1). Budget models had a price half-life of 1.10 years; mid-tier models, 1.55 years. Both are much faster than Moore's two-year doubling rate.

The same paper contains another, more interesting finding that deserves to stand alone: **flagship model prices have barely fallen at all.** The exponential fit has an R² of just 0.031—essentially noise. The reason is that the frontier keeps spending more compute on reasoning and longer chains of thought. On average, reasoning models cost 31.5 times as much as non-reasoning models.

Put those two observations together and the basic shape of intelligence pricing over the next decade becomes clear: yesterday's frontier will become as cheap as tap water, while today's frontier will always be painfully expensive.

So stop asking when AI will become free. The frontier of a generation ago will always be free; today's frontier will always carry a price. The three-to-five-year gap between them will be one of the most important dividing lines in the entire industry ten years from now.

Let us make a conservative extrapolation. Ignore the tenfold annual declines of the bubble years and assume only a threefold decline per year. If that pace holds for a decade, the same capability will cost roughly 1/60,000 of today's price. In 2036, one cent will buy 600 times as much thought as one dollar buys today.

At that point, asking how much intelligence an operation consumes will be like asking how much electricity it takes to open the refrigerator door. It will no longer be a meaningful question.

At 3 p.m. on September 4, 1882, Edison had an operator close the switch at his Pearl Street station in New York. [The station demonstrated a complete, commercially viable central power system to the public](https://ethw.org/Milestones:Pearl_Street_Station,_1882), serving 85 customers across 0.65 square kilometers on its first day. Electricity was then a luxury, used to light wealthy parlors and the stock exchange. By the 1930s, people no longer debated whether to use electricity. It had faded into the background, something you noticed only when it went out.

Intelligence will follow the same path. It will not become a product. It will become a utility: metered, available on demand, and crippling when interrupted.

An enormous class of work will fall in price with it, approaching the cost of electricity. The criterion is simple: any task that consists primarily of rearranging existing knowledge into a requested format belongs on the list. Routine legal documents, translation, initial medical triage, homework help, financial-report summaries, audit workpapers, most graphic design, and most application software development.

That does not mean these professions will disappear. It means the basis for what they can charge will no longer be "I have mastered this craft." It will be something else. What that something is will occupy the second half of this essay.

For the first time in human history, thought is not scarce. It is a consumable input.

---

## 3. Jevons's Curse: The Cheaper It Gets, the Bigger the Bill

But do not confuse a collapsing unit price with spending less money.

In 1865, William Stanley Jevons published [*The Coal Question*](https://oll.libertyfund.org/titles/jevons-the-coal-question). The prevailing British view was that Watt's more efficient steam engine would naturally conserve coal. Jevons said they had it exactly backward: using fuel more efficiently did not mean using less of it. Greater efficiency would make coal cheaper and useful for more things, driving up demand until Britain burned more coal than before.

He was right. The mechanism later became known as the [Jevons paradox](https://en.wikipedia.org/wiki/Jevons_paradox), and it has recurred across many fields over the past 160 years. More fuel-efficient engines brought more cars and longer commutes. Cheaper bandwidth brought 4K and short-form video. Cheaper storage brought a world in which nobody deletes photos anymore.

Now it is intelligence's turn, and the effect is already visible. Menlo Ventures' annual report shows that [enterprise spending on generative AI rose from $11.5 billion to $37 billion in a single year, more than tripling](https://menlovc.com/perspective/2025-the-state-of-generative-ai-in-the-enterprise/). Look back just six months and the jump is even more striking: enterprise spending on LLM APIs [rose from $3.5 billion at the end of 2024 to $8.4 billion by mid-2025](https://menlovc.com/2025-mid-year-llm-market-update/), more than doubling in half a year. Unit prices are collapsing; total bills are soaring.

The reason is no mystery. When one call falls from a dollar to a cent, you do not pocket the other ninety-nine cents. You start doing things that were previously unthinkable: letting an agent break down its own task, call tools, verify its own work, and try again. A single "thought" may cost thirty times as much as an "answer," yet you will ask the system to think ten times as often. That is how the 31.5-fold reasoning premium gets absorbed.

**Technological revolutions are never really about doing the same thing at lower cost. They are about starting to do things that were never worth doing before.**

Two examples show how far the boundary of "not worth it" will move.

In the past, writing a separate application for every user was absurd because labor costs made it impossible. Ten years from now, it will be the default. Every piece of software you use will be generated for you on the spot and discarded when you are done. It will have no version number, no changelog, and no product manager promising that your feature will arrive in the next release.

In the past, it was absurd to cross-check all of a company's meeting notes, contracts, emails, and code commits from the previous twenty years and find every contradiction. You could never hire enough people. Ten years from now, it will be a weekly routine, as ordinary as a routine physical is today.

I once wrote in another essay: any system sustained only because nobody will check it exhaustively will collapse. This section is the economic basis for that claim. Efficiency never saves resources. It simply pushes the frontier of desire one step farther out.

---

## 4. The Bill Is Paid in Electricity

All right: the bill gets bigger. Where does the money ultimately go?

Into an exceptionally unglamorous, heavy-industrial input: electricity.

Once intelligence becomes a utility, it must obey the physical laws that govern utilities. Those laws are not negotiable.

Start with the scale. In its 2026 update, the IEA projected that [global data-center electricity consumption would nearly double from 485 TWh in 2025 to about 950 TWh in 2030, or roughly 3% of global electricity demand; consumption by AI-focused data centers would rise from 155 TWh to 465 TWh](https://www.iea.org/reports/key-questions-on-energy-and-ai/executive-summary). Put differently, AI's share of data-center electricity use would rise from less than one-third to nearly half. Gartner is more aggressive. It [expects peak power demand from data centers worldwide to rise from 104 GW in 2025 to 132 GW in 2026 and 290 GW by 2030](https://www.gartner.com/en/newsroom/press-releases/2026-06-10-gartner-says-data-center-electricity-demand-to-grow-26-percent-in-2026), and says so explicitly: AI capacity is now constrained by the availability of electricity.

One number is worth remembering because it makes the scale vivid. The IEA says capital spending by technology giants exceeded $400 billion in 2025 and is expected to rise another 75% in 2026. [The combined capital spending of five technology companies now exceeds total global investment in oil and gas production](https://www.iea.org/reports/key-questions-on-energy-and-ai/executive-summary). An industry built on buying electricity now spends more than the entire industry that extracts the world's oil. That fact alone shows how tight supply and demand have become.

But generation is not the only bottleneck. Given enough money and time, new power plants can be built. For a specific project, the harder problem is often this: **you cannot get a grid connection.**

Consider a few numbers:

- Transformers. Before the pandemic, lead times were measured in months. By [the second quarter of 2025, average lead times had reached 128 weeks for power transformers and 143 weeks for generator step-up transformers](https://www.woodmac.com/ja/news/opinion/mind-the-gap-tackling-supply-chain-challenges-in-the-electric-td-sector/). Some specialized units are now [quoted at four years](https://pv-magazine-usa.com/2026/05/11/u-s-transformer-market-faces-severe-supply-constraints-as-lead-times-extend-to-four-years/). Wood Mackenzie estimates that the 2025 supply gap for power transformers was about 30%, while demand for generator step-up transformers had risen 274% from 2019.
- Want to bypass the grid and generate your own power? The line for gas turbines is longer still. By the second quarter of 2026, GE Vernova had [116 GW of contracts and slot reservations in its backlog, against annual production capacity of 20 GW, with a plan to reach only 30 GW by 2030](https://www.sec.gov/Archives/edgar/data/0001996810/000199681026000147/gev2q2026form8-k.pdf). Delivery slots [are already booked through 2031](https://solmarcapital.co/ge-vernova-gas-turbine-backlog-data-center-demand/). Siemens Energy's [lead times likewise start at three years](https://energynewsbeat.co/electrical-generation/siemens-gas-turbine-backlog-nears-70-gw-as-company-expands-manufacturing/). Prices have naturally followed. Wood Mackenzie expects gas-turbine quotes to reach $600 per kilowatt by the end of 2027, [roughly three times their 2019 level](https://www.power-eng.com/gas/turbines/data-centers-drive-record-surge-in-ge-vernova-power-equipment-orders-as-turbine-slots-tighten-through-2030/).
- The interconnection queue. At the end of 2025, about [2.06 TW of generation and storage capacity was still waiting in US interconnection queues](https://emp.lbl.gov/news/backlog-power-plants-seeking-transmission-grid-connection-eased-somewhat-2025-amidst)—more than the country's entire installed capacity. The median time from application to commercial operation now exceeds five years. The IEA estimates that unless grid constraints are resolved, [about 20% of planned data-center projects risk delay](https://www.iea.org/reports/energy-and-ai/executive-summary). In advanced economies, a new transmission line takes four to eight years to build.

The cost structure is the interesting part. According to Bloomberg, [critical electrical equipment such as transformers, switchgear, and batteries accounts for less than 10% of a data center's construction cost](https://www.bloomberg.com/news/newsletters/2026-04-01/us-data-center-boom-relies-on-hard-to-find-electrical-equipment). Less than a tenth of the budget determines whether the other nine-tenths can come online. NVIDIA is shipping; the transformer is stuck at the gate.

Once you understand that, you can see how the world map will be redrawn over the next decade.

The last decade was a contest for chips. The next will be a contest for electricity. And the playing field looks very different. In 2025, [China's total electricity consumption reached 10.3682 trillion kWh, crossing 10 trillion for the first time](https://www.nea.gov.cn/20260121/715f79826488476a9162da7c8bd77c80/c.html). That was [more than twice annual US consumption and greater than the combined consumption of the European Union, Russia, India, and Japan](https://www.ndrc.gov.cn/wsdwhfz/202602/t20260204_1403586_ext.html). In the same year, [China's installed generation capacity reached 3.89 TW, up 16.1% year over year; combined wind and solar capacity also surpassed thermal-power capacity for the first time](https://www.nea.gov.cn/20260212/d9f714e91a7f40d39282d87e384ea94a/c.html).

This is not a victory lap. More electricity does not automatically mean more compute. Chips, software ecosystems, and many other things still lie between them. My point is different: in a world where intelligence is billed by the kilowatt-hour, the ability to turn a 1 GW plan into stable current at the rack within three years will become a core national capability.

This is not a software problem. It is about electrical steel, ultra-high-voltage transmission, land acquisition, environmental review, substation construction crews, and tens of thousands of licensed electricians. It is a contest over who can actually get things built—a test of the least glamorous, heaviest kind of capability.

Ten years from now, compute will follow electricity-price contours the way aluminum smelters did in the last century—toward Inner Mongolia, western China, the Middle East, Iceland, and anywhere else with cheap, stable power. Data centers will become heavy industry in the fullest sense, with all the familiar features: capital intensity, long cycles, local protectionism, environmental disputes, job creation, and small towns that rise and fall with the industry.

As an aside, a coupled electricity-compute futures market will probably emerge within a decade, along with carbon labels for compute and specialist schedulers that arbitrage green electricity by moving workloads. All of these can be read directly from today's curves.

---

## 5. The First Thing to Get More Expensive: Trust

That covers what collapses. Now for the longer list of things that will rise in price.

The first is trust. The chain of logic is short: the cost of producing an article approaches zero, while the cost of reading one does not change at all.

A day still contains 24 hours. You are still awake for roughly sixteen of them. A passage still takes minutes to read, and getting deceived still costs real money. Supply becomes infinite while human capacity on the demand side remains fixed. That mismatch must create a new scarce good.

That scarce good is credibility. The things that gain value will be those that can answer two questions: **Who said this? Who pays if it is wrong?**

Signatures, provenance, audit trails, identity verification, responsible parties, professional license numbers, notarization, timestamps, and tamper-resistant records. These things look spectacularly dull and bureaucratic today. Over the next decade, they will become the most valuable layer of infrastructure.

I work with databases every day, so I want to dwell on this point. It has far more to do with my field than most people realize.

The purpose of a database has never been merely to "store data." A file can do that. A database exists to provide a ledger everyone accepts in a world where anyone can misremember, lie, or deny what they did.

Of the four letters in ACID, the most valuable in the future will be neither atomicity nor isolation, but D: [durability](https://www.postgresql.org/docs/current/tutorial-transactions.html), the guarantee that a committed result will not simply vanish because the system failed. Durability alone does not provide non-repudiation. Only when a durable record is combined with digital signatures, audit trails, and access controls can it serve as a ledger whose entries cannot be repudiated.

Take the idea into daily life. Ten years from now, "human-made" will be a label much like "organic," "handmade," or a protected designation of origin today. It will come with certification regimes, price premiums, and an entire suite of detection techniques. It will, of course, also produce rampant counterfeiting and endless litigation.

---

## 6. The Second Thing to Get More Expensive: Accountability

The second item is more concrete than trust, and a little darker.

An AI cannot be sued, imprisoned, bankrupted, or made to take an oath in court. You cannot make a probability distribution answer for misdiagnosing your cancer.

This is not a technical problem. It is a jurisprudential one, and it will not be solved within a decade. The foundation of the modern legal system is that responsibility must ultimately attach to a natural person, a legal person, or another entity recognized by law. Try to change that foundation and you are moving a load-bearing wall of civilization.

The conclusion is clear: people will not disappear from any step that requires someone to bear responsibility. They will become more expensive.

But the work they perform in those roles will change.

A doctor's value will shift from "I know what disease this is" to "I sign my name confirming what disease this is." A lawyer's value will shift from "I can find the relevant precedent" to "I stake my professional license on this opinion." An engineer's value will shift from "I can write this code" to "I am willing to sign off on this code going into production."

**Ten years from now, capability will not command the highest price; accountability will. A person who can be sued will be worth more than a machine that is almost never wrong.**

At this point, we have to confront the dark side, because it is the part I worry about most.

In any organization, responsibility rolls downhill along the power gradient until it reaches the person with the least bargaining power.

That will produce a typical—and brutal—job in the next decade: the AI recommends; the human signs. A modestly paid employee will bear all the legal consequences of decisions made by a model valued in the hundreds of billions. The system captures every efficiency gain; the person signing the document carries the risk.

The role will even become institutionalized. It will have dedicated professional qualifications, insurance products, and actuarial models for liability coverage. The titles will sound impressive: AI Output Review Specialist, AI Systems Compliance Officer.

In plain English: the designated fall guy.

This is not alarmism. It is the natural outcome of extrapolating today's incentive structure over another decade. The reviewer's only protection is the ability to understand the output—and therefore to refuse to sign. A reviewer who cannot say "I won't sign this" is legally disposable.

---

## 7. The Third Category to Get More Expensive: Attention, Bodies, and Atoms

The third category contains the more prosaic increases.

**Attention.** The amount each person can allocate in a day is nearly constant, while the supply of content is exploding. The price must rise. This is elementary arithmetic. Ten years from now, the war for attention will be an order of magnitude more brutal than it is today, because the competition will no longer consist of a few thousand content teams. It will be infinite.

**Physical presence.** Concerts, theater, sporting events, eating together in person, and hands-on instruction from a master to an apprentice. Anything that requires two bodies in the same physical space will become more expensive, because it cannot be copied, generated, or outsourced.

**Atoms.** Bits have become cheap; atoms have not. Houses still need to be built, pipes unclogged, older people cared for, and meals cooked. Even when robots arrive, people will still install them, repair them, and wire them up.

There is a particularly interesting connection here. Remember the transformer and interconnection bottlenecks in Section 4? The world is now competing for high-voltage electrical engineers and licensed electricians. Every electrician hired away by a data center is one fewer person on the grid-construction crew—and that same data center is waiting years to connect to the grid. It is a darkly comic feedback loop: the scarcest worker in the AI industry may turn out to be an electrician.

Make a list of the most durable jobs ten years from now and it will look remarkably similar to a list from a century ago: farmer, electrician, nurse, cook, mechanic, midwife, funeral director.

AI hollows out the middle with uncanny precision: the layer that turns text into text and spreadsheets into spreadsheets. Both ends remain.

Here is a thought that may sting: we spent thirty years training people to behave like machines—KPIs, processes, standardized slide decks, interchangeable cogs. Only when the machines finally arrived did we panic and remember to ask what people were for in the first place.

---

## 8. Organizational Collapse: A Barbell-Shaped World

In 1937, Ronald Coase wrote ["The Nature of the Firm"](https://en.wikipedia.org/wiki/The_Nature_of_the_Firm) and asked a question everyone else thought did not need asking: if markets are so efficient, why do firms exist? Why doesn't everyone simply trade independently in the market?

His answer was that market transactions have costs. Finding people, negotiating, contracting, supervising, and enforcing agreements all cost money. A firm appears when buying something on the market costs more than producing it internally. [A firm will keep expanding until the cost of organizing one more transaction internally equals the cost of carrying out the same transaction through the market](https://python-advanced.quantecon.org/coase.html). The firm's boundary lies on that line.

AI has arrived, and it lowers costs on both sides.

It cuts internal coordination costs more aggressively. Much of the coordination inside a company consists of translating, compressing, and forwarding information—precisely what language models do best. But it also cuts external transaction costs. Finding suppliers, comparing prices, drafting contracts, communicating across languages, and conducting due diligence are all becoming cheaper.

The result is neither that all companies become larger nor that all become smaller. Both extremes grow while the middle is hollowed out. The result is a barbell-shaped world.

At one end are giant platforms. Five barriers have risen rather than fallen: electricity, chips, licenses, capital, and long-established reputations. No amount of cleverness can bypass them. All require time and money.

At the other end are one-person armies. One person maintains infrastructure software used by tens of thousands. One person builds a product for the entire world. A five-person company generates $100 million in revenue. These are news stories today; in a decade they will be normal. Not because those people become stronger, but because each has a machine behind them that needs no salary, equity, or meetings and never gets temperamental.

The large middle dies: mid-sized companies that survive on information asymmetry and piles of labor, organizations where 300 people do work that five could handle.

Middle managers will be the first casualties in that middle layer. A job that translates an executive's slide deck into language employees can understand, then translates employees' complaints into language executives want to hear, lands squarely in the sights of large language models. It was translation work all along.

But this has a consequence that I believe will become the most severe—and least discussed—structural crisis of the next decade.

Consider a set of numbers that already describe the present. The Stanford Digital Economy Lab used ADP payroll data for a longitudinal study and published an updated analysis this August. [Among workers aged 22 to 25 in occupations highly exposed to AI, employment was about 19% below where it would have been had they kept pace with low-exposure peers, and the gap has continued to widen since it was first recorded in August 2025](https://digitaleconomy.stanford.edu/news/canariesaug26/). Between November 2022 and June 2026, absolute employment for the same age group fell by about 11% in the most exposed occupations and rose by about 10% in the least exposed. Older workers showed no comparable gap. Most of the adjustment is happening through hiring, not layoffs: [companies are not firing young people; they have stopped hiring them](https://digitaleconomy.stanford.edu/app/uploads/2026/08/Canaries_August2026.pdf).

This is not merely an unemployment problem. It is the breakdown of apprenticeship.

Think about how someone becomes an expert. Junior analysts check data, assemble comparable-company sets, and draft the first slide deck. Junior lawyers research precedent and organize case files. Junior doctors write patient notes and join their seniors on rounds. Junior programmers fix bugs and write unit tests. The work is tedious, cheap, and apparently unskilled, but judgment grows out of it. You must do something a hundred times yourself before you can tell what is wrong with the hundred-and-first.

And those are precisely the tasks that are easiest to hand to AI.

So ten years from now, we will face an awkward question: if entry-level jobs are gone, where will senior talent come from?

My guess is that those who entered these fields in the mid-2020s may be the last generation to make the full climb from the bottom. After them comes a gap: people who have directed AI from day one but have never done the underlying work themselves. When the old hands retire, who will judge whether the AI is right?

The most frightening thing about this crisis is that it is predictable and has already begun, yet its consequences will take fifteen years to surface. By then it will be too late.

---

## 9. Thamus's Complaint

Now, the human part.

In Plato's *Phaedrus*, the Egyptian god Theuth invents writing and presents it to King Thamus as a remedy for memory and wisdom. Thamus rejects it. [Writing, he says, will plant forgetfulness in learners' souls because they will stop exercising memory and rely on external marks instead; they will hear about many things without truly learning them, appearing to know everything while in fact knowing nothing](https://historyofinformation.com/detail.php?id=3439).

That was 2,400 years ago.

Thamus was right. We did lose the ability to memorize ten-thousand-line epics. Almost nobody today can recite the entire *Iliad* from memory as a bard in Homer's time could. That was a real, irreversible loss of capability.

In exchange, we got libraries, legal codes, science, and civilization itself.

Every later round followed the same script. Calculators cost us mental arithmetic. Navigation systems cost us our sense of direction—and that is not rhetoric; the effect has empirical support. London taxi drivers, who spend years memorizing routes, [have significantly greater gray-matter volume in the posterior hippocampus than controls, and the difference correlates positively with years on the job](https://onlinelibrary.wiley.com/doi/full/10.1002/hipo.23395). Conversely, [a study in *Scientific Reports* found that habitual GPS users performed worse on hippocampus-dependent spatial-memory tasks; a small three-year follow-up with just 13 participants also found that heavier GPS use was associated with faster decline](https://www.nature.com/articles/s41598-020-62877-0). We really did get dumber—and also went places we would never have dared to go before.

Every time we externalize a faculty, we lose a real capability—and expand our capabilities in equally real ways. That has always been the bargain. There has never been an exception.

So the question for the next decade is not whether people will get dumber. Of course we will, along certain dimensions. That is a predictable, measurable, and unavoidable cost, and debating it serves little purpose.

The question is: what are we giving away this time?

In earlier rounds, we gave away memory, calculation, and a sense of direction. Those are all instrumental abilities. They share one property: their results can be independently verified. If one calculator is wrong, you can check with another. If navigation sends you the wrong way, you know when you fail to reach your destination.

This time, we are giving away judgment.

And the only way to verify judgment is with judgment itself.

That creates a logical trap. When a model gives you a plan that appears flawless, what can you use to validate it? Only your own judgment. And if you cultivated that judgment by never doing the work yourself—only reviewing the output—what you are really applying is intuition: intuition that has never been bruised by the real world.

The line we must defend over the next decade is therefore not "use less AI." That would be futile and foolish. We need to protect two things.

The first is the ability to ask questions. In a world where answers are free, questions become the only scarce good. Every answer depends on what you ask, and AI cannot ultimately decide what you should ask. It does not know what you want. Often, neither do you.

The second is the ability to validate. The question is not whether you can produce something. It is whether you can find the three fatal flaws in something that looks perfect—and explain why they are flaws.

Ten years from now, these may be the only intellectual skills still worth paying for.

---

## 10. One Morning in August 2036

Having come this far, I want to break my opening rule and describe one scene.

It is a morning in August 2036. There are no flying cars. An alarm still wakes you. You still complain about the commute and housing prices. You still argue with someone in a group chat about something completely pointless.

But a few details have changed.

Your electricity bill has three rate tiers. One is labeled "compute hours." You have never quite understood how it is calculated.

One question in your child's homework reads: The following passage was generated by a model. Find three errors and explain how you identified them. It is worth more points than the essay question.

Every contract you sign ends with a line in small type: This document was generated by Model X. Human reviewer: So-and-so. Professional license number: XXXXXXXX. You never read that line, but you know who will be held responsible when something goes wrong.

The neighborhood barbershop has a sign on the door: "Humans Only. No Machines." It charges three times as much as the shop next door and always has a line.

Your father's medical report is ready in three seconds. But the person who sits down, explains it to him, and tells him not to worry too much is still human. He does not trust the machine, and—honestly—the machine is still not very good at that part.

Then your child runs over and asks: Dad, is it true that when you were young, people wrote software themselves, one line at a time?

Just as you once asked your grandfather: Grandpa, is it true that when you were young, people kept the books by hand, one entry at a time?

How did your grandfather answer? He probably said "yes" and left it at that. To him, the fact was hardly worth mentioning. It was not the defining feature of an era. It was simply an ordinary afternoon when he was young.

To those who live through them, every great turning point looks like a succession of ordinary afternoons.

---

## 11. The Only Event That Truly Matters

Finally, pull the camera all the way back.

About 3.8 billion years have passed since the first life appeared on Earth. In all that time, there has been only one species able to use symbols for abstract reasoning, accumulate the results, and pass them to the next generation.

That biological monopoly is ending on our watch.

Everything else—prices, employment, organizational forms, geopolitics, who makes money and who loses it—is a footnote to that event, another entry on the price list.

But technology never answers a question. It merely makes the question louder.

The steam engine did not answer "Why do people work?" It merely moved the question from the field to the factory. The internet did not answer "Why are people lonely?" It merely moved the question from the village to the social feed. AI will not answer "What makes a human human?" It will only make the question deafening by 2036, impossible for anyone to avoid.

In a world that does not need you to work, what makes you *you*?

There is no quote for that on the price list.

See you in ten years. This essay will probably still be here, and you can come back to count how many things I got wrong. I suspect the number will not be small.

But I will bet on one thing: what I get wrong will be the form, not the price.
