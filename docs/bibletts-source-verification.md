# BibleTTS Source Verification Notes

## Verified Links
- Project page: https://masakhane-io.github.io/bibleTTS/
- GitHub page/repo: https://github.com/masakhane-io/bibleTTS
- Data link from project page: http://www.openslr.org/129/ (SLR129)

## Verified Facts
- BibleTTS project page points to OpenSLR SLR129 as the data distribution endpoint.
- OpenSLR SLR129 lists aligned packages for six languages: Asante Twi, Akuapem Twi, Ewe, Hausa, Lingala, Yoruba.
- Kikuyu appears in BibleTTS project statistics but does not appear as an aligned public package in SLR129 listing.
- No canonical Hugging Face BibleTTS dataset ID for Kikuyu was confirmed in this session.

## Access Implication
- API key/token is not required for public OpenSLR downloads.
- If a future Hugging Face mirror is found and is gated/private, a Hugging Face token will be required.

## Operational Impact
- The BibleTTS mining workflow in this repo is valid and ready.
- Actual Kikuyu mining execution is blocked until a Kikuyu aligned BibleTTS subset is obtained from an authoritative source.
