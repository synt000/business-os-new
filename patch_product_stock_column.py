from pathlib import Path

p = Path("src/templates/products.html")
text = p.read_text()

text = text.replace(
'<th class="pb-3 font-medium text-right">Unit Price</th>',
'<th class="pb-3 font-medium text-right">Unit Price</th>\n'
'<th class="pb-3 font-medium text-center">Stock</th>'
)

text = text.replace(
'<td class="py-3 text-right font-semibold">$${parseFloat(p.retail_price).toFixed(2)}</td>\n'
'                                <td class="py-3 text-center"><span class="px-2 py-0.5 rounded-md bg-blue-500/10 text-blue-400 text-[10px] font-semibold border border-blue-500/10">Active</span></td>',
'<td class="py-3 text-right font-semibold">$${parseFloat(p.retail_price).toFixed(2)}</td>\n'
'<td class="py-3 text-center">${p.stock_qty}</td>\n'
'<td class="py-3 text-center"><span class="px-2 py-0.5 rounded-md bg-blue-500/10 text-blue-400 text-[10px] font-semibold border border-blue-500/10">Active</span></td>'
)

text = text.replace('colspan="4"', 'colspan="5"')

p.write_text(text)

print("STOCK COLUMN ADDED")
