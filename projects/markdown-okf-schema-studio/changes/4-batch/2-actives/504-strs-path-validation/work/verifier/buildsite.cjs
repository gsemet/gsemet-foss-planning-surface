// usage: node buildsite.cjs <compiled write.js> <site root> <report json> <repository root>
const [writeJs, siteRoot, report, root] = process.argv.slice(2);
const model = require(writeJs).writeViewerPages(siteRoot, report, root);
const stats = model ? { ...model.stats, scopes: undefined, retired: undefined, activeLifecycles: undefined } : model;
console.log(JSON.stringify(stats));
