# ProvenanceOrbit

SourceDossier is a GenLayer Studionet application for resolving factual claims against two independently fetched HTTPS sources. Validators fetch both URLs themselves, require distinct hostnames, bind SHA-256 digests of the exact response bodies, agree on one evidence code per source, and store a structured verdict with its provenance.

## Why the contract matters

The caller supplies URLs, never copied evidence text. Every validator performs the fetch and classification independently. Validation compares the complete encoded result—including both source digests and both evidence codes—so changing content or disagreement fails closed. The verdict is derived deterministically from the accepted codes.

## Run locally

1. `npm install`
2. `npm run dev`
3. Open the local URL and connect MetaMask to GenLayer Studionet.

Contract source: `contracts/source_dossier.py`. Tests cover URL and hostname rules, duplicate IDs, malformed model output, changed source bytes, and validator disagreement. Public deployment evidence is in `artifacts/`.

## Verified deployment

- Network: GenLayer Studionet
- Contract: `0x5847B68155F2a6Be6Df31A3e2a21492E907D6F5D`
- Deployment transaction: `0x5728cc7a4eaab77d68c41b1e2b9cc78cfde15ffb66ec5c843532f92d27f8d6ac`
- Live test transaction: `0x88050c8224cc733037b5c1c9012214642c0bfc78b68dfc6a7b2ce21bf2ae1887`

No private keys or secrets are stored in this repository.

