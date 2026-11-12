package linten

import (
	"github.com/hashicorp/terraform-plugin-sdk/v2/helper/schema"
)

// Provider returns a terraform.ResourceProvider.
func Provider() *schema.Provider {
	return &schema.Provider{
		ResourcesMap: map[string]*schema.Resource{
			"linten_model":                   resourceLintenModel(),
			"linten_team":                    ResourceLintenTeam(),
			"linten_organization":            resourceLintenOrganization(),
			"linten_organization_member":     resourceLintenOrganizationMember(),
			"linten_organization_member_add": resourceLintenOrganizationMemberAdd(),
			"linten_team_member":             resourceLintenTeamMember(),
			"linten_team_member_add":         resourceLintenTeamMemberAdd(),
			"linten_key":                     resourceKey(),
			"linten_mcp_server":              resourceLintenMCPServer(),
			"linten_credential":              resourceLintenCredential(),
			"linten_vector_store":            resourceLintenVectorStore(),
			"linten_jwt_key_mapping":         resourceLintenJWTKeyMapping(),
			"linten_fallback":                resourceLintenFallback(),
			"linten_key_block":               resourceLintenKeyBlock(),
			"linten_team_block":              resourceLintenTeamBlock(),
			"linten_access_group":            resourceLintenAccessGroup(),
			"linten_unified_access_group":    resourceLintenUnifiedAccessGroup(),
			"linten_guardrail":               resourceLintenGuardrail(),
			"linten_prompt":                  resourceLintenPrompt(),
			"linten_agent":                   resourceLintenAgent(),
			"linten_search_tool":             resourceLintenSearchTool(),
			"linten_user":                    resourceLintenUser(),
			"linten_budget":                  resourceLintenBudget(),
			"linten_tag":                     resourceLintenTag(),
			"linten_project":                 resourceLintenProject(),
		},
		DataSourcesMap: map[string]*schema.Resource{
			"linten_credential":            dataSourceLintenCredential(),
			"linten_vector_store":          dataSourceLintenVectorStore(),
			"linten_fallback":              dataSourceLintenFallback(),
			"linten_access_group":          dataSourceLintenAccessGroup(),
			"linten_access_groups":         dataSourceLintenAccessGroups(),
			"linten_unified_access_group":  dataSourceLintenUnifiedAccessGroup(),
			"linten_unified_access_groups": dataSourceLintenUnifiedAccessGroups(),
			"linten_guardrail":             dataSourceLintenGuardrail(),
			"linten_guardrails":            dataSourceLintenGuardrails(),
			"linten_prompt":                dataSourceLintenPrompt(),
			"linten_prompts":               dataSourceLintenPrompts(),
			"linten_agent":                 dataSourceLintenAgent(),
			"linten_agents":                dataSourceLintenAgents(),
			"linten_search_tool":           dataSourceLintenSearchTool(),
			"linten_search_tools":          dataSourceLintenSearchTools(),
			"linten_user":                  dataSourceLintenUser(),
			"linten_users":                 dataSourceLintenUsers(),
			"linten_budget":                dataSourceLintenBudget(),
			"linten_budgets":               dataSourceLintenBudgets(),
			"linten_tag":                   dataSourceLintenTag(),
			"linten_tags":                  dataSourceLintenTags(),
			"linten_project":               dataSourceLintenProject(),
			"linten_projects":              dataSourceLintenProjects(),
			"linten_key":                   dataSourceLintenKey(),
			"linten_keys":                  dataSourceLintenKeys(),
			"linten_team":                  dataSourceLintenTeam(),
			"linten_teams":                 dataSourceLintenTeams(),
			"linten_model":                 dataSourceLintenModel(),
			"linten_models":                dataSourceLintenModels(),
			"linten_organization":          dataSourceLintenOrganization(),
			"linten_organizations":         dataSourceLintenOrganizations(),
			"linten_mcp_server":            dataSourceLintenMCPServer(),
			"linten_mcp_servers":           dataSourceLintenMCPServers(),
		},
		Schema: map[string]*schema.Schema{
			"api_base": {
				Type:        schema.TypeString,
				Required:    true,
				Sensitive:   false,
				DefaultFunc: schema.EnvDefaultFunc("LINTEN_API_BASE", nil),
				Description: "The base URL of the Linten API",
			},
			"api_key": {
				Type:        schema.TypeString,
				Required:    true,
				Sensitive:   true,
				DefaultFunc: schema.EnvDefaultFunc("LINTEN_API_KEY", nil),
				Description: "The API key for authenticating with Linten",
			},
			"insecure_skip_verify": {
				Type:        schema.TypeBool,
				Optional:    true,
				Default:     false,
				DefaultFunc: schema.EnvDefaultFunc("LINTEN_INSECURE_SKIP_VERIFY", false),
				Description: "Skip TLS certificate verification. Only use for development or when using self-signed certificates",
			},
		},
		ConfigureFunc: providerConfigure,
	}
}

// providerConfigure configures the provider with the given schema data.
func providerConfigure(d *schema.ResourceData) (interface{}, error) {
	config := ProviderConfig{
		APIBase:            d.Get("api_base").(string),
		APIKey:             d.Get("api_key").(string),
		InsecureSkipVerify: d.Get("insecure_skip_verify").(bool),
	}

	return NewClient(config.APIBase, config.APIKey, config.InsecureSkipVerify), nil
}
