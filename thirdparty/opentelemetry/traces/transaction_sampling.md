## Elastic APM supports two types of sampling:

- Head-based sampling
- Tail-based sampling

### Head Based Sampling

- the sampling decision for each trace is made when the trace is initiated
- a sampling value of .2 indicates a transaction sample rate of 20%
- Head-based sampling is quick and easy to set up
- Entirely random — interesting data might be discarded purely due to chance

### Tail Based Sampling

- the sampling decision for each trace is made after the trace has completed
- 