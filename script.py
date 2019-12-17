#!/usr/bin/env python

# Copyright (c) 2019 Computer Vision Center (CVC) at the Universitat Autonoma de
# Barcelona (UAB).
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

import glob
import os
import sys

try:
    # The .egg file is copied into the repository to speed up the process
    sys.path.append(glob.glob('./carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

import random
import time
import numpy as np
import cv2

IM_WIDTH = 640
IM_HEIGHT = 480

def process_img(image):
    i = np.array(image.raw_data)  # convert to an array
    i2 = i.reshape((IM_HEIGHT, IM_WIDTH, 4))  # was flattened, so we're going to shape it.
    i3 = i2[:, :, :3]  # remove the alpha (basically, remove the 4th index  of every pixel. Converting RGBA to RGB)
    cv2.imshow("", i3)  # show it.
    cv2.waitKey(1)
    return i3/255.0  # normalize

def main():
    actor_list = []
    
    try:
        client = carla.Client('localhost', 2000)
        client.set_timeout(2.0)
        world = client.get_world()
        blueprint_library = world.get_blueprint_library()

        npc_count = 10

        for i in range(npc_count):
            bp = random.choice(blueprint_library.filter('vehicle'))
            spawn_point = random.choice(world.get_map().get_spawn_points())
            vehicle = world.spawn_actor(bp, spawn_point)
            vehicle.set_autopilot(True)

            actor_list.append(vehicle)
            print('Created NPC: %s' % vehicle.type_id)
        
        bp = random.choice(blueprint_library.filter('model3'))
        spawn_point = random.choice(world.get_map().get_spawn_points())
        user_vehicle = world.spawn_actor(bp, spawn_point)
        user_vehicle.set_autopilot(False)

        actor_list.append(user_vehicle)
        print('Created User: %s' % user_vehicle.type_id)

        # Dummy car driving always straight
        user_vehicle.apply_control(carla.VehicleControl(throttle = 1.0, steer = 0.0))

        cam_bp = blueprint_library.find('sensor.camera.rgb')
        # change the dimensions of the image
        cam_bp.set_attribute('image_size_x', f'{IM_WIDTH}')
        cam_bp.set_attribute('image_size_y', f'{IM_HEIGHT}')
        cam_bp.set_attribute('fov', '110')

        spawn_point = carla.Transform(carla.Location(x=2.5, z=0.7))

        sensor = world.spawn_actor(cam_bp, spawn_point, attach_to=user_vehicle)
        actor_list.append(sensor)

        sensor.listen(lambda data: process_img(data))

        # # Let's add now a "depth" camera attached to the vehicle. Note that the
        # # transform we give here is now relative to the vehicle.
        # camera_bp = blueprint_library.find('sensor.camera.depth')
        # camera_transform = carla.Transform(carla.Location(x=1.5, z=2.4))
        # camera = world.spawn_actor(camera_bp, camera_transform, attach_to=vehicle)
        # actor_list.append(camera)
        # print('created %s' % camera.type_id)

        # # Now we register the function that will be called each time the sensor
        # # receives an image. In this example we are saving the image to disk
        # # converting the pixels to gray-scale.
        # cc = carla.ColorConverter.LogarithmicDepth
        # camera.listen(lambda image: image.save_to_disk('_out/%06d.png' % image.frame_number, cc))

        # # Oh wait, I don't like the location we gave to the vehicle, I'm going
        # # to move it a bit forward.
        # location = vehicle.get_location()
        # location.x += 40
        # vehicle.set_location(location)
        # print('moved vehicle to %s' % location)

        # # But the city now is probably quite empty, let's add a few more
        # # vehicles.
        # transform.location += carla.Location(x=40, y=-3.2)
        # transform.rotation.yaw = -180.0
        # for _ in range(0, 10):
        #     transform.location.x += 8.0

        #     bp = random.choice(blueprint_library.filter('vehicle'))

        #     # This time we are using try_spawn_actor. If the spot is already
        #     # occupied by another object, the function will return None.
        #     npc = world.try_spawn_actor(bp, transform)
        #     if npc is not None:
        #         actor_list.append(npc)
        #         npc.set_autopilot()
        #         print('created %s' % npc.type_id)
        time.sleep(15)
    finally:
        print('Destroying actors...')

        for actor in actor_list:
            actor.destroy()

        print('Destroying actors... DONE')


if __name__ == '__main__':
    main()
