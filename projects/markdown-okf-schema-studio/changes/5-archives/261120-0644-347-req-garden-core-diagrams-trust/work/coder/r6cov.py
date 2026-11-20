import json
d=json.load(open('out/reports/requirements/requirements-report.json'))
R={x['id']:x for x in d['requirements']}
ids=['CORE-001','CORE-002','CORE-003','CORE-006','CORE-007','CORE-008','DIAG-001','DIAG-006','DIAG-007','DIAG-009','DIAG-015','TRUST-001','TRUST-004','TRUST-006','TRUST-009','TRUST-012','TRUST-014']
for s in ids:
    r=R['StRS-MDOKFSTUDIO-'+s]; c=r['stakeholder_test_coverage']
    miss=[(x['id'][17:],R[x['id']]['frontmatter'].get('req_lifecycle')) for x in c['linked_swrs'] if x['status']!='covered']
    inforce=[m for m in miss if m[1] not in ('superseded','deprecated','retired')]
    print(s, c['status'], 'vt:',c['validation_tests']['status'], c['validation_tests']['files'], 'missing-inforce:',inforce, 'missing-other:',len(miss)-len(inforce))
print(d['stakeholder_test_coverage'])
