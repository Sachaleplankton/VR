// Fill out your copyright notice in the Description page of Project Settings.

using UnrealBuildTool;
using System.IO;

public class BOZO : ModuleRules
{
    public BOZO(ReadOnlyTargetRules Target) : base(Target)
    {
        // 1) Mode de PCH
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

        // 2) (Optionnel) Si vous avez besoin d'inclure manuellement
        //    des headers du plugin Assimp dans votre code BOZO C++ :
        //
        // string ProjectRoot       = Path.GetFullPath(Path.Combine(ModuleDirectory, "..", ".."));
        // string AssimpIncludePath = Path.Combine(ProjectRoot, "Plugins", "UE4_Assimp", "Source", "UE_Assimp", "Public");
        // PublicIncludePaths.Add(AssimpIncludePath);

        // 3) Modules dont BOZO dépend directement
        PublicDependencyModuleNames.AddRange(new string[]
        {
            "Core",
            "CoreUObject",
            "Engine",
            "InputCore",

            // pour exposer vos UFUNCTION(BlueprintCallable) dans 
            // UBlueprintFunctionLibrary
            "Kismet",

            // pour votre plugin Assimp (si votre code BOZO l'utilise)
            "UE_Assimp"
        });

        // 4) Modules privés (à compléter si besoin)
        PrivateDependencyModuleNames.AddRange(new string[]
        {
            // "Slate",
            // "SlateCore",
        });

        // 5) Modules chargés dynamiquement (si besoin)
        DynamicallyLoadedModuleNames.AddRange(new string[]
        {
            // ex: "OnlineSubsystemSteam"
        });
    }
}
