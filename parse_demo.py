from demoparser.demofile import DemoFile

def parse_table(table):
    print(table)

def change_cb(entity, table_name, var_name, value):
    print(entity)
    print(table_name)
    print(var_name)
    print(value)

def game_event_cb(event, msg):
    print(event)
    print(msg)

data = open('demos/astralis-vs-liquid-m1-inferno.dem', 'rb').read()
df = DemoFile(data)
#df.add_callback('datatable_ready', parse_table)
#df.add_callback('change', change_cb)
#df.add_callback('player_footstep', game_event_cb)
df.parse()
