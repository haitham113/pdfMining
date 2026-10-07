# Stage 05 PDF comparison fixtures

These 15 PDFs are evaluation fixtures for PdfMining architecture decisions. The nine `core-*` files are matched native, scanned, and mixed variants of three content families. The six `stress-*` files isolate rotation, cropping, reading order, continued tables, degraded OCR, and conflicting figures. They are not production examples or a statistical performance sample.

## World Bank excerpts and attribution

The English and Arabic core families reproduce only two text-only executive-summary pages from each edition of *Land Matters*. The full publisher PDFs are not included here. The source pages were visually inspected for separately credited photos, figures, and tables; none appeared on the selected pages. The publisher's rights pages describe the work as [CC BY 3.0 IGO](https://creativecommons.org/licenses/by/3.0/igo/) and warn that separately owned components can require additional permission.

- English source: Anna Corsi and Harris Selod. 2023. *Land Matters: Can Better Governance and Management of Scarcity Prevent a Looming Crisis in the Middle East and North Africa?* Washington, DC: World Bank. doi:10.1596/978-1-4648-1661-1. License: CC BY 3.0 IGO. [Publisher PDF](https://documents1.worldbank.org/curated/en/099559508272442561/pdf/IDU13ee887eb13670145571be091c0095f45be26.pdf), source PDF pages 19–20.
- Arabic source: آنا كورسي وهاريس سيلود. 2023. *أهمية الأراضي: هل يفلح تحسين الحوكمة وإدارة الندرة في منع وقوع أزمة وشيكة في منطقة الشرق الأوسط وشمال أفريقيا؟* البنك الدولي. doi:10.1596/978-1-4648-1889-9. License: CC BY 3.0 IGO. [Publisher PDF](https://documents1.worldbank.org/curated/en/099605208272415635/pdf/IDU1238311ae1eae41426918dc5170a628fd0af2.pdf), source PDF pages 19–20.

The scanned and mixed files are adaptations created solely for comparison. This adaptation is not by the World Bank; the fixture authors are responsible for its form and any errors. The World Bank has not endorsed PdfMining or these fixtures.

The bilingual and stress files contain fictional, purpose-written content with no external document text or private user material. All fixtures remain subject to the [external-provider controls decided in issue #4](https://github.com/haitham113/pdfMining/issues/4) before any hosted evaluation.

See the [manifest](../../../docs/evaluation/stage-05-corpus-manifest.json) for hashes, source permissions, page geometry, and transformations. The [verified annotations](../../../docs/evaluation/stage-05-corpus-gold-draft.json) record the human-reviewed reference answers and regions.
