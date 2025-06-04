import math

class ControlPID_Pendule:
    def __init__(self, Kp=150.0, Kd=35.0, Ki=1.0):
        self.Kp = Kp
        self.Kd = Kd
        self.Ki = Ki
        self.int_e = 0.0
        self.err_prev = 0.0

    def reset(self):
        self.int_e = self.err_prev = 0.0

    def compute(self, theta, omega, dt):
        error = -theta
        self.int_e += error * dt
        d_err = (error - self.err_prev) / dt if dt else 0.0
        self.err_prev = error
        return self.Kp * error - self.Kd * omega + self.Ki * self.int_e
