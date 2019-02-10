# Implementing PBFT in DistAlgo
<https://sites.google.com/a/stonybrook.edu/sbcs535/projects/pbft-distalgo>

This repo contains implementation for PBFT in DistAlgo.

PBFT (Practical Byzantine Fault Tolerance) tolerance) proposed by Castro & Liskov is a replication algorithm that can tolerate Byzantine faults. Earlier, Byzantine fault tolerant algorithms had assumptions and requirements that were infeasible to attain and accept in practice. PBFT offers a practical solution to the BFT problem without imposing too compromising restrictions. It tolerates Byzantine Faults through an assumption that there are independent node failures and manipulated messages propagated by specific, independent nodes.

As described in paper each round of pBFT consensus (called views) comes down to 4 phases. This model follows more of a “Commander and Lieutenant” format than a pure Byzantine Generals’ Problem, where all generals are equal, due to the presence of a leader node. The phases are below:

1. A client sends a request to the leader node to invoke a service operation.
2. The leader node multicasts the request to the backup nodes.
3. The nodes execute the request and then send a reply to the client.
4. The client awaits f + 1 (f represents the maximum number of nodes that may be faulty) replies from different nodes with the same result. This result is the result of the operation.