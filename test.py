import dronekit_sitl

sitl = dronekit_sitl.start_default()
connection_string = sitl.connection_string()

print(connection_string)
while True:
    text = input()
    if text == "exit()":
        break
    pass

sitl.stop()
print("exit ...")