import math
from vpython import *

scale_radius = 1/1e5
scale_distance = 1/1e8  #Distance from the sun

sun_radius = 0.5
planet_data = [
    {"name":"Mercury", "radius":2440*scale_radius, "distance":57.9e6*scale_distance, "texture":"textures/mercury.jpg", "omega":0.04, "theta":0},
    {"name":"Venus",   "radius":6052*scale_radius, "distance":108.2e6*scale_distance, "texture":"textures/venus.jpg", "omega":0.03, "theta":0.5},
    {"name":"Earth",   "radius":6371*scale_radius, "distance":149.6e6*scale_distance, "texture":textures.earth, "omega":0.02, "theta":1},
    {"name":"Mars",    "radius":3390*scale_radius, "distance":227.9e6*scale_distance, "texture":"textures/mars.jpg", "omega":0.015, "theta":1.5},
    {"name":"Jupiter", "radius":69911*scale_radius, "distance":778.5e6*scale_distance, "texture":"textures/jupiter.jpg", "omega":0.008, "theta":2},
    {"name":"Saturn",  "radius":58232*scale_radius, "distance":1433e6*scale_distance, "texture":"textures/saturn.jpg", "omega":0.006, "theta":2.5},
    {"name":"Uranus",  "radius":25362*scale_radius, "distance":2872e6*scale_distance, "texture":"textures/uranus.jpg", "omega":0.004, "theta":3},
    {"name":"Neptune", "radius":24622*scale_radius, "distance":4495e6*scale_distance, "texture":"textures/neptune.jpg", "omega":0.003, "theta":3.5}
]

scene = canvas(title="Solar System | Press space to pause", width=1900, height=900, background=color.black)
scene.center = vector(0, 0, 0)
scene.range = 5

sun = sphere(radius=sun_radius, texture="textures/sun.jpg", emissive=True, shininess=1)

planets = []
saturn_rings = []

for pdata in planet_data:
    p = sphere(radius=pdata["radius"], texture=pdata.get("texture"), make_trail=True)
    pdata["obj"] = p
    planets.append(pdata)

    #Saturn's rings
    if pdata["name"] == "Saturn":
        ring_radii = [p.radius*1.3, p.radius*1.5, p.radius*1.7, p.radius*1.9]
        ring_thickness = [0.004, 0.005, 0.004, 0.003]
        for rr, rt in zip(ring_radii, ring_thickness):
            ring_obj = ring(
                pos=p.pos,
                axis=vector(0,1,0),
                radius=rr,
                thickness=rt,
                texture=textures.wood_old,
                opacity=0.6
            )
            saturn_rings.append(ring_obj)

paused = False
def toggle_pause(evt):
    global paused
    if evt.key == " ":
        paused = not paused

scene.bind('keydown', toggle_pause)

while True:
    rate(60)
    if not paused:
        for p in planets:
            p["theta"] += p["omega"]
            p["obj"].pos = vector(p["distance"]*math.cos(p["theta"]), 0, p["distance"]*math.sin(p["theta"]))
            if p["name"] == "Saturn":
                for ring_obj in saturn_rings:
                    ring_obj.pos = p["obj"].pos