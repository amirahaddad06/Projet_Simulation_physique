class ControlPID_Pendule:
    def __init__(self, Kp, Kd, Ki, setpoint=0.0):
        self.Kp = Kp
        self.Kd = Kd
        self.Ki = Ki
        self.setpoint = setpoint
        self.integral = 0.0
        self.prev_error = 0.0

    def compute(self, measurement, derivative, dt):
        error = self.setpoint - measurement
        self.integral += error * dt
        d_error = (error - self.prev_error) / dt
        self.prev_error = error
        return self.Kp * error + self.Kd * (-derivative) + self.Ki * self.integral
