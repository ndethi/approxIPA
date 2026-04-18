# BibleTTS Hugging Face Access Status

## Current Finding
A public Hugging Face dataset does not require an API key to download. Gated or private datasets do require a token.

## What We Know Now
- A Kikuyu BibleTTS dataset was not confirmed in Hugging Face search results during this workspace session.
- Therefore the exact repository ID and access mode still need confirmation.
- If the dataset is publicly listed, download helpers such as `huggingface_hub.snapshot_download()` or `hf_hub_download()` can be used without a token.
- If the dataset is gated or private, a Hugging Face token is required.

## Operational Rule
Do not block the BibleTTS fallback workflow on an API key unless the dataset page is explicitly gated or private.

## Next Action
Confirm the exact Hugging Face repo ID for the Kikuyu BibleTTS dataset and whether it is public, gated, or private.
