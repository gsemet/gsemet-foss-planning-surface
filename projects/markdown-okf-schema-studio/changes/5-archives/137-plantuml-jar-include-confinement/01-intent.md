# PlantUML JAR: includes are not fully confined to the workspace

Left over from CR 135 (T2). The JAR runs with the ALLOWLIST profile and the workspace folder as
allowlist path, but PlantUML's own check still reads an include path that leaves the workspace
through parent segments and an absolute path into a sibling folder whose name starts with the
workspace folder name. Recorded as a Known issue in SwRS DIAG-084.

## Expected

Resolve `!include` lines in the extension before the JAR runs (or refuse sources whose includes
leave the root), test with such sources, and remove the Known issue of DIAG-084.
