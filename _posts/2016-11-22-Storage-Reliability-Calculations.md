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
