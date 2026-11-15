import json, urllib.request, urllib.parse, re, sys
Q = {
 "cola-de-caballo": "Cola de Caballo Santiago Nuevo León",
 "huasteca": "Parque La Huasteca Santa Catarina",
 "chipinque": "Chipinque",
 "potrero-chico": "Potrero Chico Hidalgo",
 "laguna-sanchez": "Laguna de Sánchez",
 "presa-la-boca": "Presa Rodrigo Gómez La Boca",
 "santiago": "Santiago Nuevo León sierra",
 "garcia-grutas": "Grutas de García",
 "cienega": "Ciénega de González",
 "allende": "Allende Nuevo León",
 "cumbres": "Parque Nacional Cumbres de Monterrey",
 "el-cercado": "El Cercado Santiago Nuevo León",
 "matacanes": "Matacanes Nuevo León",
 "potrero-redondo": "Potrero Redondo Nuevo León",
 "iturbide": "Iturbide Nuevo León",
 "rayones": "Rayones Nuevo León",
 "montemorelos": "Montemorelos Nuevo León",
}
UA={"User-Agent":"campings-map/1.0 (personal project)"}
def get(params):
    u="https://commons.wikimedia.org/w/api.php?"+urllib.parse.urlencode(params)
    return json.load(urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=30))
out={}
for k,q in Q.items():
    try:
        r=get({"action":"query","format":"json","generator":"search","gsrsearch":q+" filetype:bitmap","gsrnamespace":6,"gsrlimit":8,
               "prop":"imageinfo","iiprop":"url|extmetadata|size","iiurlwidth":1100})
        pages=sorted(r.get("query",{}).get("pages",{}).values(), key=lambda p:p.get("index",99))
        fotos=[]
        for p in pages:
            ii=p["imageinfo"][0]
            if ii.get("width",0)<800: continue
            md=ii.get("extmetadata",{})
            strip=lambda s: re.sub("<[^>]+>","",s or "").strip()
            fotos.append({"src":ii["thumburl"],"pag":ii["descriptionurl"],"autor":strip(md.get("Artist",{}).get("value"))[:60],
                          "lic":md.get("LicenseShortName",{}).get("value",""),"titulo":p["title"][5:]})
        out[k]=fotos[:5]
        print(k,len(fotos), [f["titulo"][:40] for f in fotos[:5]])
    except Exception as e: print(k,"ERR",e)
json.dump(out,open(sys.argv[1],"w",encoding="utf-8"),ensure_ascii=False,indent=1)
