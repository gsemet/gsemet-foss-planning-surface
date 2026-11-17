# Report: short demo video process

PR: [#314](https://github.com/gsemet/markdown-okf-schema-studio/pull/314) · merged 2026-11-04 as `e086c4bf`.

## Delivered

- The 57.5-second demo video of the extension, filmed in real VS Code and assembled with Remotion:
  `docs/demo-video/short-demo-01/output/short-demo-01.mp4`, in Git LFS.
- The guide `docs/demo-video/guidelines/short-demo-process.guidelines.md`: making, editing, reviewing
  and assembling a video, up to publication, with the live storyboard as its first rule.
- The folder `docs/demo-video/short-demo-01/`: storyboard, panel pictures, the set of the video
  (`stage/`) and the scripts (`kit/`). `docs/demo-video` stays out of the VSIX.

## Working files

`demo-video/` holds the working folders of the 15, 40 and 59-second rounds, moved from the backlog
item `demo-video`. Their `node_modules` link was removed: it pointed to a scratch folder. The
storyboard of record is now the one in the repository.

## Open items

- `just preflight` passed before the last caption correction (storyboard text, pictures and video
  only); the owner asked not to run it again on the squashed commit.
- The other video ideas are in the P3 backlog item `demo-video-1-feature`.
