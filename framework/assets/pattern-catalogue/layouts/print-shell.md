<!-- ROLE: asset (pattern). STATUS: T3 stub — author full entry on first use. -->

# Pattern: print-shell

```yaml
id: print-shell
kind: layout-primitive
purpose: Print / PDF-friendly shell for invoices, receipts, reports — no app
  chrome, page-margin discipline, print-CSS rules baked in.
status: stub

when-to-use:
  - Invoice / receipt / statement / report rendered for print or PDF export
  - Surfaces accessed primarily through "Print" or "Download PDF"

when-not-to-use:
  - Web-first content that occasionally prints (use detail-page with print-friendly CSS)

variant-clusters: invoice, statement, audit-report, certificate

related: detail-page (print-friendly variant), confirmation-receipt
```

> **Author the full entry when:** the first brief requires print/PDF rendering as a primary deliverable. Use `app-shell-with-sidebar.md` as the structural reference.
