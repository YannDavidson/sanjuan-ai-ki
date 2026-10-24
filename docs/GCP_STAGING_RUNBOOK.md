# Google Cloud staging runbook

Project: `sanjuan-ki` (`475971379811`). Billing is confirmed by project owner, not independently inspected.

## Before provisioning

1. `gcloud auth login` and `gcloud config set project sanjuan-ki`.
2. Inspect existing resources: `gcloud run services list --project sanjuan-ki`, `gcloud sql instances list --project sanjuan-ki`, `gcloud artifacts repositories list --project sanjuan-ki`, and `gcloud billing projects describe sanjuan-ki`.
3. Review IAM, billing, budgets and available regions; never overwrite existing services without review.
4. Choose a region after checking cost and latency; `us-east1` is an example only.

## API staging container

`Dockerfile.api` runs FastAPI on Cloud Run's `PORT` (default 8080), includes repository knowledge definitions, and uses a non-root runtime user. Build the image using Cloud Build or Docker into an existing or newly approved Artifact Registry repository. Verify `gcloud builds submit --help` before choosing the build command.

After image publication, deploy **privately first** with service name `sanjuan-ki-api-staging`, `--min-instances 0`, `--max-instances 2`, `--memory 512Mi`, and `--no-allow-unauthenticated`. Validate `/health`, `/ask`, CORS and corpus availability with authenticated test requests. Configure a dedicated service account and Secret Manager before adding external model keys.

The web service needs a separate verified Next.js standalone image; do not expose the API publicly until web integration, central rate limiting and security review pass. The current in-memory rate limiter is per instance and insufficient as a public hard quota.

## Go/no-go

- [ ] Existing services, billing and IAM inspected
- [ ] Budget alerts and hard application quotas configured
- [ ] API container built and staging smoke tests pass
- [ ] Web staging deployment and source registry pass
- [ ] Secrets, monitoring, TLS, CORS, rollback verified
- [ ] Reviewer authorizes public access
