if (_JsonValue.HasMember(GLTFTEXT("KHR_draco_mesh_compression")) && _JsonValue[GLTFTEXT("KHR_draco_mesh_compression")].IsObject())
{
    std::shared_ptr<SKHR_draco_mesh_compressionextension> extension;
    if (!(extension << _JsonValue[GLTFTEXT("KHR_draco_mesh_compression")])) return false;
    _rData.properties.insert(std::make_pair(GLTFTEXT("KHR_draco_mesh_compression"), extension));
}
if (_JsonValue.HasMember(GLTFTEXT("KHR_materials_pbrSpecularGlossiness")) && _JsonValue[GLTFTEXT("KHR_materials_pbrSpecularGlossiness")].IsObject())
{
    std::shared_ptr<SKHR_materials_pbrSpecularGlossinessglTFextension> extension;
    if (!(extension << _JsonValue[GLTFTEXT("KHR_materials_pbrSpecularGlossiness")])) return false;
    _rData.properties.insert(std::make_pair(GLTFTEXT("KHR_materials_pbrSpecularGlossiness"), extension));
}
if (_JsonValue.HasMember(GLTFTEXT("KHR_materials_unlit")) && _JsonValue[GLTFTEXT("KHR_materials_unlit")].IsObject())
{
    std::shared_ptr<SKHR_materials_unlitglTFextension> extension;
    if (!(extension << _JsonValue[GLTFTEXT("KHR_materials_unlit")])) return false;
    _rData.properties.insert(std::make_pair(GLTFTEXT("KHR_materials_unlit"), extension));
}
if (_JsonValue.HasMember(GLTFTEXT("KHR_techniques_webgl")) && _JsonValue[GLTFTEXT("KHR_techniques_webgl")].IsObject())
{
    std::shared_ptr<SKHR_techniques_webglmaterialextension> extension;
    if (!(extension << _JsonValue[GLTFTEXT("KHR_techniques_webgl")])) return false;
    _rData.properties.insert(std::make_pair(GLTFTEXT("KHR_techniques_webgl"), extension));
}
if (_JsonValue.HasMember(GLTFTEXT("KHR_texture_transform")) && _JsonValue[GLTFTEXT("KHR_texture_transform")].IsObject())
{
    std::shared_ptr<SKHR_texture_transformtextureInfoextension> extension;
    if (!(extension << _JsonValue[GLTFTEXT("KHR_texture_transform")])) return false;
    _rData.properties.insert(std::make_pair(GLTFTEXT("KHR_texture_transform"), extension));
}
if (_JsonValue.HasMember(GLTFTEXT("ADOBE_materials_thin_transparency")) && _JsonValue[GLTFTEXT("ADOBE_materials_thin_transparency")].IsObject())
{
    std::shared_ptr<SADOBE_materials_thin_transparencyglTFextension> extension;
    if (!(extension << _JsonValue[GLTFTEXT("ADOBE_materials_thin_transparency")])) return false;
    _rData.properties.insert(std::make_pair(GLTFTEXT("ADOBE_materials_thin_transparency"), extension));
}
if (_JsonValue.HasMember(GLTFTEXT("AGI_articulations")) && _JsonValue[GLTFTEXT("AGI_articulations")].IsObject())
{
    std::shared_ptr<SAGI_articulationsglTFextension> extension;
    if (!(extension << _JsonValue[GLTFTEXT("AGI_articulations")])) return false;
    _rData.properties.insert(std::make_pair(GLTFTEXT("AGI_articulations"), extension));
}
if (_JsonValue.HasMember(GLTFTEXT("AGI_stk_metadata")) && _JsonValue[GLTFTEXT("AGI_stk_metadata")].IsObject())
{
    std::shared_ptr<SAGI_stk_metadataglTFextension> extension;
    if (!(extension << _JsonValue[GLTFTEXT("AGI_stk_metadata")])) return false;
    _rData.properties.insert(std::make_pair(GLTFTEXT("AGI_stk_metadata"), extension));
}
if (_JsonValue.HasMember(GLTFTEXT("EXT_texture_webp")) && _JsonValue[GLTFTEXT("EXT_texture_webp")].IsObject())
{
    std::shared_ptr<SEXT_texture_webpglTFextension> extension;
    if (!(extension << _JsonValue[GLTFTEXT("EXT_texture_webp")])) return false;
    _rData.properties.insert(std::make_pair(GLTFTEXT("EXT_texture_webp"), extension));
}
if (_JsonValue.HasMember(GLTFTEXT("MSFT_lod")) && _JsonValue[GLTFTEXT("MSFT_lod")].IsObject())
{
    std::shared_ptr<SMSFT_lodglTFextension> extension;
    if (!(extension << _JsonValue[GLTFTEXT("MSFT_lod")])) return false;
    _rData.properties.insert(std::make_pair(GLTFTEXT("MSFT_lod"), extension));
}
if (_JsonValue.HasMember(GLTFTEXT("MSFT_texture_dds")) && _JsonValue[GLTFTEXT("MSFT_texture_dds")].IsObject())
{
    std::shared_ptr<SMSFT_texture_ddsextension> extension;
    if (!(extension << _JsonValue[GLTFTEXT("MSFT_texture_dds")])) return false;
    _rData.properties.insert(std::make_pair(GLTFTEXT("MSFT_texture_dds"), extension));
}
_rData.schemaType = GLTFTEXT("extension.schema.json");
return true;