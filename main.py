import jsonc

print(jsonc.__doc__)


Data = '''{
   "name": "Harry",
   // defines name
   "name2": "test",
   "data": {
      "item_1": [0,1,2,3]
   },
   /* line 4
   line 5
   line 6*/
   "test": "awdw" // test
}'''

aaaa = jsonc.loads(Data)
data = jsonc.dumps(aaaa)


print(data)
