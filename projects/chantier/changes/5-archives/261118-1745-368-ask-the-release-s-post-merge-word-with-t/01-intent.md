# Ask the release's post-merge word with the merge go

In v0.12.0 (CR-352) and v0.13.0 (CR-366), the Release driver handed back after the merge of the
version PR to ask the user's word for the tag and the forge release (CONTRIBUTING.md "Release"
steps 4 and 5). The user said yes, and a second Release driver had to start to run them. The
user's word for those steps could be asked together with the version PR's ready ask, so that one
Release driver runs the procedure to its end after the merge.

Source: batch-27's retro (CR-366), kept by the retro critic.
