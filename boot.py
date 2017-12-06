# This file is executed on every boot (including wake-boot from deepsleep)
# import esp
# esp.osdebug(None)
import gc
# import webrepl
# webrepl.start()


def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    network.WLAN(network.AP_IF).active(0)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)

        sta_if.connect('Bigdoghouse', '123456')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())


gc.collect()
do_connect()