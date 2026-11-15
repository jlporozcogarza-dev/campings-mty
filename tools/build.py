# Une data.json (+ nuevos.json) + fotos.json -> data.js. Solo campings que rentan lugar y tienen precio o contacto.
import json, re, os
d = json.load(open("data.json", encoding="utf-8"))
for extra in ("google.json", "nuevos.json"):
    if os.path.exists(extra): d += json.load(open(extra, encoding="utf-8"))
F = json.load(open("fotos.json", encoding="utf-8"))
# No rentan lugar (zonas públicas, predios informales) o no tienen contacto real
FUERA = {"las-adjuntas-santiago","la-camotera","rio-ramos-allende","rio-pilon-montemorelos","vista-potrero","cabanas-laguna-azul-galeana","rio-escondido-glamp-camp","la-charca-ma"}
d = [c for c in d if c["id"] not in FUERA and (c.get("precio_min_mxn") or (c.get("contacto") or "").strip())]
ZONA = {"San Isidro (Sierra de Santiago)":"Laguna de Sánchez","Hidalgo (El Potrero Chico)":"Potrero Chico","Cumbres de Monterrey (sur de Monterrey)":"Monterrey"}
FOTO = {"Laguna de Sánchez":"laguna-sanchez","Potrero Chico":"potrero-chico","Monterrey":"chipinque2","Ciénega de González":"cienega",
        "Potrero Redondo":"matacanes","Presa La Boca":"presa2","Allende":"allende","Iturbide":"iturbide","La Huasteca":"huasteca2",
        "El Cercado":"cola-de-caballo","Cola de Caballo":"cola-de-caballo","García":"garcia-grutas","Santiago":"santiago","Las Adjuntas":"matacanes","El Cercado":"santiago","San Juan Bautista":"santiago","San José de las Boquillas":"santiago"}
MALAS = re.compile(r"Castillo|Murallas|Tobaruela|SanFelices|Agave|Chaparro|Thymophylla|Representacion|Letrero|Kenia|Ultra-Trail|Parroquia|Capilla|Grutas de Garc.a [0-9]|El Teatro", re.I)
sierra = [f for f in F.get("santiago",[]) if "Sierre" in f["titulo"]]
seen = set(); out = []
for c in d:
    if c["id"] in seen: continue
    seen.add(c["id"])
    c["zona"] = ZONA.get(c["zona"], c["zona"])
    fotos = [f for f in F.get(FOTO.get(c["zona"], ""), []) if not MALAS.search(f["titulo"])]
    if c["zona"] in ("Potrero Redondo","Las Adjuntas"): fotos = [f for f in fotos if "Chipit" in f["titulo"] or "Adj" in f["titulo"]]
    c["fotos"] = [dict(f, zona=True) for f in (fotos + sierra)][:5]
    assert -101 < c["lng"] < -99.5 and 24.5 < c["lat"] < 26.2, c["id"]
    out.append(c)
open("data.js","w",encoding="utf-8").write("window.CAMPINGS=" + json.dumps(out, ensure_ascii=False) + ";")
print(len(out), "campings:", ", ".join(c["id"] for c in out))
