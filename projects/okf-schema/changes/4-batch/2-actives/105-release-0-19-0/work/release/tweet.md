**1/3**

okf-schema 0.19.0 changes how you read a concept. `okf-schema show` now prints the file exactly as stored, comments, quoting and line endings included. The trust tier and staleness moved to a new command, `okf-schema trust`, so update any script that read them from `show`. And `okf-schema index` no longer writes broken links into subdirectory summaries.

**2/3**

Release notes: https://github.com/gsemet/okf-schema/releases/tag/v0.19.0

**3/3**

Install or update with `pip install -U okf-schema`, free under the MIT license: https://pypi.org/project/okf-schema/
