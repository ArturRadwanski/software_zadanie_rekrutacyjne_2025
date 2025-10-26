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

angle_frame = Frame(ids.BoardID.SOFTWARE, 
                           ids.PriorityID.LOW, 
                           ids.ActionID.FEED, 
                           ids.BoardID.ROCKET, 
                           ids.DeviceID.SENSOR, 
                           4, # gyroscope
                           ids.DataTypeID.FLOAT,
                           ids.OperationID.SENSOR.value.READ)

fuel_intake_frame = Frame(ids.BoardID.SOFTWARE, 
                           ids.PriorityID.LOW, 
                           ids.ActionID.FEED, 
                           ids.BoardID.ROCKET, 
                           ids.DeviceID.SERVO, 
                           0, #fuel_intake
                           ids.DataTypeID.INT16,
                           ids.OperationID.SENSOR.value.READ)
                    
oxidizer_intake_frame = Frame(ids.BoardID.SOFTWARE, 
                           ids.PriorityID.LOW, 
                           ids.ActionID.FEED, 
                           ids.BoardID.ROCKET, 
                           ids.DeviceID.SERVO, 
                           1, #oxidizer_intake
                           ids.DataTypeID.INT16,
                           ids.OperationID.SENSOR.value.READ)

fuel_main_frame = Frame(ids.BoardID.SOFTWARE, 
                           ids.PriorityID.LOW, 
                           ids.ActionID.FEED, 
                           ids.BoardID.ROCKET, 
                           ids.DeviceID.SERVO, 
                           2, #fuel_main
                           ids.DataTypeID.INT16,
                           ids.OperationID.SENSOR.value.READ)

oxidizer_main_frame = Frame(ids.BoardID.SOFTWARE, 
                           ids.PriorityID.LOW, 
                           ids.ActionID.FEED, 
                           ids.BoardID.ROCKET, 
                           ids.DeviceID.SERVO, 
                           3, #oxidizer_main
                           ids.DataTypeID.INT16,
                           ids.OperationID.SENSOR.value.READ)