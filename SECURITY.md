# Security policy

HomeScout is a public portfolio project. There is no live service yet; the repository contains documentation and, from stage 2, a cost-calculation library.

## Reporting a vulnerability

Please report security issues **privately** using GitHub's private vulnerability reporting: open the repository's **Security** tab and choose **Report a vulnerability**. Don't open a public issue for a security problem.

Include what you found, how to reproduce it, and its likely impact. You'll get an acknowledgement as soon as practical.

## Scope

- Code, workflows and configuration in this repository.
- Secrets or personal data accidentally committed here.

Third-party services and packages are out of scope; report those to their maintainers.

## What's in place

Secret scanning with push protection, Dependabot security updates and alerts, required pull requests on `main`, and GitHub Actions pinned to exact commit versions. See `docs/decisions/0027-stage-2-engineering-hardening.md`.
