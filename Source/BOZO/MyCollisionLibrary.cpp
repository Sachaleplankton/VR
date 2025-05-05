#include "AutoConvexCollisionLibrary.h"
#include "Engine/StaticMesh.h"
#include "PhysicsEngine/ConvexElem.h"
#include "PhysicsEngine/BodySetup.h"
#include "Components/StaticMeshComponent.h"
#include "Engine/World.h"
#include "GameFramework/Actor.h"

void UAutoConvexCollisionLibrary::CreateAutoConvexCollision(UStaticMesh* StaticMesh)
{
    if (StaticMesh)
    {
        // Create a temporary StaticMeshComponent to access the collision data
        UStaticMeshComponent* StaticMeshComponent = NewObject<UStaticMeshComponent>(GEngine->GetWorld(), UStaticMeshComponent::StaticClass());

        if (StaticMeshComponent)
        {
            // Set the mesh on the component
            StaticMeshComponent->SetStaticMesh(StaticMesh);

            // Access the BodySetup through the StaticMeshComponent
            UBodySetup* BodySetup = StaticMeshComponent->GetBodySetup();

            if (BodySetup)
            {
                // Clear any existing convex hulls
                BodySetup->AggGeom.ConvexElems.Empty();

                // Create and add a new convex collision
                FKConvexElem NewConvexElem;
                BodySetup->AggGeom.ConvexElems.Add(NewConvexElem);

                // Apply the new body setup with convex collision to the mesh
                BodySetup->CreatePhysicsMeshes();
            }

            // Set the collision enabled and response for StaticMeshComponent
            StaticMeshComponent->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);
            StaticMeshComponent->SetCollisionResponseToAllChannels(ECR_Block);

            // Set the body setup to use simple collision
            StaticMeshComponent->SetCollisionProfileName(TEXT("BlockAll"));

            // Correct access to set generate overlap events
            StaticMeshComponent->SetGenerateOverlapEvents(true);  // Enable overlap events

            // Enable physics simulation
            StaticMeshComponent->SetSimulatePhysics(true);  // Set simulate physics to true
        }
    }
}
