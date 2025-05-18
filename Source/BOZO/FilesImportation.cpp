#include "FilesImportation.h"
#include "HAL/FileManager.h"
#include "Misc/Paths.h"

void UFilesImportation::GetFBXFilesInFolder(
    const FString& RelativeOrAbsoluteFolderPath,
    TArray<FString>& OutFilenames,
    bool& Success)
{
    OutFilenames.Empty();
    Success = false;

    // --- Conversion robuste du chemin Unreal vers un chemin disque ---
    FString FolderPath;
    if (RelativeOrAbsoluteFolderPath.StartsWith(TEXT("/Game/")))
    {
        // Retire "/Game/" et préfixe par le dossier Content du projet
        const FString RelativePath = RelativeOrAbsoluteFolderPath.Mid(6);
        FolderPath = FPaths::ProjectContentDir() / RelativePath;
    }
    else
    {
        // Chemin classique (absolu ou relatif)
        FolderPath = FPaths::ConvertRelativePathToFull(RelativeOrAbsoluteFolderPath);
    }

    // --- Debug log pour vérifier le chemin final ---
    UE_LOG(LogTemp, Warning, TEXT("Searching folder: %s"), *FolderPath);

    // --- Normalisation du dossier ---
    FPaths::NormalizeDirectoryName(FolderPath);
    if (!FolderPath.EndsWith("/"))
    {
        FolderPath += "/";
    }

    // --- Recherche des fichiers .fbx et .obj ---
    TArray<FString> FoundFiles;
    IFileManager::Get().FindFiles(FoundFiles, *(FolderPath + TEXT("*.fbx")), true, false);
    for (const FString& FileName : FoundFiles)
    {
        OutFilenames.Add(FolderPath + FileName);
    }

    FoundFiles.Empty();
    IFileManager::Get().FindFiles(FoundFiles, *(FolderPath + TEXT("*.obj")), true, false);
    for (const FString& FileName : FoundFiles)
    {
        OutFilenames.Add(FolderPath + FileName);
    }

    // --- Succès si au moins un fichier trouvé ---
    Success = (OutFilenames.Num() > 0);
    UE_LOG(LogTemp, Warning, TEXT("Found %d files"), OutFilenames.Num());
}
