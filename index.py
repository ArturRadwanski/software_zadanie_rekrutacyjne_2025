from nicegui import ui, app
from communication_library.communication_manager import CommunicationManager, TransportType
from communication_library.tcp_transport import TcpSettings
from communication_library.frame import Frame
from communication_library import ids
from communication_library.exceptions import TransportTimeoutError, TransportError, UnregisteredCallbackError
import setup_frames
import asyncio
import time


epsilon = 1e-10
cm = CommunicationManager()


#global movement data

last_altitude = 0
last_time = 0
velocity = 0
running = False


#global controls collection
controls:dict[ui.button] = {}
tables:dict[ui.tab_panel] = {}



#global data
sensors_data = {
    "State": "IDLE",
    "Fuel Level": "0.0%",
    "Oxidizer Level": "0.0%",
    "Oxidizer Pressure": "0.0 bar",
    "Altitude": "0.0 m",
    "Velocity": "0.00 m/s"
}

servo_data = {
    "fuel_intake": "100",
    "oxidizer_intake": "100",
    "fuel_main": "100",
    "oxidizer_main": "100",
}

relays_data = {
    "oxidizer_heater": "CLOSED",
    "igniter": "CLOSED",
    "parachute": "CLOSED",
}

def root():
    ui.sub_pages({
        '/': main_page,
    }).classes('w-full')


#callback
#if fuel tank is full, close the intake and let user press start button
def wait_for_fuel(frame: Frame):
    fuel_level_update(frame)
    if 100 - frame.payload[0] < epsilon: #float inaccuracy
        
        cm.push(setup_frames.fuel_intake_close_frame)
        cm.send()
        sensors_data["State"] = "FUEL FILLED"
        controls["start_btn"].enable()
        cm.clear_callbacks()
        servo_data["fuel_intake"] = "100"

#callback
#if oxidizer tank is full, close the intake and start filling fuel tank
def wait_for_oxidizer(frame: Frame):
    oxidizer_level_update(frame)
    if 100 - frame.payload[0] < epsilon:
        cm.push(setup_frames.oxidizer_intake_close_frame)
        cm.send()
        sensors_data["State"] = "FILLING FUEL"
        
        cm.push(setup_frames.fuel_intake_open_frame)
        cm.send()

        cm.clear_callbacks()
        cm.register_callback(wait_for_fuel, setup_frames.fuel_frame)
        cm.register_callback(oxidizer_pressure_update, setup_frames.oxidizer_pressure_frame)

        
        servo_data["oxidizer_intake"] = "100"
        servo_data["fuel_intake"] = "0"
        

#handle Fuel button on_click event
#fill the oxidizer tank, then forward to fuel via callback
def fuel_action():
        
    controls["fuel_btn"].disable()
    sensors_data["State"] = "FILLING OXIDIZER"
    cm.push(setup_frames.oxidizer_intake_open_frame)
    cm.send()
        
        
    cm.register_callback(wait_for_oxidizer,setup_frames.oxidizer_frame)
    cm.register_callback(oxidizer_pressure_update, setup_frames.oxidizer_pressure_frame)
    servo_data["oxidizer_intake"] = "0"
        
#callback monitoring height, calculating velocity and deploying parachute accordingly
def parachute(frame: Frame):
    altitude_update(frame)
    global last_altitude, running
    
    if last_altitude > 10:
        running = True
    
    if velocity < 1 and running:
        cm.push(setup_frames.parachute_open_frame)
        cm.send()
        relays_data["parachute"] = "OPEN"
        sensors_data["State"] = "PARACHUTE_DEPLOYED"
    

#close oxidizer heater and handle the procedure
def ignition():
    cm.register_callback(parachute, setup_frames.altitude_frame)

    cm.push(setup_frames.oxidizer_heater__close_frame)
    cm.push(setup_frames.open_fuel_main_frame)
    cm.push(setup_frames.open_oxidizer_main_frame)
    cm.push(setup_frames.open_igniter_frame)
    
    cm.send()
    cm.send()
    cm.send()
    cm.send()

    relays_data["oxidizer_heater"] = "CLOSED"
    relays_data["igniter"] = "OPEN"
    servo_data["fuel_main"] = "0"
    servo_data["oxidizer_main"] = "0"
    sensors_data["State"] = "FLIGHT"


#callback
#start ignition procedure when oxidizer pressure is optimal
def wait_for_pressure(frame: Frame):
    oxidizer_pressure_update(frame)
    if frame.payload[0] > 55:
        cm.clear_callbacks()
        ignition()


#handle Start button:
#immidietky disable star button, start heating of oxidizer and register callback for oxidizer pressure
def start_rocket():
    controls["start_btn"].disable()
    cm.push(setup_frames.oxidizer_heater_open_frame)
    cm.send()
    cm.clear_callbacks()
    cm.register_callback(wait_for_pressure, setup_frames.oxidizer_pressure_frame)
    relays_data["oxidizer_heater"] = "OPEN"

#function generates the main page
def main_page():
    #add 3 tabs for 3 different tables
    with ui.tabs() as tabs:
        sensors = ui.tab('sensors')
        servos = ui.tab('servos')
        relays = ui.tab('relays')

    #generate tables
    with ui.tab_panels(tabs, value=sensors):
        with ui.tab_panel(sensors):
            tables["sensors"] = ui.table(rows=[
                {"parameter": data, "value": sensors_data[data]} for data in sensors_data 
            ])  

        with ui.tab_panel(servos):
           tables["servo"] = ui.table(rows=[
                {"parameter": data, "value": servo_data[data]} for data in servo_data 
            ])

        with ui.tab_panel(relays):
           tables["relays"] = ui.table(rows=[
                {"parameter": data, "value": relays_data[data]} for data in relays_data
            ])

    #synchronise tables with dictionary data
    async def update_table():
        while True:
            for i, key in enumerate(sensors_data):
                tables["sensors"].rows[i]["value"] = sensors_data[key]
            tables["sensors"].update()  

            for i, key in enumerate(servo_data):
                tables["servo"].rows[i]["value"] = servo_data[key]
            tables["servo"].update()  

            for i, key in enumerate(relays_data):
                tables["relays"].rows[i]["value"] = relays_data[key]
            tables["relays"].update() 

            #give control to main program loop
            await asyncio.sleep(1)

    asyncio.create_task(update_table())



    
    with ui.button_group():
        controls["fuel_btn"] = ui.button('Fuel').on_click(fuel_action)
        controls["start_btn"] = ui.button("Start").on_click(start_rocket)

    controls["start_btn"].disable()




#Listening for messages from server
async def wait_for_response():
    while True:
        try:
            cm.receive()
        except TransportTimeoutError:
                pass
        except UnregisteredCallbackError:
                pass
        #give control back to the main loop    
        await asyncio.sleep(0)



#Callbacks for data updates
def fuel_level_update(frame: Frame):
    sensors_data["Fuel Level"] = "{:.2f}%".format(frame.payload[0])


def oxidizer_level_update(frame: Frame):
    sensors_data["Oxidizer Level"] = "{:.2f}%".format(frame.payload[0])
    

def oxidizer_pressure_update(frame: Frame):
    sensors_data["Oxidizer Pressure"] = "{:.2f} bar".format(frame.payload[0])
    

def altitude_update(frame: Frame):
    sensors_data["Altitude"] = "{:.2f} m".format(frame.payload[0])
    cur_altitude = frame.payload[0]
    cur_time = time.time()
    global last_altitude, last_time, velocity

    delta_a = cur_altitude - last_altitude
    delta_t = cur_time - last_time
    velocity = delta_a / delta_t

    last_altitude = cur_altitude
    last_time = cur_time

    sensors_data["Velocity"] = "{:.2f} m/s".format(velocity) 
    
    

@app.on_startup
async def on_starup():
    asyncio.create_task(wait_for_response())

if __name__ in {"__main__", "__mp_main__"}:
   

    cm.change_transport_type(TransportType.TCP)
    cm.connect(TcpSettings("127.0.0.1", 3000))

    ui.run(root)
