all: build run

# Define the PWM GPIO pin number for the fan
MY_FAN_CONTROL_PWM       := 18

build:
	docker build -t ibmosquito/fanctrl:1.0.0 .

# Running `make dev` will setup a working environment, just the way I like it.
# On entry to the container's bash shell, run `cd /outside/src` to work here.
dev: build
	-docker rm -f fanctrl 2> /dev/null || :
	docker run -it --name fanctrl \
            --privileged --restart unless-stopped \
            -e MY_FAN_CONTROL_PWM=$(MY_FAN_CONTROL_PWM) \
            --volume /sys/class/thermal/thermal_zone0/temp:/cputemp \
            --volume `pwd`:/outside \
            ibmosquito/fanctrl:1.0.0 /bin/sh

# Run the container as a daemon (build not forecd here, sp must build it first)
run:
	-docker rm -f fanctrl 2> /dev/null || :
	docker run -it --name fanctrl \
            --privileged --restart unless-stopped \
            -e MY_FAN_CONTROL_PWM=$(MY_FAN_CONTROL_PWM) \
            --volume /sys/class/thermal/thermal_zone0/temp:/cputemp \
            ibmosquito/fanctrl:1.0.0

exec:
	docker exec -it fanctrl /bin/sh

push:
	docker push ibmosquito/fanctrl:1.0.0

stop:
	-docker rm -f fanctrl 2>/dev/null || :

clean: stop
	-docker rmi ibmosquito/fanctrl:1.0.0 2>/dev/null || :

.PHONY: all build dev run push exec stop clean

