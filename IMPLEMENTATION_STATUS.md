# Implementation status against the handout

| Assignment | Included and runnable | Remaining before claiming full handout acceptance |
|---|---|---|
| 1 | text/hex/file hashing, Base64, streaming, avalanche, canonical JSON | add instructor-specific CLI output formatting if required |
| 2 | domain-separated tree, empty/single/odd/even cases, proof generation/verification, benchmark script, diagram | benchmark at 100k leaves on submission machine and attach measured report |
| 3 | Ed25519 keygen, Base58Check address, canonical bytes, sign/verify, threat model | persist per-address nonce/replay registry; add explicit wrong-network/signer negative acceptance suite |
| 4 | UTXO state, P2PKH-style owner check, signed transaction validation, atomic commit, fee, largest-first selection, change builder, snapshot persistence, 20 ledger tests | complete full output locking-script model and expanded overflow/replay policy |
| 5 | header, toy PoW, Merkle validation, cumulative-work function and fork-choice skeleton | full transaction/coinbase/state-transition validation, complete branch reorg restoring UTXOs, miner/fork simulation and measured 3-target report |
| 6 | versioned TCP JSON framing, size cap, async node, ping, transaction/block acceptance, duplicate suppression and error handling | five-node discovery/inventory-request relay, rate limits/timeouts/scoring, mempool fee/expiry/conflict policy, partition/reconnect convergence and structured persistent logs |
| 7 | Solidity escrow, roles, custom errors/events, pull payments, local Foundry test suite, deploy/interact scripts, state diagram and threat model | run Foundry/Anvil in a local Solidity toolchain and attach actual deployment receipts, bytecode address and gas report |

The code and documentation deliberately identify incomplete integration work rather than presenting unimplemented requirements as completed. The PDF's deadline string (“15th Nov 2023 2359”) conflicts with the July–December 2026 course heading; confirm it with the instructor.
