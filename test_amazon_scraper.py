from amzsear import AmzSear
amz = AmzSear('Harry Potter', page=1, region='US')
ast_item = amz.rget(-1)
print(ast_item)