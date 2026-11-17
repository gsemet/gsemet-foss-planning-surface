# Verify CR-306, head 5b458421 (matches PR head 5b45842)
1. New test passes at head: `node --test test/site/e2eCampaign.test.ts` -> 10 pass, 0 fail (evidence/after-test.txt). (vitest does not apply; file uses node:test.)
2. Test fails on origin/main with only the test copied in: 9 pass, 1 fail, stdout `FAILED visual: [object Object]; [object Object]` (evidence/before-test.txt).
3. CLI at head, manual manifest: `FAILED visual: home: blank; toc: overflow` (evidence/after-report-line.txt).
4. CI run 43320601382 and heavy run 43320611782: both completed/success, headSha 5b45842.
5. Diff touches only e2e-campaign.mjs, the test, SwRS CORE-076 row and log.md, as specified. `just check` not rerun (reported passing).
VERIFIED
