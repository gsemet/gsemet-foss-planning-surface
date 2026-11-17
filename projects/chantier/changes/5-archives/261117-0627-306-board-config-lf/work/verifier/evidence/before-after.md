# before-after

Before: 51a3c8e (base). After: d15df0b.

- test_the_surface_file_edit_writes_lf_onto_a_crlf_file: before 2 failed (CR kept), after passed. Reproduce: pytest skills/chantier/scripts/cli/tests/test_playbook_edit.py -q with the base src on PYTHONPATH, then the head's.
