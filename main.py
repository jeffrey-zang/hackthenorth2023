try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup((3, 5, 7, 8, 10, 11, 12, 13, 15, 16, 18, 19, 21, 22, 23, 24, 25, 26, 29, 31, 32, 33, 35, 36, 37, 38, 40), GPIO.OUT)
    pi = True
except ModuleNotFoundError: 
    pi = False

import time

import adhawkapi
import adhawkapi.frontend
lastBlink = 0
moveMode = False
direction = None # null or 'left' or 'right' or 'forward' or 'backward'


class FrontendData:
    ''' BLE Frontend '''

    def __init__(self):
        # Instantiate an API object
        # TODO: Update the device name to match your device
        self._api = adhawkapi.frontend.FrontendApi(ble_device_name='ADHAWK MINDLINK-283')

        # Tell the api that we wish to receive eye tracking data stream
        # with self._handle_et_data as the handler
        self._api.register_stream_handler(adhawkapi.PacketType.EYETRACKING_STREAM, self._handle_et_data)

        # Tell the api that we wish to tap into the EVENTS stream
        # with self._handle_events as the handler
        self._api.register_stream_handler(adhawkapi.PacketType.EVENTS, self._handle_events)

        # Start the api and set its connection callback to self._handle_tracker_connect/disconnect.
        # When the api detects a connection to a MindLink, this function will be run.
        self._api.start(tracker_connect_cb=self._handle_tracker_connect,
                        tracker_disconnect_cb=self._handle_tracker_disconnect)

    def shutdown(self):
        '''Shutdown the api and terminate the bluetooth connection'''
        self._api.shutdown()

    @staticmethod
    def _handle_et_data(et_data: adhawkapi.EyeTrackingStreamData):
        ''' Handles the latest et data '''
        if et_data.gaze is not None:
            xvec, yvec, zvec, v = et_data.gaze
            # print(f'Gaze: x={xvec:.2f}, y={yvec:.2f}, z={zvec:.2f}', end="\r")

            if moveMode:
                x = xvec
                y = yvec
                if -2 <= x <= 2 and -2 <= y <= 2:
                    direction = None
                else:
                    abx = abs(x)
                    aby = abs(y)
                    if abx > aby: 
                        if x < 0:
                            direction = "left"
                        else:
                            direction = "right"
                    else:
                        if y < 0:
                            direction = "backwards"
                        else:
                            direction = "forwards"
                print(direction)
        # if et_data.eye_center is not None:
        #     if et_data.eye_mask == adhawkapi.EyeMask.BINOCULAR:
        #         rxvec, ryvec, rzvec, lxvec, lyvec, lzvec = et_data.eye_center
        #         print(f'Eye center: Left=(x={lxvec:.2f},y={lyvec:.2f},z={lzvec:.2f}) '
        #               f'Right=(x={rxvec:.2f},y={ryvec:.2f},z={rzvec:.2f})')

        # if et_data.pupil_diameter is not None:
        #     if et_data.eye_mask == adhawkapi.EyeMask.BINOCULAR:
        #         rdiameter, ldiameter = et_data.pupil_diameter
        #         print(f'Pupil diameter: Left={ldiameter:.2f} Right={rdiameter:.2f}')

        # if et_data.imu_quaternion is not None:
        #     if et_data.eye_mask == adhawkapi.EyeMask.BINOCULAR:
        #         x, y, z, w = et_data.imu_quaternion
        #         print(f'IMU: x={x:.2f},y={y:.2f},z={z:.2f},w={w:.2f}')
        
    @staticmethod
    def _handle_events(event_type, timestamp, *args):
        global lastBlink, moveMode
        if event_type == adhawkapi.Events.BLINK:
            duration = args[0]
            print(f'Got blink: {timestamp} {duration}, diff {timestamp - lastBlink}')
            if (timestamp - lastBlink < 1):
                print(f"Got double-blink")
                moveMode = not moveMode
            lastBlink = timestamp
            
        # if event_type == adhawkapi.Events.EYE_CLOSED:
        #     eye_idx = args[0]
        #     print(f'Eye Close: {timestamp} {eye_idx}')
        # if event_type == adhawkapi.Events.EYE_OPENED:
        #     eye_idx = args[0]
        #     print(f'Eye Open: {timestamp} {eye_idx}')

    def _handle_tracker_connect(self):
        print("Tracker connected")
        self._api.set_et_stream_rate(60, callback=lambda *args: None)

        self._api.set_et_stream_control([
            adhawkapi.EyeTrackingStreamTypes.GAZE,
            adhawkapi.EyeTrackingStreamTypes.EYE_CENTER,
            adhawkapi.EyeTrackingStreamTypes.PUPIL_DIAMETER,
            adhawkapi.EyeTrackingStreamTypes.IMU_QUATERNION,
        ], True, callback=lambda *args: None)

        self._api.set_event_control(adhawkapi.EventControlBit.BLINK, 1, callback=lambda *args: None)
        self._api.set_event_control(adhawkapi.EventControlBit.EYE_CLOSE_OPEN, 1, callback=lambda *args: None)

    def _handle_tracker_disconnect(self):
        print("Tracker disconnected")


def main():
    ''' App entrypoint '''
    frontend = FrontendData()
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        frontend.shutdown()

if __name__ == '__main__':
    main()