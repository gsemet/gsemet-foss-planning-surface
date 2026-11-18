import { pathToFileURL } from 'node:url';
const { renderMarkdown } = await import(pathToFileURL(process.argv[2]).href);
const fm = '---\ntype: cr-spec\ndescription: x\n---\n\n# Title\n\nText.\n';
const cases = {
  plain: fm,
  bom: '\ufeff' + fm,
  crlf: fm.replace(/\n/g, '\r\n'),
  empty: '---\n---\n# T\n',
  unclosed: '---\ntype: x\n\n# Heading\n',
  none: '# Title\n\nText.\n',
};
for (const [k, v] of Object.entries(cases)) console.log(k + ': ' + JSON.stringify(renderMarkdown(v)));
