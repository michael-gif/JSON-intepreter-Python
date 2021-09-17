def format_json(in_json):
    out_json = ''.join(a.strip() for a in in_json.split('\n'))
    return out_json

def parse_array(raw):
    raw_array = raw[1:-1]
    array_parts = []
    x = 0
    object_count = 0
    found_object = False
    while True:
        if raw_array[x] == '{':
            object_count += 1
            found_object = True
        elif raw_array[x] == ',':
            flag = False
            if raw_array[0] != '{':
                if raw_array[x - 1] == '"' and raw_array[x - 1] != '\\':
                    flag = True
                if raw_array[x - 1] == 'e':
                    flag = True
                try:
                    num = int(raw_array[x - 1])
                    flag = True
                except:
                    pass
            else:
                if raw_array[x - 1] == '}':
                    object_count -= 1
                    if found_object and not object_count:
                        flag = True
                        found_object = False
            if flag:
                array_parts.append(raw_array[:x].strip())
                raw_array = raw_array[x + 1:]
                x = -1
        x += 1
        if x == len(raw_array):
            array_parts.append(raw_array[:x].strip())
            break
                
    return array_parts

def parse_object(raw):
    json_object = raw.strip()

    # separate the pairs
    start_index, end_index = 0, 0
    parts = []
    pairs_string = json_object[1:-1]
    x = 0
    while True:
        if pairs_string[x] == ',':
            temp = pairs_string[x + 1:].lstrip()
            if temp[0] == '"':
                parts.append(pairs_string[:x])
                pairs_string = pairs_string.replace(pairs_string[:x + 1], '')
                x = -1
        x += 1
        if x == len(pairs_string):
            parts.append(pairs_string)
            break
    
    # separate the keys and values
    final_json = {}
    for part in parts:
        x = part.index(':')
        key = part[:x].rstrip()
        if key[-1] == '"' and key[-2] != '\\':
            key = key[1:-1]
            value = part[x+1:].lstrip()
            final_json[key] = value
                    
    return final_json

def parse_string(raw):
    string_json = None
    if raw[0] == '"' == raw[-1]:
        string_json = raw[1:-1]
    return string_json

def parse_int(raw):
    try:
        return int(raw)
    except:
        return None

def parse_float(raw):
    try:
        return float(raw)
    except:
        return None

def parse_boolean(raw):
    string_json = None
    if raw == 'true':
        string_json = True
    elif raw == 'false':
        string_json = False
    return string_json

def read(raw):
    result = None
    if raw[0] == '[' and raw[-1] == ']':
        result = parse_array(raw)
        for x in range(len(result)):
            part = result[x]
            if part[0] == '"' == part[-1]:
                result[x] = part[1:-1]
            elif part[0] == '{' and part[-1] == '}':
                result[x] = read(part)
            elif part == 'true':
                result[x] = True
            elif part == 'false':
                result[x] = False
            try:
                result[x] = int(part)
                continue
            except:
                pass
            try:
                result[x] = float(part)
            except:
                pass
    elif raw[0] == '{' and raw[-1] == '}':
        json_object = parse_object(raw)
        for key, value in json_object.items():
            new_value = parse_string(value)
            if new_value == None:
                new_value = parse_boolean(value)
            if new_value == None:
                new_value = parse_int(value)
            if new_value == None:
                new_value = parse_float(value)
            if new_value != None:
                json_object[key] = new_value
            else:
                json_object[key] = read(value)
        result = json_object
    return result

json = '''
[{
  "_id": "61421a3a7cd82c8af9eb1d36",
  "index": [1, 2, 3.0, 4, 5],
  "guid": "0987ac36-3860-4e27-a5c0-aabd7035581c",
  "isActive": true,
  "balance": "$3,279.79",
  "picture": "http://placehold.it/32x32",
  "age": 30,
  "eyeColor": "blue",
  "name": "Stacey Flores",
  "gender": "female",
  "company": "KENGEN",
  "email": "staceyflores@kengen.com",
  "phone": "+1 (857) 568-3836",
  "address": "974 Scholes Street, Chase, Maryland, 4325",
  "about": "In fugiat dolor pariatur officia magna. In aliquip labore non deserunt reprehenderit velit magna cupidatat cupidatat proident tempor cillum duis nulla. Excepteur nulla dolor ea adipisicing eiusmod sit magna et Lorem ad irure.\r\n",
  "registered": "2021-06-28T10:59:16 -01:00",
  "latitude": 38.506646,
  "longitude": -74.445677
},
{
  "_id": "asdfasdf",
  "index": 456+,
  "guid": "0987ac36-3abd7035581c",
  "isActive": false,
  "balance": "$3,279.79",
  "picture": "http://placehold.it/32x32",
  "age": 30,
  "eyeColor": "blue",
  "name": "Stacey Flores",
  "gender": "female",
  "company": "KENGEN",
  "email": "staceyflores@kengen.com",
  "phone": "+1 (857) 568-3836",
  "address": "974 Scholes Street, Chase, Maryland, 4325",
  "about": "In fugiat dolor pariatur officia magna. In aliquip labore non deserunt reprehenderit velit magna cupidatat cupidatat proident tempor cillum duis nulla. Excepteur nulla dolor ea adipisicing eiusmod sit magna et Lorem ad irure.\r\n",
  "registered": "2021-06-28T10:59:16 -01:00",
  "latitude": 38.506646,
  "longitude": -74.445677
},
true,
"fatass"
]
'''

if __name__ == '__main__':
    print(read(format_json(json)))
