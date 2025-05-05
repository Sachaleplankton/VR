#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "Engine/StaticMesh.h"
#include "PhysicsEngine/ConvexElem.h"
#include "PhysicsEngine/BodySetup.h"
#include "Components/StaticMeshComponent.h"
#include "AutoConvexCollisionLibrary.generated.h"

UCLASS()
class BOZO_API UAutoConvexCollisionLibrary : public UBlueprintFunctionLibrary
{
    GENERATED_BODY()

public:

    /**
     * Function to create auto convex collision for a Static Mesh object.
     * Sets its collision complexity to Simple and Convex.
     *
     * @param StaticMesh The Static Mesh to modify.
     */
    UFUNCTION(BlueprintCallable, Category = "Collision")
    static void CreateAutoConvexCollision(UStaticMesh* StaticMesh);
};
