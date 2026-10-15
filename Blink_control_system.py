import cv2
import mediapipe as mp
import numpy as np
import serial
import time
from abc import ABC, abstractmethod


# ===================== DEVICE LAYER =====================
class Device(ABC):
    @abstractmethod
    def on(self): pass

    @abstractmethod
    def off(self): pass

    @abstractmethod
    def close(self): pass


class Arduino(Device):
    def __init__(self, port='COM4', baud=9600):
        self.active = False
        try:
            self.conn = serial.Serial(port, baud, timeout=1)
            time.sleep(2)
            self.active = True
        except Exception as e:
            print("Arduino connection failed:", e)
            self.active = False

    def send(self, msg: bytes):
        if self.active:
            self.conn.write(msg)

    def on(self):
        self.send(b'1')

    def off(self):
        self.send(b'0')

    def close(self):
        if self.active:
            self.conn.close()


class DemoDevice(Device):
    def on(self):
        print("LIGHT ON")

    def off(self):
        print("LIGHT OFF")

    def close(self):
        print("DEVICE CLOSED")


# ===================== BLINK STATE MACHINE =====================
class BlinkStateMachine:
    """
    OPEN -> CLOSED -> OPEN transition detector
    Ensures ONE blink = ONE event (no double triggers)
    """
    def __init__(self, threshold=0.23, min_closed_time=0.08):
        self.threshold = threshold
        self.min_closed_time = min_closed_time

        self.state = "OPEN"
        self.closed_start_time = None

    def update(self, ear: float):
        now = time.time()

        # Eye is closed
        if ear < self.threshold:
            if self.state == "OPEN":
                self.state = "CLOSING"
                self.closed_start_time = now

            elif self.state == "CLOSING":
                if now - self.closed_start_time >= self.min_closed_time:
                    self.state = "CLOSED"

        # Eye is open
        else:
            if self.state == "CLOSED":
                self.state = "OPEN"
                return True  # valid blink completed

            self.state = "OPEN"

        return False


# ===================== EAR CALCULATOR =====================
class EARCalculator:
    LEFT = [33, 160, 158, 133, 153, 144]
    RIGHT = [362, 385, 387, 263, 373, 380]

    def compute(self, lm, w, h):
        def eye_ratio(eye):
            pts = [(lm[i].x * w, lm[i].y * h) for i in eye]
            p1, p2, p3, p4, p5, p6 = [np.array(p) for p in pts]

            v = (np.linalg.norm(p2 - p6) + np.linalg.norm(p3 - p5)) / 2
            h_dist = np.linalg.norm(p1 - p4)

            return v / h_dist if h_dist else 0

        left = eye_ratio(self.LEFT)
        right = eye_ratio(self.RIGHT)

        return (left + right) / 2


# ===================== BRAIN CONTROLLER =====================
class BlinkController:
    def __init__(self):
        self.calculator = EARCalculator()
        self.state_machine = BlinkStateMachine()

    def process(self, landmarks, w, h):
        ear = self.calculator.compute(landmarks, w, h)
        blink_event = self.state_machine.update(ear)
        return blink_event, ear


# ===================== MAIN SYSTEM =====================
class BlinkSystem:
    def __init__(self, device: Device):
        self.device = device
        self.controller = BlinkController()

        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True
        )

        self.cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        self.state = False
        self.blink_count = 0

    def toggle_device(self):
        self.state = not self.state
        if self.state:
            self.device.on()
        else:
            self.device.off()

    def run(self):
        while True:
            ok, frame = self.cam.read()
            if not ok:
                break

            h, w, _ = frame.shape
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = self.face_mesh.process(rgb)

            if result.multi_face_landmarks:
                lm = result.multi_face_landmarks[0].landmark

                blink, ear = self.controller.process(lm, w, h)

                if blink:
                    self.blink_count += 1
                    self.toggle_device()

                cv2.putText(frame, f"EAR: {ear:.2f}", (20, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                cv2.putText(frame, f"Blinks: {self.blink_count}", (20, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

                cv2.putText(frame, f"Light: {'ON' if self.state else 'OFF'}", (20, 120),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            cv2.imshow("Blink System", frame)

            if cv2.waitKey(1) == 27:
                break

        self.cleanup()

    def cleanup(self):
        self.cam.release()
        self.device.close()
        cv2.destroyAllWindows()


# ===================== MAIN =====================
if __name__ == "__main__":
    device = Arduino()  # or DemoDevice()
    BlinkSystem(device).run()