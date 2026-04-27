# Security Policy

## Supported Versions

The latest default-branch version is supported for security fixes.

## Reporting a Vulnerability

Please report vulnerabilities privately through GitHub Security Advisories or by contacting repository maintainers directly.

Include:

1. Issue description and impact.
2. Reproduction steps.
3. Affected endpoints or modules.
4. Suggested mitigation, if known.

## Secure Operations Guidance

1. Set `AGENT_TRACER_API_KEY` in environments exposed beyond trusted internal networks.
2. Tune `AGENT_TRACER_RATE_LIMIT_PER_MINUTE` based on expected traffic.
3. Set explicit `AGENT_TRACER_ALLOWED_HOSTS` and `AGENT_TRACER_ALLOWED_ORIGINS` values.
4. Keep `AGENT_TRACER_MAX_STEPS` aligned with retention/privacy requirements.
5. Avoid storing sensitive payloads in trace states when not required.
6. Restrict access to trace retrieval endpoints in production deployments.
