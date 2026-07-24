from pathlib import Path

p = Path("src/static/js/dashboard_api.js")
s = p.read_text()

old = '''datasets:[
                        {
                            label:"Revenue",
                            data:
                                d.sales_chart.values,

                            borderWidth:3,

                            tension:0.4
                        }
                    ]'''

new = '''datasets:[
                        {
                            label:"Revenue (MMK)",
                            data:
                                d.sales_chart.revenue,

                            borderWidth:3,

                            tension:0.4,

                            fill:true
                        },
                        {
                            label:"Orders",
                            data:
                                d.sales_chart.orders,

                            borderWidth:2,

                            tension:0.4
                        }
                    ]'''

if old in s:
    s=s.replace(old,new,1)
    p.write_text(s)
    print("✅ Dual line chart enabled")
else:
    print("❌ chart dataset block not found")
