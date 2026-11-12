package main

import (
	"github.com/LintenAI/terraform-provider-linten/linten"
	"github.com/hashicorp/terraform-plugin-sdk/v2/plugin"
)

// main is the entry point for the plugin. It serves the provider
// using the Terraform plugin SDK.
func main() {
	plugin.Serve(&plugin.ServeOpts{
		ProviderFunc: linten.Provider,
	})
}
