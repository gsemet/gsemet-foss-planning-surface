# A test catches a non-JSON, non-Markdown file in the planning folder

Planning-folder file types checked by a test (batch-11 retro). CR-184 Inspector caught a plain-text number file in the planning folder, where chantier writes only JSON and Markdown. A structure test or the long gate should catch a non-JSON, non-Markdown file the CLI writes there.