import unreal
from pathlib import Path

# --- CONFIGURATION ---
FBX_SOURCE_DIR = Path("C:/Unreal Projects/fichiersFBX")
FBX_DEST = "/Game/Meshes"
BP_DEST = "/Game/Blueprints"
TEMPLATE_BP = "/Game/Models/Meshes/BuildActor"

# --- FBX IMPORT UTILS ---

def build_options() -> unreal.FbxImportUI:
    options = unreal.FbxImportUI()
    options.import_mesh = True
    options.import_textures = True
    options.import_materials = True
    options.import_as_skeletal = False

    sm_data = options.static_mesh_import_data
    sm_data.combine_meshes = True
    sm_data.import_uniform_scale = 1.0
    sm_data.import_translation = unreal.Vector(0, 0, 0)
    sm_data.import_rotation = unreal.Rotator(0, 0, 0)
    sm_data.generate_lightmap_u_vs = True
    sm_data.auto_generate_collision = True

    return options


def build_import_task(mesh_name: str, filename: Path, destination_path: str, options: unreal.FbxImportUI):
    task = unreal.AssetImportTask()
    task.set_editor_property("automated", True)
    task.set_editor_property("destination_name", mesh_name)
    task.set_editor_property("destination_path", destination_path)
    task.set_editor_property("filename", str(filename))
    task.set_editor_property("replace_existing", True)
    task.set_editor_property("save", True)
    task.set_editor_property("options", options)
    return task

def find_fbx_files(source_dir: Path) -> dict:
    return {
        f"SM_{file.stem}": file
        for file in source_dir.glob("*.fbx")
    }

def import_all_meshes(mesh_data: dict):
    options = build_options()
    tasks = [
        build_import_task(name, fbx_path, FBX_DEST, options)
        for name, fbx_path in mesh_data.items()
    ]
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)

# --- BLUEPRINT DUPLICATION ---

def duplicate_blueprint(source_path: str, dest_path: str):
    if not unreal.EditorAssetLibrary.does_asset_exist(source_path):
        raise Exception(f"❌ Le Blueprint source n'existe pas : {source_path}")

    # Supprimer l'ancien asset s'il existe
    if unreal.EditorAssetLibrary.does_asset_exist(dest_path):
        unreal.EditorAssetLibrary.delete_asset(dest_path)

    source_bp = unreal.EditorAssetLibrary.load_asset(source_path)
    if not isinstance(source_bp, unreal.Blueprint):
        raise Exception(f"❌ L'asset source n'est pas un Blueprint : {source_path}")

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    package_path = "/".join(dest_path.split("/")[:-1])
    asset_name = dest_path.split("/")[-1]

    # Dupliquer le blueprint
    duplicated_bp = asset_tools.duplicate_asset(asset_name, package_path, source_bp)
    if not duplicated_bp:
        raise Exception(f"❌ Échec de duplication de {source_path} vers {dest_path}")

    # Vérifie le nom de la classe générée (debug info)
    generated_class = duplicated_bp.generated_class
    print(f"✅ Blueprint '{asset_name}' dupliqué. Classe générée : {generated_class}")

    return duplicated_bp



# --- ADD STATIC MESH COMPONENT ---

def add_static_mesh_component_to_blueprint(blueprint: unreal.Blueprint, mesh_path: str, component_name: str = "MeshComponent"):
    mesh = unreal.EditorAssetLibrary.load_asset(mesh_path)
    if not isinstance(mesh, unreal.StaticMesh):
        raise Exception(f"❌ Asset non valide : {mesh_path} n'est pas un StaticMesh")

    subsystem = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
    handles = subsystem.k2_gather_subobject_data_for_blueprint(blueprint)
    if not handles:
        raise Exception("❌ Impossible de récupérer les sous-objets du blueprint.")
    
    root_handle = handles[0]

    sub_handle, fail_reason = subsystem.add_new_subobject(
        unreal.AddNewSubobjectParams(
            parent_handle=root_handle,
            new_class=unreal.StaticMeshComponent,
            blueprint_context=blueprint
        )
    )

    if not fail_reason.is_empty():
        raise Exception(f"❌ Erreur à l'ajout du composant : {fail_reason}")

    subsystem.rename_subobject(sub_handle, unreal.Text(component_name))
    subsystem.attach_subobject(owner_handle=root_handle, child_to_add_handle=sub_handle)

    bfl = unreal.SubobjectDataBlueprintFunctionLibrary
    component_obj = bfl.get_object(bfl.get_data(sub_handle))

    if not isinstance(component_obj, unreal.StaticMeshComponent):
        raise Exception("❌ Le composant récupéré n'est pas un StaticMeshComponent")

    component_obj.set_static_mesh(mesh)
    component_obj.set_editor_property("mobility", unreal.ComponentMobility.MOVABLE)

# --- FULL CHAIN ---

def main():
    print("📁 Recherche des fichiers .fbx dans :", FBX_SOURCE_DIR)
    mesh_data = find_fbx_files(FBX_SOURCE_DIR)

    if not mesh_data:
        print("❌ Aucun fichier FBX trouvé.")
        return

    print("🚀 Import FBX vers StaticMesh...")
    import_all_meshes(mesh_data)

    for mesh_name in mesh_data.keys():
        mesh_path = f"{FBX_DEST}/{mesh_name}"
        bp_name = f"BP_{mesh_name}"
        bp_path = f"{BP_DEST}/{bp_name}"
        print(f"\n🔧 Duplication de BuildActor pour {bp_name}")

        bp = duplicate_blueprint(TEMPLATE_BP, bp_path)
        add_static_mesh_component_to_blueprint(bp, mesh_path)

    print("\n✅ Tous les Blueprints ont été créés à partir de BuildActor et configurés avec leurs StaticMesh.")

if __name__ == "__main__":
    main()
