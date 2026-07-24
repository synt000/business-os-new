from pathlib import Path

p = Path("src/static/js/dashboard_api.js")
s = p.read_text()

old = '''                                        pointRadius:5,
                                        pointHoverRadius:8
                                    },'''

new = '''                                        pointRadius:5,
                                        pointHoverRadius:8,

                                        datalabels:{
                                            display:true,
                                            color:"#ffffff",
                                            anchor:"end",
                                            align:"top",
                                            font:{
                                                size:12,
                                                weight:"bold"
                                            },
                                            formatter:function(value){
                                                return Number(value).toLocaleString()+" MMK";
                                            }
                                        }
                                    },'''

if old in s:
    s=s.replace(old,new,1)
    p.write_text(s)
    print("✅ Revenue value labels added")
else:
    print("❌ revenue block not found")
