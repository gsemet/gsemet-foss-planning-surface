const base = 'file:///C:/Users/gaeta/Projets/chantier.worktrees/batch-30-CR-449/skills/chantier/scripts/cli/src/chantier/clients/web/js/';
const { discussion } = await import(`${base}panel/griller-view.js`);
const { textOf } = await import(`${base}core/dom.js`);
const g = { available: true, cli: 'claude', machine: 'pc', model: 'opus', running: null, conversation: null };
console.log(textOf(discussion(g, 'me')));
const turns = [
  { n: 1, from: 'x', user: '<b>hi</b>', answer: '# A\nok', state: 'done', wrote: ['02-answers.md'], grilled: 'next batch' },
  { n: 2, from: 'me', user: 'q', state: 'failed', error: 'boom', wrote: ['a'] },
  { n: 3, from: 'me', user: 'q', state: 'running', wrote: [] },
];
console.log(textOf(discussion({ ...g, conversation: { turns } }, 'me')));
console.log(textOf(discussion({ available: false, reason: 'nope' }, 'me')));
