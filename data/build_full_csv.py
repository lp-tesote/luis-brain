#!/usr/bin/env python3
"""Join the per-client x bank pressure summary with HubSpot subscription amounts
into one analysis-ready CSV."""
import csv, os
HERE = os.path.dirname(os.path.abspath(__file__))
EXCLUDE = {"Tesote Developer","Tesote Ventas","Tesote Finance","Tesote Technologies"}

# subscription per client
subs = {}
with open(os.path.join(HERE,"bank-api-batch-1-subscriptions.tsv")) as f:
    for r in csv.DictReader(f, delimiter="\t"):
        subs[r["client"]] = r

BANK_ORDER = {"BBVA":1,"Banesco":2,"Mercantil":3,"Bancaribe":4}
rows = []
with open(os.path.join(HERE,"bank-api-batch-1-client-bank-summary.csv")) as f:
    for r in csv.DictReader(f):
        c = r["client"].strip()
        if c in EXCLUDE: continue
        for k in ("client_entities_total","entities_at_bank","accounts_at_bank",
                  "active_accounts_at_bank","tx_total","tx_last_90d"):
            r[k] = (r[k] or "0").replace(",","")
        s = subs.get(c, {})
        rows.append({
            "client": c,
            "client_entities_total": r["client_entities_total"],
            "bank": r["bank"],
            "entities_at_bank": r["entities_at_bank"],
            "accounts_at_bank": r["accounts_at_bank"],
            "active_accounts_at_bank": r["active_accounts_at_bank"],
            "tx_total": r["tx_total"],
            "tx_last_90d": r["tx_last_90d"],
            "monthly_amount_usd": s.get("monthly_amount_usd",""),
            "mrr_usd": s.get("mrr_usd",""),
            "hubspot_deal": s.get("hubspot_deal",""),
            "match_confidence": s.get("match_confidence","no_won_deal"),
        })

rows.sort(key=lambda x:(BANK_ORDER.get(x["bank"],9), -int(x["tx_last_90d"] or 0)))
cols = ["client","client_entities_total","bank","entities_at_bank","accounts_at_bank",
        "active_accounts_at_bank","tx_total","tx_last_90d","monthly_amount_usd","mrr_usd",
        "hubspot_deal","match_confidence"]
out = os.path.join(HERE,"bank-api-batch-1-full.csv")
with open(out,"w",newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader(); w.writerows(rows)
print(f"Wrote {len(rows)} rows to {out}")
