#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "UMyFileUtils.generated.h" 



UCLASS()
class BOZO_API UMyFileUtils : public UBlueprintFunctionLibrary
{
    GENERATED_BODY()

public:
    UFUNCTION(BlueprintCallable, Category = "File IO")
    static TArray<FString> GetFBXAndOBJFilesInFolder(const FString& RelativeOrAbsoluteFolderPath);
};