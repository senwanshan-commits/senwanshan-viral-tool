import json
import os
import re

import uvicorn
from fastapi import Body, FastAPI
from fastapi.responses import HTMLResponse
from openai import OpenAI


app = FastAPI(title="Senwanshan AI Short Video Tool")

API_KEY = os.getenv("API_KEY", "")
BASE_URL = os.getenv("BASE_URL", "https://api.deepseek.com")
MODEL = os.getenv("MODEL", "deepseek-chat")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.8"))

SYSTEM_PROMPT = """
You are a Douyin short-video viral content strategist.
Always write in Simplified Chinese.
Optimize for the first 5 seconds completion rate, comments, saves, shares, emotion, and practical value.
Use one main emotion from: xue mai jue xing, yi chu ji feng, duo ba an shuang gan, da po lv jing, chao jue song chi gan, huan xing zi yu, chong su nei he, huai jiu meng he.
Use natural emotion words, identity words, pain-point words, and value words. Do not make the writing stiff.
Return valid JSON only.
"""


def call_model(task, payload, schema):
    if not API_KEY:
        return {
            "error": "API_KEY is missing. Add your DeepSeek key in Render Environment Variables."
        }
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    user_prompt = (
        f"Task: {task}\n\nInput:\n"
        f"{json.dumps(payload, ensure_ascii=False)}\n\n"
        f"Return JSON with this shape:\n{schema}"
    )
    try:
        result = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=TEMPERATURE,
            max_tokens=4096,
        )
        return parse_json(result.choices[0].message.content or "")
    except Exception as exc:
        return {"error": str(exc)}


def parse_json(text):
    text = re.sub(r"```(?:json)?", "", text).replace("```", "").strip()
    for left, right in [("[", "]"), ("{", "}")]:
        start = text.find(left)
        end = text.rfind(right)
        if start >= 0 and end > start:
            try:
                return json.loads(text[start : end + 1])
            except Exception:
                pass
    return {"content": text}


@app.get("/")
async def home():
    return HTMLResponse(HTML)


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "model": MODEL,
        "base_url": BASE_URL,
        "api_key_configured": bool(API_KEY),
    }


@app.post("/api/generate/viral-topic")
async def viral_topic(data: dict = Body(default={})):
    schema = """
[
 {"title":"", "score":"8-10", "emotional_type":"", "hook":"", "reason":"", "script_brief":"", "viral_rating":{"five_second_completion":9,"comment_desire":9,"save_value":9,"emotion_resonance":9}, "comment_hook":"", "angle":""}
]
"""
    return {"success": True, "content": call_model("Generate 5 viral Douyin topic ideas.", data, schema)}


@app.post("/api/generate/monetization-topic")
async def monetization_topic(data: dict = Body(default={})):
    schema = """
[
 {"title":"", "score":"8-10", "purchase_driver":"", "emotional_type":"", "script_brief":"", "angle":"", "call_to_action":""}
]
"""
    return {"success": True, "content": call_model("Generate 5 high-conversion short-video ideas.", data, schema)}


@app.post("/api/generate/script")
async def script(data: dict = Body(default={})):
    schema = """
{"title":"","main_emotion":"","duration":"","hook":"","structure":[{"role":"","time":"","content":"","visual":"","behavior_target":"","emotion_words":"","mindset_words":""}],"closing":"","tips":[],"comment_hook":""}
"""
    return {"success": True, "content": call_model("Write a complete Douyin video script.", data, schema)}


@app.post("/api/generate/copy-rewrite")
async def copy_rewrite(data: dict = Body(default={})):
    schema = """
[
 {"title":"", "angle":"", "main_emotion":"", "content":"", "emotion_words":[], "mindset_words":[], "comment_hook":""}
]
"""
    return {"success": True, "content": call_model("Rewrite the copy into 3 viral versions.", data, schema)}


@app.post("/api/generate/video-analysis")
async def video_analysis(data: dict = Body(default={})):
    schema = """
{"summary":"","viral_points":[],"emotion_strategy":"","weaknesses":[],"rewrite_hook":"","rewrite_direction":"","comment_hook":""}
"""
    return {"success": True, "content": call_model("Analyze and improve a viral video idea.", data, schema)}


HTML = """
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Senwanshan AI Short Video Tool</title>
<style>
body{margin:0;font-family:Arial,sans-serif;background:#f4f7fb;color:#172033}
header{background:#0b1220;color:white;padding:20px 26px}
h1{margin:0;font-size:22px}header p{margin:6px 0 0;color:#cbd5e1}
main{display:grid;grid-template-columns:260px 1fr;min-height:calc(100vh - 84px)}
nav{background:#fff;border-right:1px solid #d8e0ec;padding:16px}
nav button{display:block;width:100%;margin:0 0 8px;padding:11px;border:1px solid transparent;border-radius:6px;background:white;text-align:left;cursor:pointer}
nav button.active{background:#ecfdf5;border-color:#99f6e4;color:#0f766e;font-weight:700}
.work{display:grid;grid-template-columns:430px 1fr;gap:18px;padding:20px}
section{background:white;border:1px solid #d8e0ec;border-radius:8px;padding:16px}
label{display:block;margin:12px 0 6px;color:#667085;font-size:13px}
input,textarea{width:100%;border:1px solid #d8e0ec;border-radius:6px;padding:10px;font-size:14px}
textarea{min-height:120px}
.go{margin-top:14px;background:#0f766e;color:white;border:0;border-radius:6px;padding:10px 14px;font-weight:700;cursor:pointer}
.item{border:1px solid #d8e0ec;border-radius:8px;margin:0 0 12px;padding:12px;background:#fff}
pre{white-space:pre-wrap;word-break:break-word;background:#0b1220;color:#e5e7eb;padding:12px;border-radius:6px}
.empty{background:#fff7ed;border:1px solid #fed7aa;border-radius:6px;padding:12px;color:#667085}
@media(max-width:900px){main,.work{grid-template-columns:1fr}nav{border-right:0;border-bottom:1px solid #d8e0ec}}
</style>
</head>
<body>
<header><h1>Senwanshan AI Short Video Tool</h1><p>Viral topics, monetization topics, scripts, rewrites, and video analysis.</p></header>
<main>
<nav id="tabs"></nav>
<div class="work"><section><h2 id="title"></h2><div id="form"></div></section><section><h2>Result</h2><div id="result" class="empty">Fill the form and generate.</div></section></div>
</main>
<script>
const tabs={
 viral:["Viral Topics","/api/generate/viral-topic",[["industry","Industry / persona"],["main_type","Main script type"],["sub_type","Sub type"],["elements","Viral elements, comma separated"]]],
 money:["Monetization","/api/generate/monetization-topic",[["industry","Industry / offer"],["main_type","Main script type"],["sub_type","Conversion direction"],["elements","Purchase reasons, comma separated"]]],
 script:["Script","/api/generate/script",[["topic","Topic"],["industry","Industry / persona"],["requirements","Requirements"]]],
 rewrite:["Rewrite","/api/generate/copy-rewrite",[["text","Original copy"],["style","Rewrite direction"]]],
 analysis:["Analysis","/api/generate/video-analysis",[["url","Video URL"],["description","Description"]]]
};
let current="viral";
function esc(s){return String(s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]))}
function drawTabs(){tabsEl.innerHTML=Object.entries(tabs).map(([k,v])=>`<button class="${k===current?'active':''}" onclick="current='${k}';drawTabs();drawForm();">${v[0]}</button>`).join("")}
function drawForm(){let t=tabs[current];title.textContent=t[0];form.innerHTML=t[2].map(([k,l])=>`<label>${l}</label><textarea id="${k}" placeholder="${l}"></textarea>`).join("")+`<button class="go" onclick="go()">Generate</button>`}
async function go(){result.className="empty";result.textContent="Generating...";let t=tabs[current],data={};for(let [k] of t[2]){let v=document.getElementById(k).value.trim();data[k]=k==="elements"?v.split(/[,\\uFF0C]/).map(x=>x.trim()).filter(Boolean):v}try{let r=await fetch(t[1],{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(data)});let j=await r.json();show(j.content||j)}catch(e){result.textContent=e.message}}
function show(x){result.className="";if(Array.isArray(x)){result.innerHTML=x.map((it,i)=>`<div class="item"><b>${esc(it.title||('Result '+(i+1)))}</b><pre>${esc(JSON.stringify(it,null,2))}</pre></div>`).join("");return}result.innerHTML=`<div class="item"><pre>${esc(JSON.stringify(x,null,2))}</pre></div>`}
const tabsEl=document.getElementById("tabs");drawTabs();drawForm();
</script>
</body>
</html>
"""


if __name__ == "__main__":
    port = int(os.getenv("PORT", "9100"))
    uvicorn.run(app, host="0.0.0.0", port=port)
