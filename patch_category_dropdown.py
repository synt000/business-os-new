from pathlib import Path

p = Path("src/templates/products.html")
text = p.read_text()

old = '''<label class="block text-xs font-semibold text-gray-400 mb-1.5 uppercase tracking-wide">Category ID</label>
                                <input type="text" id="category_id" required placeholder="UUID string" class="w-full px-3 py-2 bg-gray-900/60 border border-gray-800 rounded-xl text-sm text-white focus:outline-none focus:border-blue-500">'''

new = '''<label class="block text-xs font-semibold text-gray-400 mb-1.5 uppercase tracking-wide">Category</label>
                                <select id="category_id" class="w-full px-3 py-2 bg-gray-900/60 border border-gray-800 rounded-xl text-sm text-white focus:outline-none focus:border-blue-500">
                                    <option value="">Loading categories...</option>
                                </select>'''

text = text.replace(old, new)

p.write_text(text)

print("CATEGORY DROPDOWN PATCHED")
