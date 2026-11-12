package linten

import (
	"fmt"
	"testing"

	"github.com/hashicorp/terraform-plugin-sdk/v2/helper/resource"
	"github.com/hashicorp/terraform-plugin-sdk/v2/terraform"
)

func TestAccLintenOrganizationMember_basic(t *testing.T) {
	resource.Test(t, resource.TestCase{
		PreCheck:  func() { testAccPreCheck(t) },
		Providers: testAccProviders,
		Steps: []resource.TestStep{
			{
				Config: testAccLintenOrganizationMemberConfig("test-org-member", "test-user-1"),
				Check: resource.ComposeTestCheckFunc(
					testAccCheckLintenOrganizationMemberExists("linten_organization_member.test_member"),
					resource.TestCheckResourceAttr("linten_organization_member.test_member", "role", "org_admin"),
					resource.TestCheckResourceAttr("linten_organization_member.test_member", "user_id", "test-user-1"),
				),
			},
		},
	})
}

func testAccCheckLintenOrganizationMemberExists(n string) resource.TestCheckFunc {
	return func(s *terraform.State) error {
		rs, ok := s.RootModule().Resources[n]
		if !ok {
			return fmt.Errorf("Not found: %s", n)
		}

		if rs.Primary.ID == "" {
			return fmt.Errorf("No ID is set")
		}

		return nil
	}
}

func testAccLintenOrganizationMemberConfig(orgAlias, userID string) string {
	return fmt.Sprintf(`
resource "linten_model" "test_model" {
  model_name          = "gpt-3.5-turbo"
  custom_llm_provider = "openai"
  base_model          = "gpt-3.5-turbo"
}

resource "linten_organization" "test_org" {
  organization_alias = "%s"
  max_budget         = 100.0
  budget_duration    = "30d"
  
  depends_on = [linten_model.test_model]
}

resource "linten_organization_member" "test_member" {
  organization_id = linten_organization.test_org.id
  user_id         = "%s"
  user_email      = "%s@example.com"
  role            = "org_admin"
}
`, orgAlias, userID, userID)
}
