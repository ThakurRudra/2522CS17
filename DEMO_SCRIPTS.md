# Narrated video demo checklist (one unlisted video per assignment)

Keep each recording short (about 2–4 minutes), show a clean terminal, explain the design decision, run the commands/tests, and show the expected result. Do not show private keys or credentials.

1. **A1:** run text and hex modes, compare newline/no-newline hashes, run avalanche, hash a large file and explain streaming.
2. **A2:** build five-leaf root, generate a proof for index 2, verify it, tamper with a sibling and show rejection; show the diagram and performance script.
3. **A3:** generate a test-only key pair, derive address, sign a canonical transaction and independently verify; change amount and show failure.
4. **A4:** create genesis output, build a signed payment with change, apply it, replay it and show rejection; show snapshot before/after a failed transaction.
5. **A5:** mine a block, show header fields, target check, Merkle root and the fork-choice/branch diagram. Explain current limitations of the compact reference implementation.
6. **A6:** start two or more localhost nodes, ping a node, relay a transaction twice and show duplicate suppression; show protocol framing and explain the five-node extension plan.
7. **A7:** run `forge test -vv`, deploy to local Anvil, fund, release or dispute/resolve, withdraw, and show emitted events and balances.
