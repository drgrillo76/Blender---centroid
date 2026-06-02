#Centroid analysis - Blender 5.0.1

import bpy
import math
from mathutils import Vector

print("=" * 60)
print("TRANSLATION AND ROTATION ANALYSIS")
print("=" * 60)

selecionados = bpy.context.selected_objects

if len(selecionados) != 2:
    print(f"\n❌ ERROR: Select exactly 2 objects. You selected {len(selecionados)}.")
else:
    obj1 = selecionados[0]
    obj2 = selecionados[1]

    print(f"\n📦 Selected objects:")
    print(f"   1. {obj1.name}")
    print(f"   2. {obj2.name}")

    def extrair_vertices(obj):
        vertices = []
        for i, vert in enumerate(obj.data.vertices):
            if i >= 3:
                break
            coords = obj.matrix_world @ vert.co
            vertices.append((coords.x, coords.y, coords.z))
        return vertices

    vertices1 = extrair_vertices(obj1)
    vertices2 = extrair_vertices(obj2)

    def calcular_centroide(pontos):
        soma = Vector((0, 0, 0))
        for p in pontos:
            soma += Vector(p)
        return soma / 3

    c1 = calcular_centroide(vertices1)
    c2 = calcular_centroide(vertices2)

    print(f"\n📍 CENTROIDS:")
    print(f"   {obj1.name}: ({c1.x:.6f}, {c1.y:.6f}, {c1.z:.6f}) m")
    print(f"   {obj2.name}: ({c2.x:.6f}, {c2.y:.6f}, {c2.z:.6f}) m")

    # Translação (mantém o valor em metros, mas será exibido como mm)
    translacao = c2 - c1
    distancia = translacao.length

    print("\n📏 CENTROID TRANSLATION:")
    print(f"   ΔX = {translacao.x:.5f} mm")
    print(f"   ΔY = {translacao.y:.5f} mm")
    print(f"   ΔZ = {translacao.z:.5f} mm")
    print(f"   Total distance = {distancia:.5f} mm")

    # Cálculo da rotação
    vetores1 = [Vector(p) - c1 for p in vertices1]
    vetores2 = [Vector(p) - c2 for p in vertices2]

    def angulo_entre_vetores(v1, v2):
        return math.degrees(v1.angle(v2))

    angulos = []
    for i in range(min(3, len(vetores1), len(vetores2))):
        ang = angulo_entre_vetores(vetores1[i], vetores2[i])
        angulos.append(ang)

    print("\n🔄 ROTATION (angular difference):")
    for i, ang in enumerate(angulos):
        print(f"   Vertex {i+1}: {ang:.2f}°")
    if angulos:
        print(f"   Average: {sum(angulos)/len(angulos):.2f}°")

    # Pontos de referência visuais
    bpy.ops.object.empty_add(type='SPHERE', location=c1)
    empty1 = bpy.context.active_object
    empty1.name = f"CM_{obj1.name}"
    empty1.empty_display_size = 0.05

    bpy.ops.object.empty_add(type='SPHERE', location=c2)
    empty2 = bpy.context.active_object
    empty2.name = f"CM_{obj2.name}"
    empty2.empty_display_size = 0.05

    print("\n✨ Analysis completed!")
    print(f"   ✅ Reference points created: '{empty1.name}' and '{empty2.name}'")

    # Salvar resultados
    import os
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    arquivo = os.path.join(desktop, "osteotomy_analysis.txt")

    with open(arquivo, "w", encoding="utf-8") as f:
        f.write("OSTEOTOMY ANALYSIS REPORT\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Planned Object: {obj1.name}\n")
        f.write(f"Operated Object: {obj2.name}\n\n")
        f.write("TRANSLATION:\n")
        f.write(f"  ΔX = {translacao.x:.5f} mm\n")
        f.write(f"  ΔY = {translacao.y:.5f} mm\n")
        f.write(f"  ΔZ = {translacao.z:.5f} mm\n")
        f.write(f"  Total distance = {distancia:.5f} mm\n\n")
        f.write("ROTATION:\n")
        for i, ang in enumerate(angulos):
            f.write(f"  Vertex {i+1}: {ang:.2f}°\n")
        if angulos:
            f.write(f"  Average: {sum(angulos)/len(angulos):.2f}°\n")

    print(f"\n   📄 Results saved to: {arquivo}")

print("=" * 60)