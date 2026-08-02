# CHANGELOG

All notable changes to this project will be documented in this file.


## PHASE 5.5-C1.5 - Audit Evidence Review

### Added
- Verified SecurityEvent audit contract.
- Verified central security event writer.
- Verified device and login security evidence flows.

### Evidence
- SecurityEvent schema validated.
- Runtime security_events evidence verified.
- Tenant isolation verified.

### Gap
- GAP-5.5-C1.5-001
- DEVICE_BLOCKED_BY_ADMIN missing actor attribution.
- Deferred to future Security Audit Hardening Phase.

## [v5.5.1-Enterprise] - 2026-07-15
### Added
- Integrated pricing layers and mobile responsive routing targets inside the landing interface layer.

### Fixed
- Fixed runtime ORM dependency compilation blockades within multi-tenant database contexts via isolated dynamic injection.
- Synchronized compliance testing data pipelines to support mock payload authentication states safely.

## Phase 6.0.5-D1 - Purchase Receive Audit Evidence

- Added Purchase Receive AuditLog integration.
- Added RECEIVE business event evidence.
- Runtime verification pending due to unavailable PurchaseOrder data.
- Procurement Data Availability Gap recorded.

Commit: 637ec2b

## PHASE 5.4 - Security Event Risk Enrichment

### Added
- Added login_session_id binding to SecurityEvent.
- Added device_session_id binding to SecurityEvent.
- Added risk_score storage.
- Added risk_level storage.

### Evidence
- NEW_DEVICE_LOGIN verification passed.
- LoginSession → SecurityEvent trace verified.
- Security event enrichment migration completed.

Commit:
0a94ea2
