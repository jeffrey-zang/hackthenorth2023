import time

from arduino import write
import adhawkapi
import adhawkapi.frontend

import tkinter

root = tkinter.Tk()

s = tkinter.Canvas(root, width=1000, height=1000)
s.pack()
x = 0
y = 0

lastBlink = 0
moveMode = False
direction = None  # null or 'left' or 'right' or 'forward' omr 'backward'


class FrontendData:
    def __init__(self):
        self._api = adhawkapi.frontend.FrontendApi(
            ble_device_name="ADHAWK MINDLINK-283"
        )

        self._api.register_stream_handler(
            adhawkapi.PacketType.EYETRACKING_STREAM, self._handle_et_data
        )

        self._api.register_stream_handler(
            adhawkapi.PacketType.EVENTS, self._handle_events
        )

        self._api.start(
            tracker_connect_cb=self._handle_tracker_connect,
            tracker_disconnect_cb=self._handle_tracker_disconnect,
        )

    def shutdown(self):
        self._api.shutdown()

    @staticmethod
    def _handle_et_data(et_data: adhawkapi.EyeTrackingStreamData):
        global x, y, direction
        if et_data.gaze is not None:
            xvec, yvec, zvec, v = et_data.gaze

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
                            direction = "l"
                        else:
                            direction = "r"
                    else:
                        if y < 0:
                            direction = "b"
                        else:
                            direction = "f"
                # print(direction)

    @staticmethod
    def _handle_events(event_type, timestamp, *args):
        global lastBlink, moveMode
        if event_type == adhawkapi.Events.BLINK:
            duration = args[0]
            print(f"Got blink: {timestamp} {duration}, diff {timestamp - lastBlink}")
            if timestamp - lastBlink < 0.6:
                print(f"Got double-blink")
                moveMode = not moveMode
            lastBlink = timestamp

    def _handle_tracker_connect(self):
        print("Tracker connected")
        self._api.set_et_stream_rate(60, callback=lambda *args: None)

        self._api.set_et_stream_control(
            [
                adhawkapi.EyeTrackingStreamTypes.GAZE,
            ],
            True,
            callback=lambda *args: None,
        )

        self._api.set_event_control(
            adhawkapi.EventControlBit.BLINK, 1, callback=lambda *args: None
        )

    def _handle_tracker_disconnect(self):
        print("Tracker disconnected")


def main():
    frontend = FrontendData()
    try:
        while True:
            write(f"{direction},{int(moveMode)}")

            bruh = s.create_oval(
                (500 + x * 97) + 15,
                (500 + (-y) * 97) + 15,
                (500 + x * 97) - 15,
                (500 + (-y) * 97) - 15,
                fill="#000",
            )
            s.update()
            time.sleep(0.1)
            s.delete(bruh)
    except (KeyboardInterrupt, SystemExit):
        frontend.shutdown()


if __name__ == "__main__":
    main()
