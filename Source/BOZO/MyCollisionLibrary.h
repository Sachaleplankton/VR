#pragma once

#include "Kismet/BlueprintFunctionLibrary.h"
#include "MyCollisionLibrary.generated.h"

UCLASS()
class BOZO_API UMyCollisionLibrary : public UBlueprintFunctionLibrary
{
    GENERATED_BODY()

public:
    UFUNCTION(BlueprintCallable, Category = "Collision")
    static void GenerateSimpleAndComplexCollision(UStaticMesh* Mesh);
};
