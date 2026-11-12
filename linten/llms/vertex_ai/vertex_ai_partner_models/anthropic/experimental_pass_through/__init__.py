from linten.linten_core_utils.renamed_package_shim import alias_renamed_package

__getattr__ = alias_renamed_package(__name__, "linten.llms.vertex_ai.vertex_ai_partner_models.anthropic.messages")
