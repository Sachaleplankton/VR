#include "UMyFileUtils.h"
#include "HAL/FileManager.h"
#include "Misc/Paths.h"

TArray<FString> UMyFileUtils::GetFBXAndOBJFilesInFolder(const FString& RelativeOrAbsoluteFolderPath)
{
    TArray<FString> Result;

    // Convert to absolute path if needed
    FString FolderPath = FPaths::ConvertRelativePathToFull(RelativeOrAbsoluteFolderPath);

    // Ensure folder ends with "/"
    FPaths::NormalizeDirectoryName(FolderPath);
    if (!FolderPath.EndsWith("/"))
    {
        FolderPath += "/";
    }

    // Wildcards
    TArray<FString> FoundFiles;

    // Look for both .fbx and .obj
    IFileManager::Get().FindFiles(FoundFiles, *(FolderPath + "*.fbx"), true, false);
    Result.Append(FoundFiles);

    FoundFiles.Empty();
    IFileManager::Get().FindFiles(FoundFiles, *(FolderPath + "*.obj"), true, false);
    Result.Append(FoundFiles);

    return Result;
}