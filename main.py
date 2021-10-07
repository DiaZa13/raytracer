from raytracer import Raytracer, V3
from polygons.polygons import Sphere, AABB
from lights.point import PointLight
from lights.ambient import AmbientLight
from lights.directional import DirectionalLight
from materials.materials import *
from libs.obj import EnvMap

width = 256
height = 256

raytracer = Raytracer(width, height)
raytracer.envmap = EnvMap('textures/park.bmp')

raytracer.ambientLight = AmbientLight(strength=0.1)
raytracer.directionalLight = DirectionalLight(direction=V3(1, -1, -2), intensity=0.5)
raytracer.pointLights.append(PointLight(position=V3(0, 2, 0), intensity=0.5))

raytracer.scene.append(Sphere(V3(-2, 0, -8), 1.5, GLASS))


raytracer.render()
raytracer.end('output.bmp')
