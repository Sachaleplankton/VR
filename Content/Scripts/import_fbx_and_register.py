import unreal
from pathlib import Path

# --- CONFIGURATION ---
FBX_SOURCE_DIR = Path("C:/Unreal Projects/fichiersFBX")
FBX_DEST = "/Game/Meshes"
BP_DEST = "/Game/Blueprints"

# --- FBX IMPORT UTILS ---

def build_options() -> unreal.FbxImportUI:
    options = unreal.FbxImportUI()
    options.set_editor_property("import_mesh", True)
    options.set_editor_property("import_textures", False)
    options.set_editor_property("import_materials", False)
    options.set_editor_property("import_as_skeletal", False)
    options.static_mesh_import_data.set_editor_property("import_uniform_scale", 1.0)
    options.static_mesh_import_data.set_editor_property("combine_meshes", True)
    options.static_mesh_import_data.set_editor_property("auto_generate_collision", True)
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

# --- BLUEPRINT CREATION ---

def make_blueprint(package_path, asset_name):
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    
    # ✅ Crée le dossier s'il n'existe pas
    if not unreal.EditorAssetLibrary.does_directory_exist(package_path):
        unreal.EditorAssetLibrary.make_directory(package_path)

    # ✅ Vérifie si un blueprint avec le même nom existe déjà
    full_path = f"{package_path}/{asset_name}"
    if unreal.EditorAssetLibrary.does_asset_exist(full_path):
        unreal.EditorAssetLibrary.delete_asset(full_path)

    # Crée le Blueprint
    bp_factory = unreal.BlueprintFactory()
    bp_factory.set_editor_property("ParentClass", unreal.Actor)

    bp = asset_tools.create_asset(
        asset_name=asset_name,
        package_path=package_path,
        asset_class=unreal.Blueprint,
        factory=bp_factory
    )

    if not bp:
        raise Exception(f"❌ Échec de la création du Blueprint '{asset_name}' dans '{package_path}'")
    
    return bp
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
        print(f"\n🔧 Création de {bp_name}")

        bp = make_blueprint(BP_DEST, bp_name)
        add_static_mesh_component_to_blueprint(bp, mesh_path)

    print("\n✅ Tous les Blueprints ont été créés et configurés avec leurs StaticMesh.")

if __name__ == "__main__":
    main()
