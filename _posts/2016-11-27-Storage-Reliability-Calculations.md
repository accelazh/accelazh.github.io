---
layout: post
title: "Storage Reliability Calculations"
tagline : "Storage Reliability Calculations"
description: "Storage Reliability Calculations"
category: "storage"
tags: [storage, reliability, cloud]
---
{% include JB/setup %}

When designing storage systems, for example comparing different coding schema, it is necessary to calculate reliability numbers. Here I summarize the useful concepts from reliability engineering and their math relations.

__Reliability engineering__

```
λ = failure rate, expressed in failures per unit of time
MTBF (mean time between failures) = 1/λ    // why? see hazard function and exponential distribution
AFR = 1 - e^(-exposure_time/MTBF) = 1-e^(-exposure_time*λ) = probability of failure occurs within the exposure_time
Assuming a small AFR (<5%), we can approximatedly have AFR ≈ 8760/MTBF
1 - AFR = probability of failure does not occur (survived) within the exposure_time
```

__Hazard function__

```
T = a random variable of the time until some event of interest happens 
f(t) = probability density of event happens at t
F(t) = P(T<=t) = probability of event happens before t

S(t) = survivor function / reliability function := 1 − F(t) = probability of event happens after t, or say event survived beyond t

h(t) = hazard function := lim(h->0+, P[t ≤ T < t + h|T ≥ t]/h) = f(t)/S(t-) = - d ln(1-F(t)) / dt = - d ln(S(t)) / dt
h(t)dt = f(t)dt/S(t) ≈ P[fail in [t,t+dt) | survive until t]
H(t) = cumulative hazard function := ∫ (0->t, h(u)du) (t>0) = -ln(1-F(t)) = -ln(S(t))
So, S(t) = e^−H(t), f(t) = h(t)e^−H(t)

Exponential Distribution: T ~ Exp(λ), for t>0.
    f(t) = λe^−λt for λ > 0 (scale parameter)
    F(t) = 1 − e^−λt    // this is the AFR mentioned above
    S(t) = e^−λt    // this is the (1 - AFR) mentioned above
    h(t) = λ    // constant hazard function. this is the failure rate mentioned above
    H(t) = λt
    Characteristics: 
        E(T) = 1/λ    // this is the MTBF mentioned above
        "Lack of Memory": P[T > t] = P[T > t + t0|T > t0]. Probability of surviving another t time units does not depend on how long you’ve lived so far.
```

__Calculating MTBF from observation__

```
observed AFR = failed device count / total device count
calculated MTBF(hrs) = 8760 / AFR    // 8760 is the number of hours in a year
exposure_time: for storage system with auto repair, the exposure time of second node failure should be the recovery window
failure possibility in a given time window = F(t) = 1 − e^−λt ≈ λt = t/MTBF = t * AFR / 8760, t is the time window length. note that for storage systems, time unit of hour may be more appropriate
```

__Availability vs durability__

```
Availability: the probability of data is accessible by user. The data needs to be on disk, and server nodes have to be healthy. Also the network.
Durability: the probability of data is safe on disk. The data may not available to user, but still on disk.
For example: AWS S3 offers 99.999999999% durability and 99.9% availability.
```

__Data loss probabilities__

```
Basics
    
    A(n, k) := Permutation(n, k) = n! / (n-k)!
	C(n, k) := Combination(n, k) = n! / ((n-k)! k!)
	Zm := {0, 1, .., m-1}
	Subset(A) := {a | a is subset of A}
	¬A := overbar A := complementary set of A
	I := the complete set = A + ¬A
	Code schema (D-K, K) := the simplest erasure-coding schema of D-K data fragments and K parity fragments. When lost fragment count <= K, survive. When lost fragment count > K, lost this extent.
	P(event): a probability is operating on event. An event is a set. So set algebra applies to events.
	∩: event1 AND. This is aligned with set algebra
	∪: event1 OR. This is aligned with set algebra
	¬ or overbar: event NOT happen. This is aligned with set algebra

Basic formulas (proof omitted)

	Event breakdown formula: (aux1)
	Multiple event breakdown formula: (aux2)
	If Ai are mutually independent, then ¬Ai are mutually independent: (aux3)
	Conditional probability can reverse: (aux4)
	If Ai are mutually conditional independent given N, then ¬Ai are mutually conditional independent given N: (aux5)
	Space division, which is useful for node failure probability: (aux6)

Notations
	
	Cluster setup: 
		
		We have N nodes, each have independent probability p to fail.
		We have M extents (extent is the basic data unit, i.e. object), each is encoded into a D-fragment code.
		We randomply place the fragments on nodes, each node holds at most 1 fragment from a given extent.
		The code schema can be complex, e.g. LRC code.
		The placement may have constraints, e.g. domains, copysets.

	Node failure

		Node set is ZN ("N" in subscript)
		NL := a node failure event. NL is a subset of Zn.
		NLS := the space of NL = Subset(Zn)

	Extent and Extent Loss

		Ei := Extent i, i in ZM ("M" in subscript)
		EL := an extent loss event = {indexes of the lost fragments}    // fragment index is element of ZD ("D" in subscipt)
		ELS := the space of EL = {EL|any EL}, it is the set of which fragment-loss can cause extent loss 
		¬ELS := Subset(ZD) - ELS, it is the set of safe fragment-loss

	Placement

		PM := a placement = [node indexes of the placed fragment, for fragment from idx=0 to idx=D-1]
		PMi := extent i's placement
		Sall ("all" in subscript) := {all possible placements }
		S := set of the allowed placements, S is subset of Sall, due to placement constraints
		SNL ("NL" in subscript) := {placement that will cause extent loss}, given NL
		∩h ("h" in subscript) := set intersect and map node index to fragment index. if (PM ∩h NL) is element of ELS, we have extent lost.

	Data loss

		Ei DL := an event of extent i is lost. P(Ei DL) is the probability of lost extent i
		Ei DL | NL = extent i loses, given NL. P(Ei DL|NL) is the conditional probability of Ei DL given NL
		DL := an event of data loss. P(DL) = P(DL>0) is the probability of losing at least 1 extent in the cluster. P(DL=r) is the probability of losing r extent in the cluster.

Assumptions

	Extent placements are mutually independent: (asp1)
	Given an extent, placements are exclusive: (asp2)
	Placement is evenly randomized: (asp3)

	Node failure is exclusive: (asp4)
	Node failure is independent with extent placement: (asp5)

Implications (proof omitted)

	Extent placement sets are independent: (imp1)
	Node failure is independent with extent placement sets: (imp2)
	Sample space (elementary event space)
		An elementary event is: (NL, PM0, PM1, .., PMM-1)    ("0", "1", .., "M-1" in subscript)
		The sample space is: NLS × S × S × ... × S    (count of S = M)
		Given NL, P(ʘ) := elementary event probability, P(ʘ) formula:   (imp3)
		Key takeaway: most of the proofs below is conducted by breaking events down to elementary events
		              probability is essentially counting elementary events

Conclusions (proof omitted)

	Calculate P(Ei DL|NL): (thr1)
	(Ei DL|NL) are mutually conditional independent: (thr2)
	(Ei DL|NL) and ¬(Ei DL|NL) are mutually conditional independent: (thr3)
	Calculate P(Ei DL): (thr4)    // To proove the two forms are equal, breakdown them into P(ʘ)
	Ei DL are not independent: (thr5)
	Alternative assumption, Ei DL are still not independent: Assume extent placements are fixed/known, the sample space becomes NLS. Find a counter-case: PMi, PMj are overlapped.
	Data loss count distribution: (thr6)
	Data loss probability: (thr7)
	P(Ei DL) vs P(DL): connected by |SNL|/|S| ("NL" in subscript), but not always matched
		Counter-case: from (N, p, D, K, M) = (20, 0.16, 4, 1, 50) to (20, 0.16, 12, 2, 50), P(DL) drops, but P(Ei DL) raises.

Question

	If we have a large number of nodes, and many extents, will the extent loss event become nearly independent?
		We can think this way
			Since cluster is large, (Ei DL) is less affected by (Ej DL).
			When we take extents E0, E1, ..., Em-1, they are more likely to be not overlapped
				When E0, E1, ..., Em-1 are not overlapped, we can deduce that Ei DL are independent
```

![Formula index](/images/dataloss-formula-index.png "Formula index")