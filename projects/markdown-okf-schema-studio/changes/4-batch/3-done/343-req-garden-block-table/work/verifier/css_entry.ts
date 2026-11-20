// Verifier probe entry: print the produced CSS of the two split style modules.
import { EDIT_MODE_CSS } from "SRC/core/preview/styles/editModeStyles";
import { CONTENT_BLOCK_CSS } from "SRC/core/preview/styles/contentBlockStyles";
process.stdout.write(EDIT_MODE_CSS + "\n=====SPLIT=====\n" + CONTENT_BLOCK_CSS);
