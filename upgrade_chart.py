from pathlib import Path

p = Path("src/static/js/dashboard_api.js")
s = p.read_text()

old = '''new Chart(
            ctx,
            {
                type:"line",

                data:{
                    labels:
                        d.sales_chart.labels,

                    datasets:[
                        {
                            label:"Revenue",

                            data:
                                d.sales_chart.values,

                            borderWidth:3,

                            tension:0.4
                        }
                    ]
                },

                options:{
                    responsive:true,

                    plugins:{
                        legend:{
                            display:true
                        }
                    }
                }
            }
        );'''

new = '''const gradient = ctx.getContext("2d").createLinearGradient(
            0,0,0,300
        );

        gradient.addColorStop(0,"rgba(0,229,255,0.45)");
        gradient.addColorStop(1,"rgba(0,229,255,0.02)");

        new Chart(
            ctx,
            {
                type:"line",

                data:{
                    labels:d.sales_chart.labels,

                    datasets:[
                        {
                            label:"Revenue (MMK)",
                            data:d.sales_chart.values,

                            borderWidth:3,
                            borderColor:"#00e5ff",

                            backgroundColor:gradient,

                            fill:true,
                            tension:0.45,

                            pointRadius:5,
                            pointHoverRadius:8
                        }
                    ]
                },

                options:{
                    responsive:true,
                    maintainAspectRatio:false,

                    animation:{
                        duration:1200
                    },

                    plugins:{
                        legend:{
                            display:true
                        },

                        tooltip:{
                            callbacks:{
                                label:function(context){
                                    return Number(
                                        context.raw || 0
                                    ).toLocaleString()+" MMK";
                                }
                            }
                        }
                    }
                }
            }
        );'''

if old in s:
    s=s.replace(old,new,1)
    p.write_text(s)
    print("✅ Premium chart upgraded")
else:
    print("❌ chart block not found")
