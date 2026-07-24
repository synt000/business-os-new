from pathlib import Path

p = Path("src/static/js/dashboard_api.js")
s = p.read_text()

old = '''                                        tension:0.45,
                                        pointRadius:4,
                                        pointHoverRadius:7
                                    }
'''

new = '''                                        tension:0.45,
                                        pointRadius:4,
                                        pointHoverRadius:7,

                                        datalabels:{
                                            display:true,
                                            color:"#ffcc00",
                                            anchor:"end",
                                            align:"bottom",
                                            font:{
                                                size:11,
                                                weight:"bold"
                                            },
                                            formatter:function(value){
                                                return value + " Orders";
                                            }
                                        }
                                    }
'''

if old in s:
    s=s.replace(old,new,1)
    p.write_text(s)
    print("✅ Orders labels added")
else:
    print("❌ Orders block not found")
