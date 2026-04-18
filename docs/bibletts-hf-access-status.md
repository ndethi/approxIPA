# BibleTTS Hugging Face Access Status

## Current Finding
A public Hugging Face dataset does not require an API key to download. Gated or private datasets do require a token.

For BibleTTS specifically, the official project links point to OpenSLR (SLR129) as the data distribution source, not to a canonical Hugging Face dataset repository.

## What We Know Now
- A Kikuyu BibleTTS dataset was not confirmed in Hugging Face search results during this workspace session.
- The BibleTTS project page and repo point to OpenSLR SLR129 for data downloads.
- OpenSLR SLR129 explicitly lists aligned data for six languages (Asante Twi, Akuapem Twi, Ewe, Hausa, Lingala, Yoruba).
- Kikuyu appears on the project website statistics table but without aligned data links in the public SLR129 package listing.
- If a separate Hugging Face mirror exists, the exact repo ID is still unknown and must be provided explicitly.

## Operational Rule
Do not block workflow on a Hugging Face API key unless a specific Hugging Face repository is confirmed and is gated/private. For now, treat OpenSLR SLR129 as the primary public source.

## Next Action
1. Use OpenSLR SLR129 as the authoritative public source for immediately available BibleTTS data.
2. Confirm whether a Kikuyu aligned subset exists outside SLR129 (maintainer contact or project updates).
3. If a Hugging Face mirror is identified later, record its repo ID and access mode.
