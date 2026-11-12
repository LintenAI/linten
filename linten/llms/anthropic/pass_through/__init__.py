from linten.linten_core_utils.renamed_package_shim import alias_renamed_package

__getattr__ = alias_renamed_package(
    __name__,
    "linten.llms.anthropic.messages",
    nested_renames=((f"{__name__}.messages", "linten.llms.anthropic.messages.native"),),
)
