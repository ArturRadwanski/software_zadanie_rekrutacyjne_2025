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
last_altitude = 0
last_time = 0
velocity = 0
running = False


#global controls collection
controls:dict[ui.button] = {}
tables:dict[ui.tab_panel] = {}

cm = CommunicationManager()
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

def wait_for_fuel(frame: Frame):
    fuel_level_update(frame)
    if 100 - frame.payload[0] < epsilon: #float inaccuracy
        servo_close_frame = Frame(ids.BoardID.ROCKET, 
                           ids.PriorityID.LOW, 
                           ids.ActionID.SERVICE, 
                           ids.BoardID.SOFTWARE, 
                           ids.DeviceID.SERVO, 
                           0, # fuel intake 
                           ids.DataTypeID.INT16,
                           ids.OperationID.SERVO.value.POSITION,
                           (100,) # 0 is for open position, 100 is for closed
                           )
        cm.push(servo_close_frame)
        cm.send()
        sensors_data["State"] = "FUEL FILLED"
        controls["start_btn"].enable()
        cm.clear_callbacks()
        servo_data["fuel_intake"] = "100"

def wait_for_oxidizer(frame: Frame):
    oxidizer_level_update(frame)
    if 100 - frame.payload[0] < epsilon:
        servo_close_frame = Frame(ids.BoardID.ROCKET, 
                           ids.PriorityID.LOW, 
                           ids.ActionID.SERVICE, 
                           ids.BoardID.SOFTWARE, 
                           ids.DeviceID.SERVO, 
                           1, # oxidizer intake 
                           ids.DataTypeID.INT16,
                           ids.OperationID.SERVO.value.POSITION,
                           (100,) # 0 is for open position, 100 is for closed
                           )
        cm.push(servo_close_frame)
        cm.send()
        sensors_data["State"] = "FILLING FUEL"
        servo_open_frame = Frame(ids.BoardID.ROCKET, 
                           ids.PriorityID.LOW, 
                           ids.ActionID.SERVICE, 
                           ids.BoardID.SOFTWARE, 
                           ids.DeviceID.SERVO, 
                           0, # fuel intake 
                           ids.DataTypeID.INT16,
                           ids.OperationID.SERVO.value.POSITION,
                           (0,) # 0 is for open position, 100 is for closed
                           )
        cm.push(servo_open_frame)
        cm.send()

        cm.clear_callbacks()
        try:
            cm.register_callback(wait_for_fuel, setup_frames.fuel_frame)
            cm.register_callback(oxidizer_pressure_update, setup_frames.oxidizer_pressure_frame)
        except UnregisteredCallbackError as e:
            print(f"unregistered frame received: {e.frame}")
        except:
            pass
        
        servo_data["oxidizer_intake"] = "100"
        servo_data["fuel_intake"] = "0"
        

def fuel_action():
        
        print("xd")
        controls["fuel_btn"].disable()
        sensors_data["State"] = "FILLING OXIDIZER"
        servo_open_frame = Frame(ids.BoardID.ROCKET, 
                           ids.PriorityID.LOW, 
                           ids.ActionID.SERVICE, 
                           ids.BoardID.SOFTWARE, 
                           ids.DeviceID.SERVO, 
                           1, # oxidizer intake 
                           ids.DataTypeID.INT16,
                           ids.OperationID.SERVO.value.POSITION,
                           (0,) # 0 is for open position, 100 is for closed
                           )
        cm.push(servo_open_frame)
        cm.send()
        

        
        cm.register_callback(wait_for_oxidizer,setup_frames.oxidizer_frame)
        servo_data["oxidizer_intake"] = "0"
        
def parachute(frame: Frame):
    altitude_update(frame)
    global last_altitude, running
    parachute_open_frame = Frame(ids.BoardID.ROCKET, 
                           ids.PriorityID.LOW, 
                           ids.ActionID.SERVICE, 
                           ids.BoardID.SOFTWARE, 
                           ids.DeviceID.RELAY, 
                           2, # parachute
                           ids.DataTypeID.FLOAT,
                           ids.OperationID.RELAY.value.OPEN,
                           ()
                           )
    if last_altitude > 10:
        running = True
    
    if velocity < 1 and running:
        cm.push(parachute_open_frame)
        cm.send()
        relays_data["parachute"] = "OPEN"
        sensors_data["State"] = "PARACHUTE_DEPLOYED"
    

def ignition():
    relay_close_frame = Frame(ids.BoardID.ROCKET, 
                           ids.PriorityID.LOW, 
                           ids.ActionID.SERVICE, 
                           ids.BoardID.SOFTWARE, 
                           ids.DeviceID.RELAY, 
                           0, # oxidizer heater
                           ids.DataTypeID.FLOAT,
                           ids.OperationID.RELAY.value.CLOSE,
                           ()
                           )
    open_fuel = Frame(ids.BoardID.SOFTWARE, 
                           ids.PriorityID.LOW, 
                           ids.ActionID.FEED, 
                           ids.BoardID.ROCKET, 
                           ids.DeviceID.SERVO, 
                           2, # fuel main
                           ids.DataTypeID.INT16,
                           ids.OperationID.SERVO.value.POSITION,
                           (0,))
    

    open_oxidizer = Frame(ids.BoardID.SOFTWARE, 
                           ids.PriorityID.LOW, 
                           ids.ActionID.SERVICE, 
                           ids.BoardID.ROCKET, 
                           ids.DeviceID.SERVO, 
                           3, # fuel main
                           ids.DataTypeID.INT16,
                           ids.OperationID.SERVO.value.POSITION,
                           (0,))

    open_relay_igniter = Frame(ids.BoardID.SOFTWARE, 
                           ids.PriorityID.LOW, 
                           ids.ActionID.SERVICE, 
                           ids.BoardID.ROCKET, 
                           ids.DeviceID.RELAY, 
                           1, # igniter
                           ids.DataTypeID.FLOAT,
                           ids.OperationID.RELAY.value.OPEN)

    cm.register_callback(parachute, setup_frames.altitude_frame)
    
    relays_data

    cm.push(relay_close_frame)
    cm.push(open_fuel)
    cm.push(open_oxidizer)
    cm.push(open_relay_igniter)
    
    cm.send()
    cm.send()
    cm.send()
    cm.send()

    relays_data["oxidizer_heater"] = "CLOSED"
    relays_data["igniter"] = "OPEN"
    servo_data["fuel_main"] = "0"
    servo_data["oxidizer_main"] = "0"
    sensors_data["State"] = "FLIGHT"


def wait_for_pressure(frame: Frame):
    oxidizer_pressure_update(frame)
    if frame.payload[0] > 55:
        cm.clear_callbacks()
        ignition()
        #cm.register_callback(setup_frames.altitude_frame)

def start_rocket():
    controls["start_btn"].disable()
    relay_open_frame = Frame(ids.BoardID.ROCKET, 
                           ids.PriorityID.LOW, 
                           ids.ActionID.SERVICE, 
                           ids.BoardID.SOFTWARE, 
                           ids.DeviceID.RELAY, 
                           0, # oxidizer heater
                           ids.DataTypeID.FLOAT,
                           ids.OperationID.RELAY.value.OPEN,
                           ()
                           )
    cm.push(relay_open_frame)
    cm.send()
    cm.register_callback(wait_for_pressure, setup_frames.oxidizer_pressure_frame)
    relays_data["oxidizer_heater"] = "OPEN"

def main_page():
    with ui.tabs() as tabs:
        sensors = ui.tab('sensors')
        servos = ui.tab('servos')
        relays = ui.tab('relays')

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

            await asyncio.sleep(1)

    asyncio.create_task(update_table())



    
    with ui.button_group():
        controls["fuel_btn"] = ui.button('Fuel').on_click(fuel_action)
        controls["start_btn"] = ui.button("Start").on_click(start_rocket)

    controls["start_btn"].disable()




async def wait_for_response():
    while True:
        try:
            cm.receive() # We can handle frames using callbacks or by getting frame right from receive() call
        except TransportTimeoutError:
                pass
        except UnregisteredCallbackError as e:
                # print(f"unregistered frame received: {e.frame}")
                pass
        await asyncio.sleep(0)



#####Callbacki do aktualizaji danych
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

    sensors_data["Velocity"] = "{:.2} m/s".format(velocity) 
    

def fuel_intake_update(frame: Frame):
    servo_data["fuel_intake"] = str(frame.payload[0])
    

def oxidizer_intake_update(frame: Frame):
    servo_data["oxidizer_intake"] = str(frame.payload[0])
    

def fuel_main_update(frame: Frame):
    servo_data["fuel_main"] = str(frame.payload[0])
    

def oxidizer_main_update(frame: Frame):
    servo_data["oxidizer_main"] = str(frame.payload[0])
    

@app.on_startup
async def on_starup():
    asyncio.create_task(wait_for_response())

if __name__ in {"__main__", "__mp_main__"}:
   

    cm.change_transport_type(TransportType.TCP)
    cm.connect(TcpSettings("127.0.0.1", 3000))
   # cm.register_callback(fuel_level_update, setup_frames.fuel_frame)
    #cm.register_callback(oxidizer_level_update, setup_frames.oxidizer_frame)
    #cm.register_callback(oxidizer_pressure_update, setup_frames.oxidizer_pressure_frame)
    #cm.register_callback(altitude_update, setup_frames.altitude_frame)
    cm.register_callback(fuel_intake_update, setup_frames.fuel_intake_frame)
    cm.register_callback(oxidizer_intake_update, setup_frames.oxidizer_intake_frame)
    cm.register_callback(fuel_main_update, setup_frames.fuel_main_frame)
    cm.register_callback(oxidizer_main_update, setup_frames.oxidizer_main_frame)

    ui.run(root)

    
    # controls["start_btn"].disabled()