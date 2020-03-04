import SVG

svg = SVG.SVG(200)

svg.parse('svg/' + input("SVG Input: "))
svg.export('mstp/' + input("MSTP Output: "))
