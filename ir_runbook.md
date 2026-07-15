# Ransomware Incident Response Runbook

Concise playbook organized by NIST SP 800-61 phases. Use as a checklist during an active incident. **Verify findings before acting** — do not assume scope or attribution.

---

## 1. Preparation

*Complete before an incident occurs. Revisit quarterly.*

- [ ] 1.1 Maintain an incident response contact list (IR lead, legal, PR, executives, MSSP, cyber insurer, law enforcement liaison).
- [ ] 1.2 Document critical assets, data classifications, and recovery priorities (tier 0/1/2 systems).
- [ ] 1.3 Ensure offline, immutable backups exist and test restores at least quarterly.
- [ ] 1.4 Segment networks; restrict lateral movement (least privilege, disable unused RDP/SMB, enforce MFA on remote access).
- [ ] 1.5 Deploy and tune EDR, logging (auth, DNS, proxy, firewall), and centralized SIEM with 90+ day retention.
- [ ] 1.6 Pre-stage an IR toolkit: forensic workstation, write-blockers, spare network gear, out-of-band comms channel.
- [ ] 1.7 Draft and exercise a ransomware-specific playbook (tabletop at least annually).
- [ ] 1.8 Pre-negotiate retainers with external IR counsel and forensic vendors; know cyber insurance claim procedures.
- [ ] 1.9 Define decision authority for isolation, shutdown, ransom payment, and public disclosure.
- [ ] 1.10 Maintain a current network/asset inventory and data-flow diagram for scoping during an incident.

---

## 2. Detection & Analysis

*Confirm the incident, determine scope, and preserve evidence.*

### Initial Triage

- [ ] 2.1 Activate the IR team and switch to the out-of-band comms channel (assume email/Slack may be compromised).
- [ ] 2.2 Record the detection source and time (user report, EDR alert, ransom note, SIEM correlation, helpdesk ticket).
- [ ] 2.3 Capture the ransom note, file extensions, and affected hostnames — photograph screens; do not reboot yet.
- [ ] 2.4 Classify severity and open an incident ticket with a unique ID; start an incident log (who, what, when, action taken).

### Scope & Validation

- [ ] 2.5 Identify patient zero: first encrypted host, first suspicious login, or earliest malicious process.
- [ ] 2.6 Query EDR/SIEM for common ransomware precursors (Cobalt Strike, PsExec, `vssadmin delete shadows`, `bcdedit`, mass file renames).
- [ ] 2.7 Check domain controllers, backup servers, and hypervisors — ransomware often targets these first.
- [ ] 2.8 Review VPN, RDP, and SaaS auth logs for impossible travel, new MFA devices, or after-hours admin logins.
- [ ] 2.9 Determine encryption status: number of hosts, shares, SaaS tenants, and whether backups are affected.
- [ ] 2.10 Identify the ransomware family if possible (note hash, extension, onion URL) — do not visit attacker sites from corporate network.

### Evidence Preservation

- [ ] 2.11 Snapshot or image affected VMs; collect volatile data (memory dump) before shutdown where feasible.
- [ ] 2.12 Preserve relevant logs (firewall, proxy, DNS, AD, EDR, mail gateway) — export with chain-of-custody notes.
- [ ] 2.13 Block known C2 IPs/domains at the perimeter; do not mass-delete artifacts until forensics is consulted.
- [ ] 2.14 Notify legal and cyber insurer; determine regulatory notification obligations (breach vs. availability event).

---

## 3. Containment, Eradication & Recovery

*Stop spread, remove attacker access, restore operations.*

### Containment

- [ ] 3.1 Isolate affected hosts at the network level (EDR network containment or switch port shutdown) — avoid casual power-off unless spreading actively.
- [ ] 3.2 Disable compromised accounts and revoke active sessions (AD, Entra ID, VPN, SaaS, service accounts).
- [ ] 3.3 Block lateral-movement paths: restrict SMB/RDP between segments, disable remote WMI/PsExec where possible.
- [ ] 3.4 If domain compromise is suspected, isolate domain controllers from the internet and peer segments pending triage.
- [ ] 3.5 Protect backups: verify immutability, disconnect backup management interfaces, confirm last clean backup timestamp.
- [ ] 3.6 Communicate internally: instruct staff not to power on machines, not to pay ransom independently, and use out-of-band updates.

### Eradication

- [ ] 3.7 Identify and remove persistence (scheduled tasks, registry run keys, new local admins, GPO changes, web shells).
- [ ] 3.8 Rotate all potentially exposed credentials — prioritize domain admin, service accounts, cloud API keys, and VPN secrets.
- [ ] 3.9 Rebuild compromised hosts from known-good images; do not decrypt-in-place on production without IR approval.
- [ ] 3.10 Patch exploited vulnerabilities and close ingress paths (exposed RDP, unpatched VPN, stolen cookies, phishing vector).
- [ ] 3.11 Validate that C2 channels are dead and no new encryption activity appears for 24–48 hours before broad recovery.

### Recovery

- [ ] 3.12 Restore from the most recent verified clean backup; test a subset before full rollout.
- [ ] 3.13 Recover in priority order (tier 0 → tier 1 → tier 2) per the pre-defined asset list.
- [ ] 3.14 Reconnect systems to the network incrementally; monitor for re-infection (EDR, SIEM watchlists).
- [ ] 3.15 Confirm business-critical services and data integrity with system owners before declaring recovery complete.
- [ ] 3.16 Document ransom payment decision (if any) with legal and executive approval — payment does not guarantee decryption.

---

## 4. Post-Incident

*Learn from the event and harden defenses.*

- [ ] 4.1 Hold a blameless post-incident review within 5 business days; document timeline, root cause, and control gaps.
- [ ] 4.2 Update the incident ticket with final scope: hosts affected, data accessed/exfiltrated, downtime, and recovery time.
- [ ] 4.3 File required regulatory and contractual breach notifications within applicable deadlines.
- [ ] 4.4 Submit cyber insurance claim with evidence package (timeline, costs, forensic report).
- [ ] 4.5 Implement remediation actions with owners and due dates (MFA gaps, backup failures, segmentation, monitoring rules).
- [ ] 4.6 Update detection content: new IOCs, SIEM correlation rules, EDR policies, and phishing indicators.
- [ ] 4.7 Revise this runbook and re-run a tabletop exercise incorporating lessons learned.
- [ ] 4.8 Brief leadership and (if appropriate) staff on outcome, user responsibilities, and reporting procedures.

---

## Quick Reference — First 15 Minutes

1. **Do not panic-pay.** Payment decisions require legal and executive approval.
2. **Isolate** the affected host(s) from the network.
3. **Preserve** ransom notes, screenshots, and logs.
4. **Activate** the IR team on out-of-band comms.
5. **Protect backups** — confirm they are not encrypted and are offline/immutable.
6. **Call** your IR counsel, insurer, and (if engaged) forensic vendor.

*When in doubt, contain first and investigate second.*
