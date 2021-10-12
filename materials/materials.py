from materials.opaque import Opaque
from materials.reflective import Reflective
from materials.transparent import Transparent
from libs import zutils as zu
from libs.obj import Texture

# OPAQUE MATERIALS
SKY = Opaque(diffuse=zu.colors(135 / 255, 206 / 255, 235 / 255), spec=16)
GRASS = Opaque(diffuse=zu.colors(86 / 255, 125 / 255, 70 / 255), spec=128)
STONE = Opaque(diffuse=zu.colors(0.4, 0.4, 0.4), spec=64)
WOOD = Opaque(diffuse=(0.6, 0.2, 0.2), spec=64)
SKIN = Opaque(diffuse=(1, 244 / 255, 161 / 255), spec=64)
BLACK = Opaque(diffuse=(0, 0, 0), spec=128)
KASA = Opaque(diffuse=(172 / 255, 96 / 255, 57 / 255))
WHITE = Opaque(diffuse=(1, 1, 1))

# REFLECTIVE MATERIALS
MIRROR = Reflective(spec=128)
GOLD = Reflective(diffuse=zu.colors(1, 0.8, 0), spec=32)
COPPER = Reflective(diffuse=zu.colors(168 / 255, 98 / 255, 66 / 255), spec=16)
ALUMINUM = Reflective(diffuse=zu.colors(210 / 255, 217 / 255, 219 / 255), spec=128)
METALLIC = Reflective(diffuse=zu.colors(170 / 255, 169 / 255, 173 / 255), spec=128)
NEON_YELLOW = Reflective(diffuse=zu.colors(1, 243 / 255, 0), spec=128)

# TRANSPARENT MATERIALS
GLASS = Transparent(spec=64, ior=1.5)
CRISTAL = Transparent(spec=32, ior=1.51)
ICE = Transparent(spec=128, ior=1.31)
QUARTZ = Transparent(spec=32, ior=1.46)
SAPPHIRE = Transparent(spec=32, ior=1.77)
DIAMOND = Transparent(spec=30, ior=2.41)


