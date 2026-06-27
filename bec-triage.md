9:53 PM
Email Triage Report — Suspected CEO Fraud (BEC)

Analyst note: Based on the headers provided. Verify all findings before acting. Do not initiate any transfer.
(1) Origin — Where Did This Email Actually Come From?

The email did not originate from Meridian Group's infrastructure.

The key line is:
Received: from [192.168.43.7] (unknown [41.223.57.188])

    41.223.57.188 is the real public IP that connected to Gmail's servers
    Geolocation of 41.223.57.188 places it in Nigeria (AFRINIC-managed IP block, AS29465 — MTN Nigeria Communications)
    192.168.43.7 is a private/internal IP — likely a phone hotspot or local device the sender used. It tells us nothing useful, but it's consistent with a mobile device on a cellular network
    The email was then routed through Google's servers (smtp.gmail.com → mail-lj1-f201.google.com) before arriving at Meridian Group

In plain English: Someone in Nigeria used Gmail to send an email pretending to be your CEO. It never touched Meridian Group's mail servers until it landed in the inbox.

    ⚠️ Verify: IP geolocation isn't perfect. Confirm via a tool like ipinfo.io or AbuseIPDB. VPNs can also shift apparent location — though the MTN Nigeria ASN is a strong signal.

(2) What the DKIM, SPF, and DMARC Failures Mean

DKIM — fail (signature did not verify)
DKIM is a cryptographic signature that proves an email wasn't tampered with and actually came from the claimed domain's mail server. A failure means one of two things: the email was modified in transit, or — more likely here — it was never sent from meridiangroup.com's servers at all. The signature is invalid because the real mail server didn't sign it.

SPF — softfail (domain of transitioning sender)
SPF checks whether the sending server (Gmail, in this case) is authorized to send mail on behalf of meridiangroup.com. A softfail means Gmail is not on the authorized senders list, but the domain's SPF policy isn't strict enough to outright reject it. This is a policy weakness on Meridian Group's side — the domain should be set to ~all or -all with tighter controls.

DMARC — fail (p=none)
DMARC ties SPF and DKIM together and tells receiving mail servers what to do when both fail. Here, p=none means the domain owner said "do nothing — just report." That's why this email wasn't blocked — Meridian Group's DMARC policy is in monitoring mode, not enforcement. A properly configured p=reject policy would have stopped this before it reached the inbox.

Combined meaning: All three authentication layers failed or were too weak to block the email. The message has no legitimate claim to the meridiangroup.com domain.
(3) The Reply-To Discrepancy — What It Means and Why Attackers Use It
Field	Value
From	marcus.webb@meridiangroup.com
Reply-To	mwebb.ceo2026@gmail.com

The From field is what the victim sees in their email client — it looks like the CEO. The Reply-To field silently redirects any response to a Gmail address the attacker controls.

This is a deliberate, classic technique in Business Email Compromise (BEC). Here's the attacker's logic:

    They can't send from marcus.webb@meridiangroup.com without access to that account (hence the spoofed From)
    But they need replies to go to them, not to the real CEO
    So they insert a Reply-To that most employees will never notice — your email client auto-populates it when you hit Reply

If an employee responds, confirms the wire, or sends banking details — it all goes straight to the attacker. The real Marcus Webb never sees any of it.

    ⚠️ The Gmail address mwebb.ceo2026@gmail.com is also a tell — "2026" appended to a name is a common pattern in freshly created fraud accounts.

(4) Verdict — Legitimate, Spoofed, or Compromised Account?

This is a spoofed email. Not a compromised account.

Here's the reasoning:

    A compromised account would show the email originating from Meridian Group's own infrastructure, and DKIM would likely pass (since it would be sent through the real mail server)
    Instead, the email came from a Nigerian IP via Gmail, DKIM failed, and the Reply-To routes to an external Gmail account — all consistent with domain spoofing, not account takeover

This is a textbook Business Email Compromise (BEC) / CEO Fraud attempt.
Signal	Finding
Origin	Nigeria (MTN, AS29465) via Gmail
DKIM	Failed — not sent from real server
SPF	Softfail — Gmail not authorized
DMARC	Failed — policy too weak to block
Reply-To	Attacker-controlled Gmail
Request type	Urgent wire transfer

Confidence level: High (roughly 95%)

The remaining 5% accounts for the unlikely scenario that your CEO is traveling, using a personal Gmail for some reason, and routed through a Nigerian cell network — possible in theory, eliminated easily with one phone call.
Immediate Actions — Next 30 Minutes

    Do not reply to the email. Do not click anything in it.
    Call Marcus Webb directly on a phone number from your company directory — not from anything in this email. Ask if he sent it. This takes 60 seconds and ends the ambiguity.
    Do not initiate any wire transfer until verbal confirmation is obtained through a known, trusted channel.
    Escalate to your security team and forward the raw headers — not just the email body.
    Preserve everything — don't delete or move the email until your security team has reviewed it.

The phone call is your ground truth. Everything else is analysis.
