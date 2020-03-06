import time


class Explorer:
    """
    Class that controls the robots movements.
    """

    def __init__(self, logger, communication, odometry, planet, expression, motor_right, motor_left, color_sensor, us_sensor):
        self.logger = logger
        self.communication = communication
        self.odometry = odometry
        self.planet = planet
        self.motor_right = motor_right
        self.motor_left = motor_left
        self.color_sensor = color_sensor
        self.us_sensor = us_sensor
        self.expression = expression

        self.target_power = 20

        self.stop_cmd = False
        self.is_running = False

        self.logger.debug("Explorer initialized and ready")

    def start(self):
        self.logger.debug("Explorer starting")

        self.is_running = True

        # Setup hardware
        self.color_sensor.mode = "RGB-RAW"  # Measure RGB values
        self.us_sensor.mode = "US-DIST-CM"  # Measure distance in cm
        self.motor_right.reset()
        self.motor_left.reset()
        self.motor_right.stop_action = "coast"
        self.motor_left.stop_action = "coast"

        # See http://www.inpharmix.com/jps/PID_Controller_For_Lego_Mindstorms_Robots.html for documentation
        k_p = 0.11  # Proportional constant
        offset = 170  # Light sensor offset
        target_power_right = self.target_power  # Target power cycle level (20% for right, 22% for left)
        target_power_left = self.target_power + 2
        k_i = 0  # Integral constant
        integral = 0  # Integral
        k_d = 0.04  # Derivative constant
        last_error = 0

        red_counter = 0
        blue_counter = 0

        while not self.stop_cmd:
            if self.us_sensor.distance_centimeters < 15:
                self.logger.debug("Path blocked")
                self.motor_left.duty_cycle_sp = 0
                self.motor_right.duty_cycle_sp = 0
                self.expression.tone_warning()
                self.motor_right.duty_cycle_sp = -target_power_right
                self.motor_left.duty_cycle_sp = target_power_left
                time.sleep(4)  # Replace with odometry stuff
                continue

            rgb = self.color_sensor.bin_data("hhh")  # Read RGB values from sensor
            r = rgb[0]
            g = rgb[1]
            b = rgb[2]
            gs = self.rgb_to_grayscale(r, g, b)  # Convert RGB to grayscale

            if r > 100 > g and b < 100:
                self.logger.debug("Detected RED")
                if red_counter >= 3:
                    self.expression.beep()  # for testing
                    # self.scan_for_paths()
                    red_counter = 0
                    continue
                else:
                    red_counter += 1
            elif 20 <= r <= 40 and 70 <= b <= 100:
                self.logger.debug("Detected BLUE")
                if blue_counter >= 3:
                    self.expression.beep()  # for testing
                    # self.scan_for_paths()
                    blue_counter = 0
                    continue
                else:
                    blue_counter += 1

            # Calculate error, turn and motor powers
            error = gs - offset
            integral = 2/3 * integral + error
            derivative = error - last_error
            last_error = error
            turn = k_p * error + k_i * integral + k_d * derivative
            power_right = target_power_right + turn
            power_left = target_power_left - turn

            # Apply motor powers
            self.motor_left.duty_cycle_sp = power_left
            self.motor_right.duty_cycle_sp = power_right
            self.motor_left.command = "run-direct"
            self.motor_right.command = "run-direct"

            time.sleep(0.05)

        self.is_running = False

    def found_square(self):
        pass

    def found_path(self):
        pass

    def run_motors(self, tp_right, tp_left):
        self.motor_right.duty_cycle_sp = tp_right + 2
        self.motor_left.duty_cycle_sp = tp_left
        self.motor_left.command = "run-direct"
        self.motor_right.command = "run-direct"

    def stop_motors(self):
        self.logger.debug("Stopping motors")
        self.motor_right.stop()
        self.motor_left.stop()

    def scan_for_paths(self):
        self.logger.debug("Scanning for paths")

        self.color_sensor.mode = "COL-COLOR"

        # Drive until we detect either white or black, which means our robot sits directly on the square
        self.run_motors(self.target_power, self.target_power)

        color_val = -1
        while not (color_val == 0 or color_val == 6):
            color_val = self.color_sensor.value()
            time.sleep(0.2)

        started_at_degrees = 1  # Add odometry stuff here

        # Slowly rotate with half the target power
        self.run_motors(self.target_power, - self.target_power)

        current_degrees = 1  # This is a placeholder for some odometry method call inside the while condition

        # We don't technically have to do a full 360, 270 degrees would be enough
        while current_degrees < started_at_degrees + 360:
            color = self.color_sensor.value()

            if color == 1:
                # black -> path
                pass
            elif color == 6:
                # white -> nothing
                pass
            elif color == 2 or color == 5:
                # blue or red -> square
                pass

            current_degrees += 2
            time.sleep(0.1)

        self.stop_motors()
        self.color_sensor.mode = "RGB-RAW"

    def stop(self):
        self.stop_cmd = True
        while self.is_running:
            time.sleep(0.1)
        self.stop_cmd = False
        self.stop_motors()
        self.logger.info("Explorer stopped")

    @staticmethod
    def rgb_to_grayscale(red, green, blue):
        return 0.3 * red + 0.59 * green + 0.11 * blue
