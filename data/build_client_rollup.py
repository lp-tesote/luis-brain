#!/usr/bin/env python3
"""Client-level rollup across all 4 selected banks, with MRR.
Columns: client, total_entities, active_bank_accounts, tx_last_90d, mrr_usd."""
import csv, os
HERE = os.path.dirname(os.path.abspath(__file__))
EXCLUDE = {"Tesote Developer","Tesote Ventas","Tesote Finance","Tesote Technologies"}

# subscription per client -> effective MRR = mrr_usd if present else monthly_amount_usd
mrr = {}
with open(os.path.join(HERE,"bank-api-batch-1-subscriptions.tsv")) as f:
    for r in csv.DictReader(f, delimiter="\t"):
        m = r["mrr_usd"] or r["monthly_amount_usd"]
        mrr[r["client"]] = m

agg = {}  # client -> dict
with open(os.path.join(HERE,"bank-api-batch-1-client-bank-summary.csv")) as f:
    for r in csv.DictReader(f):
        c = r["client"].strip()
        if c in EXCLUDE: continue
        for k in ("client_entities_total","active_accounts_at_bank","tx_total","tx_last_90d"):
            r[k] = (r[k] or "0").replace(",","")
        a = agg.setdefault(c, {"total_entities": int(r["client_entities_total"]),
                               "active_bank_accounts": 0, "tx_last_90d": 0, "tx_total": 0})
        a["active_bank_accounts"] += int(r["active_accounts_at_bank"])
        a["tx_last_90d"]          += int(r["tx_last_90d"])
        a["tx_total"]             += int(r["tx_total"])

rows = [{"client": c, "total_entities": v["total_entities"],
         "active_bank_accounts": v["active_bank_accounts"],
         "tx_last_90d": v["tx_last_90d"], "tx_total": v["tx_total"],
         "mrr_usd": mrr.get(c, "")} for c, v in agg.items()]
rows.sort(key=lambda x: -x["tx_last_90d"])

out = os.path.join(HERE,"bank-api-batch-1-client-rollup.csv")
with open(out,"w",newline="") as f:
    w = csv.DictWriter(f, fieldnames=["client","total_entities","active_bank_accounts","tx_last_90d","tx_total","mrr_usd"])
    w.writeheader(); w.writerows(rows)
print(f"Wrote {len(rows)} clients to {out}")
