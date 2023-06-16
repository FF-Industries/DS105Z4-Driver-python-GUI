from ds1054z import DS1054Z

scope = DS1054Z('169.254.1.5')
print("Connected to: ", scope.idn)

print("Currently displayed channels: ", str(scope.displayed_channels))
scope.write("*IDN?\n")
dbytes = scope.read()
print(dbytes)

scope.write( ":STOP\n")
scope.write( ":WAV:MODE RAW\n")
scope.write( ":WAV:FORM BYTE\n")
scope.write( ":WAV:SOUR CHAN1 \n")
scope.run()
float(scope.query(":ACQuire:SRATe?"))
scope.query(":ACQuire:SRATe?")