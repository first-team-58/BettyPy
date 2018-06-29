#import maestro

# For motor controllers, servo speed setting dampens acceleration (acts like inertia).
# Higher values will reduce inertia (try values around 50 to 100)
INERTIA = 200
#

class DriveTrain:
        # Init drive train, passing maestro controller obj, and channel
        # numbers for the motor servos Left and Right
	def __init__(self, maestro,chLeftFront,chRightFront, chLeftRear, chRightRear):
		self.maestro = maestro
		self.chRightFront = chRightFront
		self.chLeftFront = chLeftFront
		self.chLeftRear = chLeftRear
		self.chRightRear = chRightRear
		# Init motor accel/speed params
		self.maestro.setAccel(chRightFront,0)
		self.maestro.setAccel(chLeftFront,0)
		self.maestro.setAccel(chRightRear,0)
		self.maestro.setAccel(chLeftRear,0)
		self.maestro.setSpeed(chRightFront,INERTIA)
		self.maestro.setSpeed(chLeftFront,INERTIA)
		self.maestro.setSpeed(chRightRear, INERTIA)
		# Right motor min/center/max vals
		self.minR = 2760
		self.centerR = 6000
		self.maxR = 9300
		# Left motor min/center/max vals
		self.minL = 2760
		self.centerL = 6000
		self.maxL = 9300

	# Mix joystick inputs into motor L/R mixes
	def mecanumMix(self, dir, mag, rot):
		dirrad = math.radians(dir)
		x = mag*math.sin(dirrad)
		y = mag*math.cos(dirrad)
		motorLF = x + y + rot
		motorRF = -x + y - rot
		motorLR = -x + y + rot
		motorRR = x + y - rot
		return (motorRF, motorLF, motorRR, motorLR)

	# Scale motor speeds (-1 to 1) to maestro servo target values
	def maestroScale(self, motorRF, motorLF, motorRR, motorLR):
		if (motorRF >= 0) :
			rf = int(self.centerR + (self.maxR - self.centerR) * motorRF)
		else:
			rf = int(self.centerR + (self.centerR - self.minR) * motorRF)
		if (motorLF >= 0) :
			lf = int(self.centerL + (self.maxL - self.centerL) * motorLF)
		else:
			lf = int(self.centerL + (self.centerL - self.minL) * motorLF)
		if (motorRR >= 0) :
			rr = int(self.centerR + (self.maxR - self.centerR) * motorRR)
		else:
			rr = int(self.centerR + (self.centerR - self.minR) * motorRR)
		if (motorLR >= 0) :
			lr = int(self.centerL + (self.maxL - self.centerL) * motorLR)
		else:
			lr = int(self.centerL + (self.centerL - self.minL) * motorLR)
		return (rf, lf, rr, lr)

	# Blend X and Y joystick inputs for arcade drive and set servo
	# output to drive motor controllers
	def drive(self, dir, mag, rot):
		(motorRF, motorLF, motorRR, motorLR) = self.mecanumMix(dir, mag, )
		(servoRF, servoLF, servoRR, servoLR) = self.maestroScale(motorRF, motorLF, motorRR, motorLR)
		#print "Target R = ",servoR
		self.maestro.setTarget(self.chRightFront, servoRF)
		self.maestro.setTarget(self.chLeftFront, servoLF)
		self.maestro.setTarget(self.chRightRear, servoRR)
		self.maestro.setTarget(self.chLeftRear, servoLR)

	# Set both motors to stopped (center) position
	def stop(self):
		self.maestro.setTarget(self.chRightFront, self.centerR)
		self.maestro.setTarget(self.chLeftFront, self.centerL)
		self.maestro.setTarget(self.chRightRear, self.centerR)
		self.maestro.setTarget(self.chLeftRear, self.centerL)

	# Close should be used when shutting down Drive object
	def close(self):
		self.stop()
