# Une data.json + fotos.json -> data.js (lo que carga index.html)
import json, re
d = json.load(open("data.json", encoding="utf-8"))
F = json.load(open("fotos.json", encoding="utf-8"))
d += [
 {"id":"parque-la-huasteca","nombre":"Parque Ecológico La Huasteca","municipio":"Santa Catarina","zona":"La Huasteca","lat":25.6505,"lng":-100.4595,"coords_aprox":True,
  "tipo":"parque público","precio":"Hay cuota de entrada desde 2025 (monto no publicado). Acampar se permite en temporadas y eventos que anuncia el municipio.","precio_min_mxn":None,
  "capacidad":"Zona de camping abierta; en eventos organizados (cine o astronomía) el cupo lo pone el organizador.",
  "reglas":["Acampar solo en temporadas o eventos autorizados por el municipio (ej. Semana Santa 2025)","Pagar la cuota de acceso del parque","Llevarse la basura","Revisar avisos de Protección Civil por lluvias y crecidas del río"],
  "servicios":["Asadores y mesas (en eventos)","Baños y vestidores (en eventos)","Estacionamiento","Senderismo, rapel y ciclismo de montaña"],
  "resenas":[],"rating":None,"contacto":"Municipio de Santa Catarina","confianza":"baja",
  "fuente_urls":["https://www.posta.com.mx/nuevo-leon/jesus-nava-anuncia-apertura-de-atractivos-turisticos-de-santa-catarina/v-vl2023158","https://www.posta.com.mx/nuevo-leon/victor-perez-cuestiona-tarifa-en-la-huasteca-pide-acceso-libre-y-servicios/vl2056170","https://monterreysecreto.com/movies-camping-huasteca/"],
  "nota":"La apertura para acampar cambia según la temporada. Confirma con el municipio antes de ir.","_foto":"huasteca2"},
 {"id":"cola-de-caballo","nombre":"Cascada Cola de Caballo","municipio":"Santiago","zona":"Cola de Caballo","lat":25.3636,"lng":-100.1607,"coords_aprox":False,
  "tipo":"punto de referencia","precio":"Entrada al parque de la cascada: $50 adulto, menores de 4 años gratis. Dentro del parque no se acampa.","precio_min_mxn":None,
  "capacidad":"Parque de día, sin zona de camping.",
  "reglas":["No se acampa dentro del parque de la cascada","Para pasar la noche, los campings más cercanos están subiendo por la carretera a Laguna de Sánchez y Ciénega de González"],
  "servicios":["Senderos a la cascada","Paseos a caballo","Comida en la entrada"],
  "resenas":[],"rating":None,"contacto":"","confianza":"media",
  "fuente_urls":["https://www.posta.com.mx/nuevo-leon/rutas-costos-y-todo-para-escaparte-a-la-cola-de-caballo/vl2167752"],
  "nota":"Es la puerta de entrada a la sierra de Santiago. Los campings de Ciénega de González y Laguna de Sánchez quedan a 30–60 min.","_foto":"cola-de-caballo"},
]
ZONA = {"Hidalgo (El Potrero Chico)":"Potrero Chico","Cumbres de Monterrey (sur de Monterrey)":"Monterrey",
        "Las Adjuntas / San José de las Boquillas":"Las Adjuntas","Galeana (Cerro del Potosí)":"Galeana"}
FOTO = {"Laguna de Sánchez":"laguna-sanchez","Potrero Chico":"potrero-chico","Monterrey":"chipinque2","Ciénega de González":"cienega",
        "Potrero Redondo":"matacanes","Las Adjuntas":"matacanes","Presa La Boca":"presa2","Allende":"allende","Iturbide":"iturbide"}
MALAS = re.compile(r"Castillo|Murallas|Tobaruela|SanFelices|Agave|Chaparro|Thymophylla|Representacion|Letrero|Kenia|Ultra-Trail", re.I)
for c in d:
    c["zona"] = ZONA.get(c["zona"], c["zona"])
    k = c.pop("_foto", None) or FOTO.get(c["zona"])
    fotos = [dict(f, zona=True) for f in F.get(k, []) if not MALAS.search(f["titulo"])]
    if c["zona"] == "Potrero Redondo": fotos = [f for f in fotos if "Chipit" in f["titulo"]] + [f for f in F.get("santiago",[]) if "Sierre" in f["titulo"]]
    if c["zona"] == "Las Adjuntas": fotos = [dict(f,zona=True) for f in F["matacanes"] if "Adj" in f["titulo"]]
    if c["zona"] == "Monterrey": fotos += [dict(f,zona=True) for f in F.get("santiago",[]) if "Sierre" in f["titulo"]]
    c["fotos"] = fotos[:5]
    assert -101 < c["lng"] < -99.5 and 24.5 < c["lat"] < 26.2, c["id"]  # dentro de N.L. centro/sur
ids = [c["id"] for c in d]; assert len(ids) == len(set(ids))
open("data.js","w",encoding="utf-8").write("window.CAMPINGS=" + json.dumps(d, ensure_ascii=False) + ";")
print(len(d), "lugares;", sum(1 for c in d if c["fotos"]), "con fotos")
