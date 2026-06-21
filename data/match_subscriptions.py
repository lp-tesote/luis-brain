#!/usr/bin/env python3
"""Match bank-API batch-1 clients to their HubSpot Closed Won subscription amount.
Outputs a joined table with a confidence flag per row, plus unmatched lists."""
import csv, re, unicodedata, os

HERE = os.path.dirname(os.path.abspath(__file__))

# --- HubSpot Closed Won deals: (deal_name, amount_usd, mrr_or_None) ---
DEALS = [
 ("Cashea",7000,7000),("Farmacias San Francisco",4000,None),("Agroavícola del Llano",3500,None),
 ("Mykonos",3150,None),("Kaizen",3000,None),("Grupo F",3000,None),("Seguros Crecer",3000,None),
 ("Forum Supermayorista",2399,None),("Grupo Abreu",2199,None),("Grupo Velutini",1999,None),
 ("Crixto",1999,1999),("Balú - Grupo Futura",1900,None),("Covencaucho Industrias S.A",1750,None),
 ("Grupo Cometa",1700,1700),("Red de farmacias San Ignacio",1500,2000),("Arajet",1500,1650),
 ("NetUno",1499,None),("Canguro Venezuela",1350,None),("Di Massi",1200,1500),("Prevaler",1150,None),
 ("Camor International",1100,None),("Bande Corp",1000,900),("Real Seguros",1000,1250),
 ("Alimentos Munchy",1000,None),("Futura Retail",1000,None),("Farmabien",1000,None),
 ("Tu Aliado Venezuela",1000,None),("Grupo Gipsy",1000,None),("Inquiport",1000,None),
 ("Alimentos L'Prado",999,None),("Plan B",999,None),("Constructora Pedeca",999,None),
 ("Gerais",850,None),("Seguros Venezuela",849,849),("En Otro Orden de Ideas",800,1000),
 ("Lácteos Torondoy",800,1000),("Megalabs",800,None),("Alimentos Las Tunas C.A",799,799),
 ("Grupo Canaima",750,None),("Besser Solutions - New Deal",750,None),("Grupo Mimesa",750,1500),
 ("Grupo Avila",750,None),("Supermercados Luxor",750,None),("Inversiones PAD 21",750,None),
 ("Hageco",750,375),("Disbattery",750,None),("ASOPORTUGUESA",750,None),("Viva Supercentro",749,None),
 ("Euromercado",729,777.81),("Grupo Leiros",699,None),("Laboratorios Pharmakum",693,600),
 ("APB Group",650,650),("Granos Sagrados Trading Corp - New Deal",650,650),("Mangocenter",649,None),
 ("Cruz Roja Venezolana",612.5,875),("Latinbien (Grupo Ramvall)",600,900),("Protinal Proagro",600,600),
 ("Empresas Tapa Amarilla",599,None),("Hispana de Seguros",599,None),("Crustissimo",599,None),
 ("Alimentos La Giralda",572.92,572.92),("Grupo Oriand",550,None),("Estar Seguros, S.A.",549,None),
 ("Fivenca",500,None),("Suvica",500,None),("Innova Centro",500,500),("Promaker",500,None),
 ("Corporación Bel",500,800),("Coseimpa",500,None),("Yummy",500,None),("Ualeet / COINXPRESS",499,None),
 ("Grupo NSM",499,None),("Casagri",490,700),("Robust Tires",455,650),
 ("Centro Medico de Oncologia - New Deal",455,650),("Grupo Bazzi",450,None),("Pineco",450,None),
 ("Molina Viajes",450,None),("Casa MAR",450,None),("Abonos Dominicanos",450,450),
 ("Acabados y Pinturas- Sherwin Williams",450,None),("Grupo Nueve Once",449,None),
 ("Capital Foods",449,None),("LABORATORIOS KIMICEG",449,None),("Cencozotti",449,None),
 ("Grupo Rica",449,None),("Eway",449,None),("Latinoamericana de Carbon - New Deal",449,None),
 ("Tu Gruero",449,None),("Alvarigua",449,None),
 ("Comercializadora de Alimentos Global M&P, C.A",400,400),("Socado",400,None),
 ("Grupo Medisolutions",379,None),("Grupo Landa",375,None),("Dinamo",375,None),("Motasa",350,None),
 ("Sizuca",350,None),("goliiive",350,None),("La Sante",350,None),("Grupo Parawa",350,None),
 ("Curiara",350,None),("Laboratorios Biotech",350,350),("Comercializadora Tiares",350,350),
 ("Marsoca",350,None),("Traki",349,None),("Paisa (Pasteurizadora Táchira)",349,None),
 ("Elmor",349,None),("Quo Vadis Viajes",349,None),("GSI Food",349,None),("Jomi App",349,None),
 ("Corporación Angles",349,None),("Alimentos Arawak",332.5,475),("Binaural",325,325),
 ("Maxy Sweet (Grupo Da Silva)",315,450),("Grupo del Este",300,None),("Distribuidora Inmarket",300,None),
 ("Armi",300,None),("Tamayo & CIA S.A",300,None),("Tealca",300,None),("Grupo Maralac",299,None),
 ("Global Care Pharma",297.5,425),("Supermercados RioVida",250,None),("Importadora VDT",250,250),
 ("Ama de Casa",250,None),("Sanucorp",249,None),("Cines Unidos",225,None),("Flety",130,None),
 ("CALA",100,None),("VICTUM LEGAL",100,None),("Marambio Rivillo Perez Pineda",50,None),
 ("Grupo Oriand - Odoo Connector",0,0),
]

# Manual aliases for cases normalization can't bridge (concatenations, acronyms, entity names).
# client (as in TSV) -> deal_name (as in DEALS)
ALIAS = {
 "Bandecorp":"Bande Corp","Dimassi":"Di Massi","alimentosmunchy":"Alimentos Munchy",
 "Capitalfoods":"Capital Foods","Gruporica":"Grupo Rica","Sanu Corp":"Sanucorp",
 "ALIMENTOS LPRADO":"Alimentos L'Prado","Supermercados Rio Vida":"Supermercados RioVida",
 "SEGVEN":"Seguros Venezuela","EOODI":"En Otro Orden de Ideas","Valles del Turbio":"Importadora VDT",
 "Grupo UP":"Constructora Pedeca","CONSORCIO MEDISOLUTIONS":"Grupo Medisolutions",
 "Corporación Tu Aliado Digital":"Tu Aliado Venezuela","AVICOLA LAS TUNAS":"Alimentos Las Tunas C.A",
 "Grupo cashea":"Cashea","Crixto Venezuela":"Crixto","TORONDOY":"Lácteos Torondoy",
 "Grupo Ramvall":"Latinbien (Grupo Ramvall)","Maxy Sweet":"Maxy Sweet (Grupo Da Silva)",
 "Pharmakum":"Laboratorios Pharmakum","Alimentos Global":"Comercializadora de Alimentos Global M&P, C.A",
 "Somos Jomi C.A":"Jomi App","Soluciones Tu Gruero":"Tu Gruero","Grupo Quo Vadis":"Quo Vadis Viajes",
 "GRUPO MOLINA VIAJES":"Molina Viajes","Protinal":"Protinal Proagro","Procesadora Marsoca":"Marsoca",
 "Laboratorios Elmor":"Elmor","Arawak":"Alimentos Arawak","Cruz Roja":"Cruz Roja Venezolana",
 "Granos Sagrados":"Granos Sagrados Trading Corp - New Deal","Grupoforum":"Forum Supermayorista",
 "GRUPO DINAMO":"Dinamo","Grupo traki":"Traki","Crecer":"Seguros Crecer","Casagri de Lara":"Casagri",
 "Alimentos Alvarigua, c.a.":"Alvarigua","GRUPO MAR":"Casa MAR",
 "Grupo Vertice":"Mykonos","CAMOR INTERNACIONAL":"Camor International",
 "MARCAS PROPIAS":"Balú - Grupo Futura","GRUPO FUTURA":"Futura Retail",
 # confirmed by Luis 2026-06-02:
 "Corporación JSL, C.A.":"Crustissimo","PASTCA":"Paisa (Pasteurizadora Táchira)","Welf":"GSI Food",
}
LOW_CONF_ALIAS = set()  # all alias matches confirmed correct by Luis
# Internal Tesote workspaces — exclude from analysis entirely.
EXCLUDE = {"Tesote Developer","Tesote Ventas","Tesote Finance","Tesote Technologies"}
# Clients with no real Closed Won deal — block spurious token matches.
NO_MATCH = {"Noordzee Fantasie Luxury Group"}

SUFFIX = {"ca","sa","cia","srl","inc","corp","llc","c","a","s","sociedad","anonima","compania"}
def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii","ignore").decode()
    s = s.lower().replace("- new deal","").replace("new deal","")
    s = re.sub(r"[^a-z0-9 ]"," ", s)
    toks = [t for t in s.split() if t and t not in SUFFIX]
    return " ".join(toks), set(toks)

deal_by_name = {d[0]: d for d in DEALS}
deal_norm = {d[0]: norm(d[0]) for d in DEALS}

# unique clients from the summary TSV
clients = []
seen = set()
with open(os.path.join(HERE,"bank-api-batch-1-client-bank-summary.csv")) as f:
    for row in csv.DictReader(f):
        c = row["client"].strip()
        if c and c not in seen and c not in EXCLUDE:
            seen.add(c); clients.append(c)

def match(client):
    if client in NO_MATCH:
        return None,"none"
    if client in ALIAS:
        conf = "low" if client in LOW_CONF_ALIAS else "high"
        return ALIAS[client], conf
    cn, ct = norm(client)
    # normalized exact
    for dn,(dnn,dtt) in deal_norm.items():
        if dnn==cn: return dn,"high"
    # substring containment (>=4 chars)
    for dn,(dnn,dtt) in deal_norm.items():
        if len(cn)>=4 and len(dnn)>=4 and (cn in dnn or dnn in cn): return dn,"medium"
    # distinctive shared token (Jaccard)
    best=None;bestj=0
    for dn,(dnn,dtt) in deal_norm.items():
        if not ct or not dtt: continue
        j=len(ct&dtt)/len(ct|dtt)
        if j>bestj: bestj=j;best=dn
    if bestj>=0.5: return best,"medium"
    if bestj>0:    return best,"low"
    return None,"none"

rows=[]; unmatched=[]
used=set()
for c in clients:
    dn,conf = match(c)
    if dn:
        d=deal_by_name[dn]; used.add(dn)
        rows.append((c,dn,d[1],d[2],conf))
    else:
        unmatched.append(c)

rows.sort(key=lambda r:-(r[2] or 0))
print(f"{'CLIENT':<34}{'HUBSPOT DEAL':<40}{'MO_AMT':>8}{'MRR':>8}  CONF")
print("-"*100)
for c,dn,amt,mrr,conf in rows:
    print(f"{c[:33]:<34}{dn[:39]:<40}{amt:>8}{(mrr if mrr is not None else ''):>8}  {conf}")

with open(os.path.join(HERE,"bank-api-batch-1-subscriptions.tsv"),"w",newline="") as f:
    w=csv.writer(f,delimiter="\t")
    w.writerow(["client","monthly_amount_usd","mrr_usd","hubspot_deal","match_confidence"])
    for c,dn,amt,mrr,conf in sorted(rows,key=lambda r:r[0].lower()):
        w.writerow([c,amt,(mrr if mrr is not None else ""),dn,conf])
    for c in sorted(unmatched,key=str.lower):
        w.writerow([c,"","","","no_won_deal"])

print(f"\n=== MATCHED {len(rows)}/{len(clients)} clients ===")
print(f"\nUNMATCHED CLIENTS ({len(unmatched)}): "+", ".join(unmatched))
unused=[d[0] for d in DEALS if d[0] not in used]
print(f"\nWON DEALS NOT MATCHED TO ANY CLIENT ({len(unused)}): "+", ".join(unused))
