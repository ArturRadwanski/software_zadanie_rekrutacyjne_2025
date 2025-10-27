from communication_library import ids
from communication_library.frame import Frame

fuel_frame = Frame(ids.BoardID.SOFTWARE, 
                           ids.PriorityID.LOW, 
                           ids.ActionID.FEED, 
                           ids.BoardID.ROCKET, 
                           ids.DeviceID.SENSOR, 
                           0, # fuel
                           ids.DataTypeID.FLOAT,
                           ids.OperationID.SENSOR.value.READ)
                           
oxidizer_frame = Frame(ids.BoardID.SOFTWARE, 
                           ids.PriorityID.LOW, 
                           ids.ActionID.FEED, 
                           ids.BoardID.ROCKET, 
                           ids.DeviceID.SENSOR, 
                           1, # oxidizer
                           ids.DataTypeID.FLOAT,
                           ids.OperationID.SENSOR.value.READ)

altitude_frame = Frame(ids.BoardID.SOFTWARE, 
                           ids.PriorityID.LOW, 
                           ids.ActionID.FEED, 
                           ids.BoardID.ROCKET, 
                           ids.DeviceID.SENSOR, 
                           2, # altitude sensor
                           ids.DataTypeID.FLOAT,
                           ids.OperationID.SENSOR.value.READ)

oxidizer_pressure_frame = Frame(ids.BoardID.SOFTWARE, 
                           ids.PriorityID.LOW, 
                           ids.ActionID.FEED, 
                           ids.BoardID.ROCKET, 
                           ids.DeviceID.SENSOR, 
                           3, # pressure sensor
                           ids.DataTypeID.FLOAT,
                           ids.OperationID.SENSOR.value.READ)



fuel_intake_close_frame = Frame(ids.BoardID.ROCKET, 
                           ids.PriorityID.LOW, 
                           ids.ActionID.SERVICE, 
                           ids.BoardID.SOFTWARE, 
                           ids.DeviceID.SERVO, 
                           0, # fuel intake 
                           ids.DataTypeID.INT16,
                           ids.OperationID.SERVO.value.POSITION,
                           (100,) # 0 is for open position, 100 is for closed
                           )

oxidizer_intake_close_frame = Frame(ids.BoardID.ROCKET, 
                           ids.PriorityID.LOW, 
                           ids.ActionID.SERVICE, 
                           ids.BoardID.SOFTWARE, 
                           ids.DeviceID.SERVO, 
                           1, # oxidizer intake 
                           ids.DataTypeID.INT16,
                           ids.OperationID.SERVO.value.POSITION,
                           (100,) # 0 is for open position, 100 is for closed
                           )

fuel_intake_open_frame = Frame(ids.BoardID.ROCKET, 
                           ids.PriorityID.LOW, 
                           ids.ActionID.SERVICE, 
                           ids.BoardID.SOFTWARE, 
                           ids.DeviceID.SERVO, 
                           0, # fuel intake 
                           ids.DataTypeID.INT16,
                           ids.OperationID.SERVO.value.POSITION,
                           (0,) # 0 is for open position, 100 is for closed
                           )

oxidizer_intake_open_frame = Frame(ids.BoardID.ROCKET, 
                           ids.PriorityID.LOW, 
                           ids.ActionID.SERVICE, 
                           ids.BoardID.SOFTWARE, 
                           ids.DeviceID.SERVO, 
                           1, # oxidizer intake 
                           ids.DataTypeID.INT16,
                           ids.OperationID.SERVO.value.POSITION,
                           (0,) # 0 is for open position, 100 is for closed
                           )

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

oxidizer_heater__close_frame = Frame(ids.BoardID.ROCKET, 
                           ids.PriorityID.LOW, 
                           ids.ActionID.SERVICE, 
                           ids.BoardID.SOFTWARE, 
                           ids.DeviceID.RELAY, 
                           0, # oxidizer heater
                           ids.DataTypeID.FLOAT,
                           ids.OperationID.RELAY.value.CLOSE,
                           ()
                           )

open_fuel_main_frame = Frame(ids.BoardID.SOFTWARE, 
                           ids.PriorityID.LOW, 
                           ids.ActionID.FEED, 
                           ids.BoardID.ROCKET, 
                           ids.DeviceID.SERVO, 
                           2, # fuel main
                           ids.DataTypeID.INT16,
                           ids.OperationID.SERVO.value.POSITION,
                           (0,))
    

open_oxidizer_main_frame = Frame(ids.BoardID.SOFTWARE, 
                           ids.PriorityID.LOW, 
                           ids.ActionID.SERVICE, 
                           ids.BoardID.ROCKET, 
                           ids.DeviceID.SERVO, 
                           3, # fuel main
                           ids.DataTypeID.INT16,
                           ids.OperationID.SERVO.value.POSITION,
                           (0,))

open_igniter_frame = Frame(ids.BoardID.SOFTWARE, 
                           ids.PriorityID.LOW, 
                           ids.ActionID.SERVICE, 
                           ids.BoardID.ROCKET, 
                           ids.DeviceID.RELAY, 
                           1, # igniter
                           ids.DataTypeID.FLOAT,
                           ids.OperationID.RELAY.value.OPEN)                           