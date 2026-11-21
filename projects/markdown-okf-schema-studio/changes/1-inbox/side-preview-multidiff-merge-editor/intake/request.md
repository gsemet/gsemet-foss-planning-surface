# Side preview: multi-file diff and merge editor not supported

Known limit left by CR-455 (side-preview-diff-gaps, spec decision 10): the side preview does not follow the multi-file diff editor nor the merge editor, because VS Code gives no tab input class for them in the API. Decide whether to support them some other way or document the limit.