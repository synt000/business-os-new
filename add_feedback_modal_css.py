from pathlib import Path

p = Path("src/templates/dashboard.html")

s = p.read_text()

marker = "/* FEEDBACK CENTER */"

css = '''

/* FEEDBACK MODAL */

.feedback-modal{

display:none;
position:fixed;
top:0;
left:0;
width:100%;
height:100%;
background:rgba(0,0,0,.65);
z-index:9999;
align-items:center;
justify-content:center;

}


.feedback-modal-card{

background:#111827;
width:90%;
max-width:420px;
padding:20px;
border-radius:20px;
border:1px solid #334155;

}


.feedback-modal-card h3{

color:#00e5ff;
margin-bottom:15px;

}


.feedback-input{

width:100%;
padding:12px;
margin-bottom:12px;
border-radius:12px;
border:1px solid #334155;
background:#0f172a;
color:white;

}


.feedback-submit{

width:100%;
padding:12px;
border:none;
border-radius:12px;
background:#2563eb;
color:white;
cursor:pointer;

}


.feedback-close{

margin-top:10px;
text-align:center;
color:#94a3b8;
cursor:pointer;

}

'''

if "FEEDBACK MODAL" not in s:
    s=s.replace(marker, css+marker,1)
    p.write_text(s)
    print("✅ feedback modal CSS added")
else:
    print("⚠️ already exists")
