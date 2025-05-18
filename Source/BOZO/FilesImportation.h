#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "FilesImportation.generated.h"

UCLASS()
class BOZO_API UFilesImportation : public UBlueprintFunctionLibrary
{
    GENERATED_BODY()

public:
    /**
     * R�cup�re tous les fichiers .fbx et .obj dans le dossier sp�cifi� (chemin relatif ou absolu).
     * @param RelativeOrAbsoluteFolderPath  Chemin relatif ou absolu vers le dossier � scanner.
     * @param OutFilenames                  (out) Tableau des chemins complets des fichiers trouv�s.
     * @param Success                       (out) true si au moins un fichier a �t� trouv�.
     */
    UFUNCTION(BlueprintCallable, Category = "File IO")
    static void GetFBXFilesInFolder(
        const FString& RelativeOrAbsoluteFolderPath,
        TArray<FString>& OutFilenames,
        bool& Success
    );
};
