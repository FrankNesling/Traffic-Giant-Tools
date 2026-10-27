import frida

# Attach to the running game
session = frida.attach("trafficgiant.exe")

script = session.create_script(r"""
const game = Process.getModuleByName("trafficgiant.exe");

// Ghidra address 004D2AE8, relative to image base 00400000
const address = game.base.add(0xD2AE8);

console.log("Schwebebahn hook installed at " + address);

Interceptor.attach(address, function () {
    this.context.eax = this.context.eax.xor(8);
});
""")

script.on("message", lambda message, data: print(message))
script.load()

input("Hook active. Press Enter to detach.\n")
session.detach()
