# Feedback and contributions

Report a reproducible issue through the repository's issue tracker when available,
or the channel through which you received this package. Include:

- Package version, distribution commit if available, and verification result.
- Cursor version, OS and selected model if visible.
- Whether the loaded Skill comes from the intended project or another installation.
- A minimal synthetic prompt, expected result and actual result.

Redact personal paths, credentials, private project content and conversation history.
Prefer a small synthetic example over uploading a complete real workspace.

This repository contains generated distribution packages. Accepted method or integration
fixes are made in the maintained development source and regenerated into a new package;
keep local experiments distinct from a verified release. The checksum verifier should
reject a modified package until it has its own reviewed manifest.

A structural test does not establish semantic correctness or real Cursor support.
Use the [validation protocol](ACCEPTANCE.md) when reporting discovery, correction,
approval, recovery or coexistence results. Follow the existing [MIT license](LICENSE).
