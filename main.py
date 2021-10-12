from raytracer import Raytracer, V3
from polygons.polygons import Sphere, AABB
from polygons.cone import Cone
from lights.point import PointLight
from lights.ambient import AmbientLight
from lights.directional import DirectionalLight
from materials.materials import *
from libs.obj import EnvMap

width = 1920
height = 1080

raytracer = Raytracer(width, height)
raytracer.envmap = EnvMap('textures/cannon.bmp')
# TEXTURE MATERIALS
SUN = Opaque(texture=Texture('textures/sun.bmp'))
SNOW = Reflective(texture=Texture('textures/snow.bmp'))

raytracer.ambientLight = AmbientLight(strength=0.1)
raytracer.directionalLight = DirectionalLight(direction=V3(1, -1, -2), intensity=0.6)
raytracer.pointLights.append(PointLight(position=V3(9, 4.5, 0), intensity=1, color=(252 / 255, 244 / 255, 144 / 255)))
raytracer.pointLights.append(PointLight(position=V3(3, 3, 0), intensity=0.8, color=(252 / 255, 244 / 255, 144 / 255)))
raytracer.pointLights.append(PointLight(position=V3(1, 0, 0), intensity=0.8))


# Personaje
raytracer.scene.append(Cone(V3(1.05, 1.2, -13), 0.70, V3(0, -1, 0), 2, SKY))
raytracer.scene.append(Sphere(V3(1.05, -0.65, -13), 1.1, GRASS))
raytracer.scene.append(AABB(V3(1.05, -1.9, -13), V3(0.5, 0.8, 0.2), GRASS))
raytracer.scene.append(AABB(V3(1.05, -2.9, -13), V3(1.9, 2, 0.3), BLACK))
# Piernas
raytracer.scene.append(AABB(V3(1, -3.8, -12), V3(1.8, 0.18, 0.5), BLACK))
raytracer.scene.append(AABB(V3(0.295, -3.78, -11), V3(0.4, 0.155, 1.5), BLACK))
raytracer.scene.append(AABB(V3(1.7, -3.78, -11), V3(0.4, 0.155, 1.5), BLACK))

raytracer.scene.append(AABB(V3(0.303, -4.04, -10), V3(0.4, 0.8, 0.14), GRASS))
raytracer.scene.append(AABB(V3(1.69, -4.04, -10), V3(0.4, 0.8, 0.14), GRASS))
raytracer.scene.append(AABB(V3(0.3, -4.1, -9), V3(0.4, 0.155, 0.3), COPPER))
raytracer.scene.append(AABB(V3(1.55, -4.1, -9), V3(0.4, 0.155, 0.3), COPPER))
# # Brazo derecho
raytracer.scene.append(Sphere(V3(2.25, -2.1, -13), 0.28, BLACK))
raytracer.scene.append(Sphere(V3(2.5, -2.5, -13), 0.25, BLACK))
raytracer.scene.append(Sphere(V3(2.7, -2.8, -13), 0.25, BLACK))
raytracer.scene.append(Sphere(V3(2.9, -3.1, -13), 0.23, BLACK))
raytracer.scene.append(Sphere(V3(3.1, -3.4, -13), 0.18, BLACK))
raytracer.scene.append(AABB(V3(3.05, -3.42, -12), V3(0.2, 0.1, 1.3), GRASS))
raytracer.scene.append(AABB(V3(3.15, -3.34, -11), V3(0.5, 0.1, 0.32), GRASS))
# Brazo izquierdo
raytracer.scene.append(Sphere(V3(-0.15, -2.1, -13), 0.28, BLACK))
raytracer.scene.append(Sphere(V3(-0.35, -2.5, -13), 0.25, BLACK))
raytracer.scene.append(Sphere(V3(-0.55, -2.8, -13), 0.25, BLACK))
raytracer.scene.append(Sphere(V3(-0.75, -3.1, -13), 0.23, BLACK))
raytracer.scene.append(Sphere(V3(-0.95, -3.4, -13), 0.18, BLACK))
raytracer.scene.append(AABB(V3(-0.95, -3.4, -12), V3(0.2, 0.1, 1.3), GRASS))
raytracer.scene.append(AABB(V3(-1.08, -3.33, -11), V3(0.5, 0.1, 0.32), GRASS))

raytracer.scene.append(Sphere(V3(3.2, -2.2, -11), 1, SNOW))
raytracer.scene.append(Cone(V3(-0.8, -0.8, -8), 0.85, V3(0, -1, 0), 1.3, QUARTZ))

# Sol
raytracer.scene.append(Sphere(V3(9, 4.5, -12), 0.8, SUN))

raytracer.render()
raytracer.end('output.bmp')
