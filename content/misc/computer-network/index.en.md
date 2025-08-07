---
title: "Computer Networks and Logistics Systems"
date: 2013-09-14
author: vonng
summary: Computer networks are like a logistics system, with the only difference being that logistics systems transmit material entities like mail and packages, while computer networks transmit intangible information.
math: true
---

{{< katex >}}

Computer networks are like a logistics system, with the difference being that logistics systems transmit material entities like mail and packages, while computer networks transmit intangible information.

Computer networks are divided into five layers from bottom to top: physical layer, data link layer, network layer, transport layer, and application layer:

1. Dense networks of roads form the **physical layer**.
2. Transfer stations and roads together constitute the **data link layer**.
3. Various distribution centers are routers, which form the core of the **network layer**.
4. Going up, those delivery stores become the main body of the **transport layer**.
5. Finally, various users, consumers, enterprises, and companies are located at the top of the system—the **application layer**.

## 1. Application Layer

Consumers buying things online and sending letters to distant friends need to use services provided by the logistics system.

Sharing (transmitting) data (goods) and communication are the two major functions of networks.

Consumers and sellers agreeing on shopping and payment details, processes, and rules online, this is **protocol**.

Sending packages has rules for sending packages, such as **File Transfer Protocol (FTP)**

Sending letters has rules for sending letters, such as **Simple Mail Transfer Protocol (SMTP)**

Sellers contacting logistics companies is called requesting service.

Delivery personnel are **Service Access Points (SAP)**

The goods to be sent are protocol **data units (PDU)**

Some people send packages, which need to go to counters or community guards. Some people send letters, which can be directly put into home mailboxes.

Counters and mailboxes are **ports**, providing different services for different application layer objects.

## 2. Transport Layer

When mail arrives at stores, many pieces of mail from the same place are classified by destination and packed into large packages (**TCP/UDP datagrams**)

For regular mail, if lost, the post office is not responsible, but they will try their best (who knows) to deliver. This rule is called **User Datagram Protocol (UDP)**.

If lost, then there's no way around it, users can only send another copy (application layer retransmission). Fortunately, when traffic is smooth, this rarely happens.

Although not very reliable, regular mail is cheap. So most mail and packages that aren't very important or urgent are sent this way. Because there aren't many procedures, it's also slightly faster to send this way.

Registered mail is slightly more troublesome and expensive (higher overhead). But the post office guarantees delivery. If lost, they'll help you send it again (**retransmission**).

The specific rules are: before each mailing, contact the destination store, tell them we want to send a package please check (**connection request**), then after they confirm receipt, start the mailing process (**connection confirmation**). After they receive the package, they'll also tell this side: we received it (**acknowledgment of acknowledgment**).

This entire three-way handshake process is part of **Transmission Control Protocol (TCP)**.

Each mail must have an address written on it indicating where to send it, whether to throw it in the mailbox or leave it with the guard or deliver door-to-door (port number). This address combined with the distribution center's **address (IP address)** is called a **socket**.

Sometimes when logistics pressure is high, the destination store will include notes (window field) in packages sent to this side, saying "slow down your packages, send fewer, we haven't finished processing yet." (**Window control**).

Sometimes, letters have feathers inserted (urgent pointer), and when the post office sees such letters, it will immediately stop current delivery activities and deliver this letter to users. (**Urgent data**)

Traffic congestion is always inevitable, or sometimes transport vehicles flip on the road and all mail is destroyed. At this time, as long as this side's post office doesn't receive a response after a period of time, it will resend a package (**timeout retransmission**)

Regardless, packages received by stores must be submitted (using network layer services) to distribution centers (**routers**) for unified scheduling (routing).

## 3. Network Layer

Logistics systems have many, many distribution centers (routers), and various distribution centers are also connected by many transport methods (data links).

Every distribution center (router) connected to the public transport network (internet) has a unique address (IP address). Of course, each town (host) may also have multiple distribution centers (multiple IP addresses).

Sometimes, local emperors (LAN administrators) will also build a local postal network (LAN), which uses local addresses (local LAN IP addresses). Mail with such addresses cannot enter the public transport network.

After each package arrives at a distribution center (router), it will be labeled (**IP datagram header**) with destination address and sender address written on it. Like Zhejiang Ningbo XXX distribution center, Jiangsu Nanjing XXX distribution center, etc.

Previously, mail addresses only needed four segments (4-segment decimal IP address notation), like China – Zhejiang Province – Ningbo City – Yinzhou District, because distribution centers were relatively rare at that time. But with economic development, even remote mountain villages have built distribution centers, so four-segment addresses became insufficient. So the standard currently being promoted is six-segment addresses, not only writing to the city but also writing town, village, community... a total of six levels (IPv6).

Of course, the content on this package label has much more.

When distribution centers see the distribution center IP (target IP) to send to, although they know what this distribution center is called (network address IP), they don't know which road to take (physical address MAC). So they send a letter to all connected roads, writing, "I'm looking for XXX distribution center, who knows, tell me which road to take." This is called (ARP addressing). Then XXX receives this and replies: "I am XXX, take this road." (ARP response packet)

After packages are sent out, the next distribution center will again choose the best route and continue passing this package along (routing).

Usually, distribution centers also have levels (network types). National level (Class A), provincial level (Class B), city level (Class C). The higher the level, the larger the jurisdiction (network size) of this distribution center, and the fewer the number of this type of distribution center. Sometimes, townships will also have their own distribution points, like various communities building pickup and delivery points (subnets).

When distribution centers work, they coordinate and communicate with each other not by phone, but also through letters—Internet Control Message Protocol (ICMP). Exchanging information about which roads are not good (destination unreachable), roads too congested, reduce business volume (source quench), etc.

Sometimes, various distribution centers will also exchange information about the best logistics routes (routing protocols). Generally, intra-provincial and intra-city networks prefer internal communication first (Routing Information Protocol RIP), then designate a main distribution center as the main logistics export for the province (BGP Speaker Border Gateway Protocol speaker), then national-level distribution centers arrange inter-provincial route selection (Open Shortest Path First Protocol OSPF).

## 4. Data Link Layer

Hard-working drivers are always working on delivery roads. Their work is very simple: make a phone call before departure (synchronization), then carry goods (IP datagrams), pack them up (encapsulate into frames) and hit the road.

To prevent goods from being lost in transit or embezzled by drivers, distribution centers put a manifest containing goods information (check code) in each container. If it doesn't match when receiving (checksum error), then this truck of goods must be discarded (discard frame). But drivers only handle transport work; to resend goods, you need to pay again (data link layer doesn't provide retransmission service, most of the time).

Usually, a city (user) has direct highways to the provincial capital (ISP), and trucks driving these roads are the most comfortable because they never get lost (Point-to-Point Protocol PPP), and this road is exclusive, spacious with no one competing. Packages sent don't need to tell drivers which road to take (PPP protocol doesn't need physical addresses) because it's point-to-point.

However, most of the time it's not this comfortable. Local road networks (Ethernet) within cities are complex and intricate. Driving on such road networks requires navigation and addresses (MAC). A popular road structure is one main road connecting many, many branch roads (bus-type Ethernet). Most frustratingly, this road is also one-way, only allowing one car in one direction at a time (half-duplex working mode). So trucks from various districts wanting to access the public transport network must compete for this road (collision).

Because only one car can pass at a time, to resolve conflicts, truck drivers established a rule (CSMA/CD protocol): before getting on the road, first put your ear to the road and listen if there are any cars; if no cars, then get on the road (Carrier Sense CS). But often two drivers hear the road is empty and get on together, resulting in collisions, and both trucks' goods are wasted. The new solution is: first calculate the time 2t needed for trucks to make a round trip along the longest path on the main road (contention period). After each collision, both sides first shout "collision! collision!" (collision reinforcement) to let everyone know. Then both sides randomly wait for a while before getting on the road; if they collide again, then wait randomly within an even longer range (dynamic backoff) before getting on the road (truncated binary exponential backoff). If they collide sixteen times, then this road is really too congested. Better go home obediently (network busy, transmission failed).

So how do drivers navigate? The answer is that each container (MAC frame) that needs to run on city road networks (Ethernet) has an address written on it. This address is globally unique; every mailbox, every counter, every mail room has such an address.

But usually house numbers (MAC) are not easy to see. So when delivering, drivers will run through every community, saying: "Packages for XXX community, come collect them" (broadcast). If the address matches, then the community reception desk uncle (network card) accepts it. Of course, there are also some bad guys who secretly accept packages that aren't theirs (this is because information can be copied), called (promiscuous mode). There are also bad people who install surveillance on roads (sniffers) to peek at package contents.

By the way, inter-city point-to-point highways (PPP), if not connected by the provincial capital (subordinate ISP) to a specific town (user), but connected to a transport network (LAN/Ethernet) composed of towns, then the goods specifications (frame format) also need to be unified. The industry practice is to wrap specialized containers (PPP frames) with another layer of ordinary road network containers (MAC frames). This double packaging is called "specialized containers running on city roads" (PPPoE PPP on Ethernet - PPP frames running on Ethernet).

## 5. Physical Layer

The physical layer is the roads drivers take.

High-speed rail is optical fiber; highways are coaxial cables and twisted pair cables.

Maximum load capacity is maximum data rate—bandwidth.

But road speed doesn't correspond to computer network speed; it corresponds to departure frequency.

Delay and throughput are the same concept. Delay is divided into several types: departure time (transmission delay), time spent on the road (propagation delay), time wasted at toll stations (queuing delay), time wasted at distribution centers (processing delay).

Delivery time (delay) mainly depends on road width (bandwidth, network speed). For a batch of 100 trucks, roads that can only accommodate one truck at a time versus roads that can accommodate ten trucks at a time will definitely take very different amounts of time. Trucks run very fast (near light speed), so time spent on the road is very short. One kilometer takes only 5 microseconds to complete. Of course, this is when road conditions (network conditions) are good; if there's traffic congestion, then it mainly depends on queuing and processing time.

Generally speaking, having one road run only one company's trucks is too monopolistic, so engineers always think about letting one road simultaneously run more companies' vehicles (bit streams). Main methods include: expanding lanes on one road: A lane, B lane... (Frequency Division Multiplexing FDM), everyone taking turns (TDM Time Division Multiplexing), or one truck simultaneously carrying goods from several companies (CDM Code Division Multiplexing).

So how do roads come about? Generally speaking, main roads are directly built by national departments (major ISPs) by clearing wasteland. Roads within towns generally connect to main roads using old dirt roads (public telephone networks). Although dirt roads, they're spacious enough. The tractors (3KHz telephone signals) that used to run can now run big trucks (1MHz digital signals). But this dirt method (ADSL) has a problem: main roads are usually at higher elevations, so trucks going down are fast, but going up is very laborious (ADSL asymmetric user lines have downstream rates much higher than upstream rates).

Some towns are wealthy enough to build high-speed railways right to their doorstep (FTTH fiber to home), while less wealthy ones build to city centers (FTTx fiber to street, to community, to...).