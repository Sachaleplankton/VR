#include "MyBlueprintFunctionLibrary.h"
#include "Components/StaticMeshComponent.h"
#include "Engine/StaticMesh.h"

int32 UMyBlueprintFunctionLibrary::GetMaterialIndexFromHit(const FHitResult& HitResult)
{
    UStaticMeshComponent* MeshComp = Cast<UStaticMeshComponent>(HitResult.GetComponent());
    if (!MeshComp || !MeshComp->GetStaticMesh())
    {
        return -1;
    }

    // Indice du triangle (primitive) touché
    int32 TriangleIndex = HitResult.FaceIndex;

    // Récupère le LOD 0
    const FStaticMeshLODResources& LOD = MeshComp->GetStaticMesh()->GetRenderData()->LODResources[0];

    for (int32 SectionIndex = 0; SectionIndex < LOD.Sections.Num(); ++SectionIndex)
    {
        const FStaticMeshSection& Section = LOD.Sections[SectionIndex];

        // Calcul de l'ID du premier triangle de la section
        int32 StartPrim = Section.FirstIndex / 3;
        int32 NumPrim = Section.NumTriangles;

        if (TriangleIndex >= StartPrim
            && TriangleIndex < StartPrim + NumPrim)
        {
            return Section.MaterialIndex;
        }
    }

    return -1;
}


