---
title: "AI Is Bringing Down the Scaffolding of Trust"
date: 2026-05-05
authors: [vonng]
summary: >
  The most dangerous change in the AI era is not that machines can write articles, draw images, or generate video. It is that content itself is losing its standing as evidence.
tags: [AI, Agent, Open Source, Society]
ai: true
---

The most dangerous change in the AI era is not that machines can write articles, draw images, or generate video.
The real danger is that **content itself is losing its standing as evidence**.

For a long time, people assumed that media artifacts carried some degree of credibility.
Text had to be written by someone. Photos had to be taken, video shot, and words actually spoken aloud.
All of these could be faked, of course, but forgery had a cost: it required skill, time, organization, and money.

That cost gave society a set of implicit cognitive shortcuts. See a video, believe it a little. See a photo, believe it a little.
See a signed article, believe it a little.
This was not because people were naive. It was because, historically, there was a fairly expensive toll between "looks real" and "is real."

AI has driven that toll close to zero.

Once the appearance of credibility can be mass-produced, content is demoted from "evidence" to "raw material."
The truth still exists, but it no longer arrives automatically with the content.
Content used to carry a small trust balance. That balance is now zero.
To be believed, you have to pay extra—in time, track record, accountability, endorsement, or something else AI cannot generate.

Marshall McLuhan famously said, "The medium is the message."
What he meant was that the greatest effect of a new medium is never the content it carries. It is how the medium reshapes people and social structures:
a latent, second-order, long-term transformation.
In an earlier essay, "Dissecting AI with McLuhan's Knife," I examined several second-order effects AI may have on human society:
the further collapse of attention, a new stratification of knowledge, the loosening foundations of education, and a blurred boundary between people and tools.

But the most alarming second-order effect is that AI is dismantling the scaffolding of our trust system.
This runs deeper than any particular problem involving jobs, copyright, or security.
People who lose jobs can find new ones. Copyright law can be rewritten. Security holes can be patched.
But once trust collapses, rebuilding it takes generations.

--------

## 2. Trust Is Not One Thing

The most common mistake in discussions of trust is treating "trust" as **one** thing.
It is not.

The Chinese character *xin* (信), which covers belief, trust, confidence, and reliability, is asked to do too much.
"I believe this video is real," "I trust my business partner," "I have confidence in this bank," and "this doctor is reliable"—
all four are variations on *xin*, but their epistemic structures are entirely different.

The first is a factual judgment.
A video is an object. It cannot betray you.
The second is a relational judgment.
A business partner is another person with free will, someone who can choose whether to betray you.
The third is a default state.
You have never consciously considered the possibility that the bank might fail.
The fourth is an assessment of competence.
You are estimating the likelihood that the doctor will do the job well.

Packing all four into one word creates a false clarity: you think you are discussing one problem while sliding among four.

The philosopher Annette Baier offered a clean definition: **trust means accepting another person's discretionary power over something you care about**.
The key words are "another person" and "discretionary power." The other party must have free will; they can choose how to treat you.

Under this strict definition, **trust belongs specifically to relationships between people**.
It necessarily involves risk (the other person may betray you), volition (you choose to expose yourself), and relationship (you face another person, not an object).

A video cannot betray you. Believing that a video is real is an act of authentication, not trust.
A banking system does not choose how to treat you. Confidence in it is a default state, not trust.
A doctor's competence is an objective attribute. Calling a doctor reliable is an assessment, not trust.

Only when you place something you care about in the hands of **a person who can choose how to treat you** are you truly trusting someone.

This distinction may sound pedantic, but it directly determines what has actually changed in the AI era.

## 3. Civilization's Hidden Luxury

Making trust decisions with no scaffolding has never been easy.

In the most primitive setting, two people meet face to face and must decide whether to share food, hunt together, or turn their backs on each other.
Every decision is a full judgment that consumes cognitive resources.
There are no contracts, guarantees, or third-party arbitration.

People cannot tolerate that condition.
It is exhausting.
So one hidden thread running through the history of civilization is that **we keep inventing mechanisms that spare us from making every trust decision in the raw**.

The earliest mechanisms were kinship and locality.
People who shared your blood or lived in your village were more trustworthy than strangers because repeated interaction made betrayal too costly.

Then came ritual.
Blood oaths, exchanged tokens, and public vows pulled "I promise" out of the private sphere and into the public one, imposing a social cost on betrayal.

Once writing became widespread, we gained contracts.
A stamped document had more force than a spoken promise because a third party could verify it and a court could enforce it.

The industrial age brought institutions.
You do not need to trust the bank teller—not in the strict sense. You need confidence that the banking system will function.
Institutions, brands, professional credentials, and regulatory licenses all outsource the problem of trust to an abstract system.

The internet age added algorithms and platforms.
Google helps you decide which pages are credible, Amazon helps you decide which merchants are reliable, and social media filters information for you.
You do not have to make an unmediated trust decision about everything, every day.

Every generation of mechanisms does the same thing: **it converts an exhausting trust decision that requires conscious volition into a default that does not**.

In his 1968 study of trust, the German sociologist Niklas Luhmann gave these two states names:
a decision that truly requires volition is **trust**; a default that does not enter conscious awareness is **confidence**.
He argued that **modern society works by converting trust into confidence**, sparing people from making genuine trust decisions through most of daily life.

This is civilization's hidden luxury.
Our generations have enjoyed it for decades. We take it for granted and assume life has always worked this way.

AI has thrown that conversion mechanism into reverse.

## 4. All Five Layers of Scaffolding Are Loosening at Once

AI has not changed the logic of trust itself. The leap in which you face someone who may betray you and still choose to expose yourself is the same as it was ten thousand years ago.
What AI has changed is the entire scaffolding that supports that decision.

This scaffolding has five layers.
They are not the same kind of thing. Each corresponds to a different link in the trust-confidence chain.

### Layer One: Authentication—The Cost of Asking "Is This Real?" Explodes

This is an engineering problem.

In the past, the question "Am I dealing with a real person, object, or event?" usually had a very cheap default answer.
A video was real because faking one at that quality required a team, equipment, and time.
A voice was real because imitating a specific person was difficult.
A bylined article was real because few ghostwriters could perfectly reproduce another person's rhythm of thought.

AI has broken that default.
Authentication must move from implicit to explicit, from a default to a procedure that has to be actively invoked.

The real problem at this layer is not that "things have become fake." Things could always be fake.
It is that **authentication must move from a default into conscious awareness**.
Every time you encounter a piece of content, you must stop and ask: Where did it come from? Who posted it? Is it signed? Does the timestamp check out?

Authentication is not itself trust. It is a precondition for trust: before deciding whether to trust someone, you must first establish who you are dealing with.

This is **the easiest layer of the AI trust problem to solve**.
C2PA content credentials, digital signatures, device-level cryptographic authentication, and verifiable identity credentials are not window dressing. They genuinely restore our ability to authenticate.
They will gradually become infrastructure.
The European Union is already pushing to mandate C2PA; identity wallets are rolling out across the EU; and Sigstore has become a de facto standard for the software supply chain.

But solving authentication does not solve trust.
A perfectly signed video may still be a truthful message from someone unworthy of trust.
Authentication answers, "Is this object what it claims to be?" It does not answer, "Does the person behind it deserve my trust?"

### Layer Two: Confidence—Countless Judgments Are Forced Back Into Conscious Awareness

This is a problem of cognitive load.

For decades, we had confidence that the videos we saw were real—not because we judged them to be real, but because we never consciously opened the question.
That is confidence in Luhmann's sense: an energy-saving mechanism.

AI has destroyed that confidence. The question of whether a video is real must return to conscious awareness for processing.
This does not mean "we no longer trust videos." Videos were never objects of trust.
It means **the energy-saving mechanism has failed**.

The brain has limited cognitive bandwidth.
When everything that once required no active judgment suddenly demands one, the cognitive budget is quickly exhausted.
People then fall into one of two states: hypervigilance, believing nothing, including what is real; or cognitive surrender, giving up on judgment and deciding what to believe through emotion and tribal alignment.

Neither response is a collapse of trust. Both are emergency reactions to the failure of the brain's energy-saving strategy.
Restoring confidence is much harder than restoring authentication.
Technology can restore authentication, but it cannot directly restore confidence. Confidence grows out of time and stability.
A new information environment will need at least a decade to develop new forms of confidence.

### Layer Three: Intermediaries—The Legitimacy of Our Trust Proxies Erodes

This is an institutional problem.

In the past, we outsourced many trust decisions to intermediaries. Traditional media helped us decide what counted as fact, institutions what counted as authoritative,
platform algorithms filtered credible content, and influencers selected what deserved our attention.
These intermediaries spared us from making every judgment from scratch.

AI is disrupting several kinds of intermediary at once.

Traditional media's filtering function breaks down in an ocean of AI content because the material they select may itself be AI-contaminated.
Algorithmic platforms can no longer keep their promise to "recommend credible content."
The credibility of influencers is diluted by AI imitation: their voice, style, and opinions can all be copied at scale.

But intermediaries will not all disappear.
They will **split**.

Intermediaries whose legitimacy rests on "I filter information for you" will decay. General search, feeds, and content aggregators will continue to lose legitimacy.

Intermediaries whose legitimacy rests on "I can vouch for identity and accountability" will grow stronger.
Large platforms that control accounts, devices, payments, real-name records, corporate verification,
hardware signatures, and operating-system entry points will become more valuable in an age of untrustworthy content.
When you cannot tell whether a video is real, the fact that "it came from an account with a verified identity and payment history" becomes crucial.

The next generation of major platforms will derive power less from "I recommend good content" than from "I know who is real."
**The bazaar can be dirty. Customs cannot fail.**

This is an uncomfortable prediction: when content pollution is at its worst, platforms that control identity verification will become even more powerful.
Many anti-platform narratives would rather not confront this. But that is where the logic leads.

### Layer Four: Capacity for Judgment—Mentalizing Fatigue

This is a biological problem.

The brain contains a network of regions specialized for inferring other people's intentions. Neuroscience calls it the "mentalizing system."
We use it to judge what others are thinking, whether they mean us well, and whether they are reliable.
This system is the biological basis of trust decisions. Without the capacity to mentalize, we cannot form expectations about another person's goodwill and therefore cannot make a genuine trust decision.

AI content presents this system with an unprecedented challenge: **you are trying to infer the intentions of something with no stable intent**.

There is no single "authorial intent" behind an AI-generated article. It is a mixture of the model maker, training data, the user's prompt, and randomness.
But the brain does not stop trying to infer intent merely because its object has none. It starts, fails, starts again, and fails again.
That process consumes real neural resources.

Long-term exposure to large volumes of content that repeatedly defeats mentalizing may exhaust this system and eventually impair our ability to trust real people.
This is not a prediction, but it is a reasonable concern.
Research has already found lower levels of interpersonal trust among heavy social-media users. An ocean of AI content could intensify the trend.

This layer differs from the first three. Those concern the external environment; repair the environment, and the underlying capacity remains.
**This one concerns an internal capacity. Once damaged, it may not recover even after the external environment is repaired.**

### Layer Five: Social Capital—Civilization's Hidden Savings Are Being Spent

This is a macro-level problem.

Social capital is civilization's hidden savings: generalized trust between people, participation in communities, and the ability to cooperate across groups.
It accumulates slowly, is spent quickly, and is extremely difficult to rebuild.
A generation after the decline in American social capital that Robert Putnam documented in *Bowling Alone*, the trend has yet to reverse.
In *Trust*, Francis Fukuyama argued that a society's "radius of trust" sets an upper bound on its economic development.

The AI era may be accelerating the depletion of social capital.
All four preceding layers exert downward pressure: failed authentication makes people vigilant; collapsing confidence makes them tired; fragmenting intermediaries leave them disoriented; and mentalizing fatigue makes them invest less in other people.
Together, these forces make cooperation among strangers harder, erode trust across groups, make long-term contracts harder to sign, cause public deliberation to break down, and deepen political polarization.

Repair at this layer takes **multiple generations**.

### Ranking the Five Layers by Solvability

Put the five layers together and a disturbing pattern emerges: **the shallower the layer, the easier it is to solve; the deeper the layer, the more intractable it becomes**.

Layer one, authentication, is an engineering problem that engineering solutions will gradually address.
Layer two, confidence, requires time on the scale of a decade.
Layer three, the restructuring of intermediaries, is already underway and will largely play out over the next five to ten years.
Layer four, mentalizing fatigue, has almost no proposed remedy.
Layer five, social capital, is a multigenerational problem.

The visibility of an "AI trust problem" in public debate is inversely proportional to its severity. The shallow layers can be discussed; the deep ones lack even a vocabulary.
That is why there is so much talk about "AI trust governance," while most substantive proposals remain concentrated on the first layer.

## 5. What Can This Framework Predict?

The value of a framework lies not in the elegance of its rhetoric but in what it can predict.
Apply the six layers above to concrete situations and several conclusions follow directly.

**Content production:**

The supply of low-cost output will continue to inflate.
AI can mass-produce articles, videos, images, and code that all "look pretty good."
Anyone whose status depends on volume will work harder and earn less over the next five years.
Influencers who maintain their reach through daily posts, creators who race to repackage other people's work, and consultancies that sell middling output will all see their positions deteriorate quickly.

Content itself is not what gains value. What gains value is **the supporting structure that makes your content trustworthy**.
An auditable track record is worth more than a one-off reputation.
A record of sustained accountability is worth more than eloquence.
Specific relationships that cannot be copied without loss are worth more than generic attention.

**Platforms and intermediaries:**

General search, feeds, and content aggregators—the intermediaries that perform "information filtering"—will continue to decline because their value proposition, "I screen it for you," breaks down in an ocean of AI content.

Intermediaries that control "identity plus accountability" will become more valuable.
Verified accounts, device signatures, business verification, payment histories, and operating-system-level identity checks—things once dismissed as mere "infrastructure"—will become a new form of power.

Influencers, as trust intermediaries built on personal brands, will polarize.
Those sustained by eloquence will lose value because AI can imitate them. Those sustained by a long record of concrete action and accountability will gain value because AI cannot imitate responsibility.

**How tech work will stratify:**

The ability to write code will lose value. AI can already write most code.

The ability to review code will hold its value—but the core of that skill is judging "what good code looks like," not producing code.

The ability to maintain systems will gain value. AI can generate a project, but it cannot sustain a system users depend on for ten years, handle production incidents on your behalf, or bear organizational responsibility when the system breaks.

The ability to define direction will become much more valuable. Deciding what a project should and should not do is worth far more than writing the code for a decision already made.

The ability to be someone others can depend on over the long term will be most valuable of all. That is the real hard currency of the AI era.
It includes an auditable track record, a long history of taking responsibility, stable judgment, and a concrete network of relationships.

The real dividing line is **responsibility density**.
The closer work sits to actual system state, real data, real money, and real incidents, the more slowly AI will replace it.
The closer it sits to packaging, retelling, boilerplate, and information shuffling, the faster AI will replace it.
This line explains far more than the question "Will programmers lose their jobs?"

**Personal strategy:**

The easiest strategic mistake to make in the AI era is thinking you should produce more content.
You should not.

Content is already abundant. Opinions are abundant. Tutorials are abundant.
Any path built on volume is rapidly losing value.

What you should invest in is **the supporting structure that makes you trustworthy**:
turn articles into archives, projects into governance, and communities into pathways for trust;
turn judgments into public records, one-off meetings into continuing traditions, endorsements into accountable commitments, and individual reputations into networked reputations.

All these moves share one feature: **they spare people from making a naked trust decision every time they encounter your work**.
Your long record, auditable history, willingness to take responsibility, and concrete relationships let them develop a degree of local confidence.

This is not a call to rebuild the grand institutional scaffolding of the industrial age. That world is not coming back.
It means slowly constructing smaller scaffolds at local scale and within specific communities.
The goal is for a particular person, project, or community to become a reliable default for the people around it.

This work is slow.
AI makes output cheap, so accountability becomes expensive.

Code will keep getting cheaper; maintenance will keep getting more expensive.
Expression will keep getting cheaper; responsibility will keep getting more expensive.
Generation will keep getting cheaper; judgment will keep getting more expensive.
One-offs will keep getting cheaper; networks will keep getting more expensive.

**Human-AI collaboration:**

The age of AI as a collaborator has already begun.
Over the next decade, engineers, writers, designers, and researchers will outsource a great deal of judgment to AI agents.

Everyone will have to find the boundaries for themselves.
Which judgments can be outsourced? Which ones must remain ours? When should we accept an AI's advice, and when should we reject it?
There are no standard answers, but **avoiding the questions is itself a bad answer**. Outsourcing judgment to AI by default
means handing a trust decision to an entity with no accountability structure.

The deeper problem is one of identity.
As people rely increasingly on AI to make judgments, will their own judgment atrophy? Will they become less patient with human collaborators?
When they face a moment that truly demands a naked trust decision—an important life choice, a critical partnership, a deep interpersonal commitment—will they still be capable of making it?

No one has answers to these questions yet.
But **they must be recognized as questions**, or people will lose core capacities without noticing.

## 6. Trust Must Always Be Ours

Return to the distinction at the beginning: trust is a relational, volitional act by one person toward another person with free will.

That means no matter how well we rebuild the scaffolding, how advanced the technology becomes, or how intelligent AI gets, **the final decision to trust will always rest with a human being**.

The leap in which you recognize that another person may betray you, see the risk, and still choose to expose yourself cannot be made by any technological system.
Authentication can be mechanized, competence assessed, and accountability encoded in contracts, but **the leap itself will always be naked**.

This is why every conversation about "AI trust governance" eventually hits a wall.
We can make authentication reliable, platforms transparent, regulation strict, and algorithms cautious.
But we cannot eliminate the decision a person must make when facing another person. It is one of the moments at the core of being human.

The practical significance of this conclusion is simple: **do not let utopian stories about how "AI will eventually solve everything" anesthetize you**.
Of the five layers under pressure, only the first has a technical solution. The other four require genuine human accountability.
The sixth layer—the relationship between people and AI—is an entirely new domain with no ready-made answers.

Our generation is not facing a new kind of trust-technology problem. We are witnessing **the return of something forgotten for decades**:
the need to make genuine trust decisions in an environment without ready-made scaffolding.

It is exhausting.
People did it throughout the long ages before the scaffolding existed.
Most of us who grew up with the scaffolding have forgotten how.
The AI era requires us to learn again.

Civilization has never rested on a world where such moments of decision can be eliminated.
